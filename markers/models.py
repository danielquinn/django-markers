import colorsys
import hashlib
import os
import re

from django.conf import settings
from django.contrib.staticfiles.finders import (
    AppDirectoriesFinder,
    FileSystemFinder,
)
from django.template.defaultfilters import escape

import numpy

from PIL import Image, ImageChops, ImageDraw, ImageFont

from .exceptions import (
    InvalidColourError,
    InvalidHueError,
    InvalidOpacityError,
    InvalidTemplateError,
)


class Marker:

    template = None
    hue = None
    opacity = None
    text = None
    text_position = None
    text_size = None
    text_colour = None

    rgb_to_hsv = numpy.vectorize(colorsys.rgb_to_hsv)
    hsv_to_rgb = numpy.vectorize(colorsys.hsv_to_rgb)

    def __init__(
        self,
        template,
        hue=0,
        opacity=1,
        text="",
        text_position=(None, None),
        text_size=10,
        text_colour="000000",
    ):
        """
        Dynamic marker creation

          Required:
            template: The path to file used as the basis for this marker
          Optional:
            opacity:       The opacity of the finished marker
            hue:           A value between 0 and 360 dictating how to colourise the template
            text:          The text string, if any to apply
            text_position: The position of the text
            text_size:     The size of the font used
            text_colour:   The colour of the text, in hexadecimal
        """

        try:
            self.hue = int(hue)
            assert self.hue >= 0 and self.hue <= 360
        except (ValueError, AssertionError):
            raise InvalidHueError(
                "Hue must be an integer between -180 and 180"
            )

        if not re.match("^[a-fA-F0-9]{6}$", text_colour):
            raise InvalidColourError(
                "%s does not appear to be a hex colour" % text_colour
            )

        if not isinstance(opacity, (int, float)) or opacity > 1 or opacity < 0:
            raise InvalidOpacityError(
                "Opacity must be a float or integer <= 1 and >= 0"
            )

        if self.hue:
            self.template = self._build_template_from_rgb(template)
        else:
            self.template = self._check_template_exists(template)

        self.opacity = int(float(opacity) * float(255))
        self.text = text
        self.text_position = list(text_position)
        self.text_size = text_size
        self.text_colour = text_colour

        self._hash = hashlib.md5(
            (
                "%s-%s-%s-%s-%s-%s-%s"
                % (
                    self.template,
                    self.hue,
                    self.opacity,
                    self.text,
                    self.text_position,
                    self.text_size,
                    self.text_colour,
                )
            ).encode("utf-8")
        ).hexdigest()

    def get_marker(self):
        """
        Returns a compiled marker image object
        """
        return self._get_marker()

    def get_marker_url(self):
        return self._get_marker().filename.replace(
            settings.MEDIA_ROOT, settings.MEDIA_URL
        )

    def _get_marker(self):

        cache_file = os.path.join(
            settings.MEDIA_ROOT, "cache", "markers", "%s.png" % self._hash
        )

        try:

            return Image.open(cache_file)

        except IOError:

            base = self._get_base_image()
            text_overlay, text_alpha = self._get_text_layer(base)
            base.paste(text_overlay, (0, 0), text_alpha)

            try:
                os.makedirs(os.path.dirname(cache_file))
            except:
                pass  # Directory exists, as it should

            base.save(cache_file, "PNG")

            return self._get_marker()

    def _get_base_image(self):

        # We need the final image dimensions, so we start here
        template = Image.open(self.template, "r")

        # Create a base, transparent image
        base = Image.new("RGBA", template.size)
        template_alpha = Image.new("L", template.size, self.opacity)

        base.paste(template, (0, 0), template_alpha)

        return base

    def _get_text_layer(self, base):

        #
        # Most of this logic was adapted from
        # http://xxki.com/tutorial/pukiwiki.php?Python%2FPIL
        #

        # Create a transparent text image
        text_overlay = Image.new("RGB", base.size, (0, 0, 0))
        text_alpha = Image.new("L", text_overlay.size, "black")

        # Make a grayscale image of the font, white on black.
        image_text = Image.new("L", text_overlay.size, 0)
        draw_text = ImageDraw.Draw(image_text)

        font_path = os.path.join(
            os.path.dirname(__file__),
            "static",
            "markers",
            "fonts",
            "DroidSans-Bold.ttf",
        )

        # Thanks to http://stackoverflow.com/questions/1970807/center-middle-align-text-with-pil

        image_width, image_height = base.size
        text_width, text_height = draw_text.textsize(self.text)

        if self.text_position[0] is None:
            self.text_position[0] = (image_width - text_width) / 2
        if self.text_position[1] is None:
            self.text_position[1] = (image_height - text_height) / 2

        font = ImageFont.truetype(font_path, self.text_size)
        draw_text.text(
            self.text_position, escape(self.text), font=font, fill="white"
        )

        # Add the white text to our collected alpha channel. Gray pixels around
        # the edge of the text will eventually become partially transparent
        # pixels in the alpha channel.
        text_alpha = ImageChops.lighter(text_alpha, image_text)

        # Make a solid color, and add it to the color layer on every pixel
        # that has even a little bit of alpha showing.
        solidcolor = Image.new(
            "RGBA", text_overlay.size, "#%s" % self.text_colour
        )
        immask = Image.eval(image_text, lambda p: 255 * (int(p != 0)))
        text_overlay = Image.composite(solidcolor, text_overlay, immask)
        text_overlay.putalpha(text_alpha)

        return text_overlay, text_alpha

    def _check_template_filename(self, path):

        m = re.match(r"^(.*)\.(\w+)$", path)
        if not m:
            raise InvalidTemplateError(
                "The template path supplied does not look like it points to an image file"
            )

        return m.group(1), m.group(2)

    def _check_template_exists(self, path):

        template = FileSystemFinder().find(path)
        if not template:
            template = AppDirectoriesFinder().find(path)
        if not template:
            raise InvalidTemplateError("%s is not a known template" % path)

        return template

    def _build_template_from_rgb(self, template):

        image = self._colourize(
            Image.open(self._check_template_exists(template), "r")
        )

        to_hash = ("%s-%s" % (template, self.hue)).encode("ascii")
        working_filename = os.path.join(
            settings.MEDIA_ROOT,
            "cache",
            "markers",
            "_workspace",
            "%s.png" % hashlib.md5(to_hash).hexdigest(),
        )

        try:
            os.makedirs(os.path.dirname(working_filename))
        except:
            pass  # Directory exists, and that's cool

        image.save(working_filename, "PNG")

        return working_filename

    #
    # The following methods were shamelessly ripped from StackOverflow and are
    # practically voodoo to me.
    #
    # Reference:
    #   http://stackoverflow.com/questions/7274221/
    #

    def _shift_hue(self, arr, hout):

        r, g, b, a = numpy.rollaxis(arr, axis=-1)
        h, s, v = self.rgb_to_hsv(r, g, b)
        h = hout
        r, g, b = self.hsv_to_rgb(h, s, v)
        arr = numpy.dstack((r, g, b, a))

        return arr

    def _colourize(self, image):

        return Image.fromarray(
            self._shift_hue(
                numpy.array(
                    numpy.asarray(image.convert("RGBA")).astype("float")
                ),
                self.hue / float(360),
            ).astype("uint8"),
            "RGBA",
        )

import hashlib, os, re

from django.conf import settings
from django.contrib.staticfiles.finders import FileSystemFinder, AppDirectoriesFinder

from PIL import Image, ImageDraw, ImageFont, ImageChops

class InvalidTemplateError(StandardError):
    pass



class InvalidColourError(StandardError):
    pass



class InvalidOpacityError(StandardError):
    pass



class Marker(object):

    template = None
    opacity  = None
    text     = None
    position = None
    size     = None
    colour   = None

    def __init__(self, template=None, opacity=1, text="", position=(0,0), size=10, colour="000000"):

        self.template = FileSystemFinder().find(template)
        if not self.template:
            self.template = AppDirectoriesFinder().find(template)
        if not self.template:
            raise InvalidTemplateError("%s is not a known template" % template)

        if not re.match("^[a-fA-F0-9]{6}$", colour):
            raise InvalidColourError("%s does not appear to be a hex colour" % colour)

        if not isinstance(opacity, (int,float)) or opacity > 1 or opacity < 0:
            raise InvalidOpacityError("Opacity must be a float or integer <= 1 and >= 0")

        self.opacity  = int(float(opacity) * float(255))
        self.text     = text
        self.position = position
        self.size     = size
        self.colour   = colour

        self._hash = hashlib.md5(
            "%s-%s-%s-%s-%s-%s" % (
                self.template,
                self.opacity,
                self.text,
                self.position,
                self.size,
                self.colour
            )
        ).hexdigest()


    def get_marker(self):
        """
        Returns a compiled marker image object
        """

        return self._get_marker()


    def get_marker_url(self):

        marker = self._get_marker()
        return marker.filename.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)


    def _get_marker(self):

        cache_file = os.path.join(settings.MEDIA_ROOT, "cache", "markers", "%s.png" % self._hash)
        try:
            return Image.open(cache_file)
        except IOError:
            base = self._get_base_image()
            text_overlay, text_alpha = self._get_text_layer(base)
            base.paste(text_overlay, (0,0), text_alpha)
            base.save(cache_file, "PNG")
            return self._get_marker()


    def _get_base_image(self):

        # We need the final image dimensions, so we start here
        template = Image.open(self.template, "r")

        # Create a base, transparent image
        base = Image.new("RGBA", template.size)
        template_alpha = Image.new("L", template.size, self.opacity)

        base.paste(template, (0,0), template_alpha)

        return base


    def _get_text_layer(self, base):

        # 2. Create a transparent text image
        text_overlay = Image.new("RGB", base.size, (0,0,0))
        text_alpha   = Image.new("L", text_overlay.size, "black")

        # Make a grayscale image of the font, white on black.
        image_text = Image.new("L", text_overlay.size, 0)
        draw_text = ImageDraw.Draw(image_text)
        font = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, "cartography", "fonts", "DroidSans-Bold.ttf"), self.size)
        draw_text.text(self.position, self.text, font=font, fill="white")

        # Add the white text to our collected alpha channel. Gray pixels around
        # the edge of the text will eventually become partially transparent
        # pixels in the alpha channel.
        text_alpha = ImageChops.lighter(text_alpha, image_text)

        # Make a solid color, and add it to the color layer on every pixel
        # that has even a little bit of alpha showing.
        solidcolor = Image.new("RGBA", text_overlay.size, "#%s" % self.colour)
        immask = Image.eval(image_text, lambda p: 255 * (int(p != 0)))
        text_overlay = Image.composite(solidcolor, text_overlay, immask)
        text_overlay.putalpha(text_alpha)
        # overlay.save("transtext.png", "PNG") #save for testing

        return text_overlay, text_alpha

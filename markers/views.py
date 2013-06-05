from __future__ import absolute_import

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View

from .models import Marker
from .exceptions import (
    InvalidTemplateError, 
    InvalidColourError, 
    InvalidOpacityError, 
    InvalidHueError
)

class MarkerView(View):

    def get(self, request, template=None, *args, **kwargs):

        text_x = self.request.GET.get("text_x")
        if text_x and text_x.isdigit():
            text_x = int(text_x)

        text_y = self.request.GET.get("text_y")
        if text_y and text_y.isdigit():
            text_y = int(text_y)

        try:
            marker = Marker(
                template=template,
                hue=self._get_float("hue", 0),
                text=request.GET.get("text",""),
                text_position=(text_x, text_y),
                text_size=self._get_int("text_size", 11),
                text_colour=self.request.GET.get("text_colour", "000000"),
                opacity=self._get_float("opacity", 1)
            )
        except (InvalidTemplateError, InvalidColourError, InvalidOpacityError, InvalidHueError) as e:
            return HttpResponseBadRequest(e)

        response = HttpResponse(mimetype="image/png")
        marker.get_marker().save(response, "PNG")

        return response


    def _get_float(self, key, default):

        r = default
        try:
            r = float(self.request.GET.get(key, r))
        except ValueError:
            pass

        return r


    def _get_int(self, key, default):

        r = default
        try:
            r = int(self.request.GET.get(key, r))
        except ValueError:
            pass

        return r

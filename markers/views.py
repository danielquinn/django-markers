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

        opacity = request.GET.get("opacity", 1)
        try:
            opacity = float(opacity)
        except ValueError:
            opacity = 1

        try:
            marker = Marker(
                template=template,
                hue=self._get_int("hue", 0),
                text=request.GET.get("text",""),
                text_position=(self._get_int("text_x", 0), self._get_int("text_y", 0)),
                text_size=self._get_int("text_size", 11),
                text_colour=self.request.GET.get("text_colour", "000000"),
                opacity=opacity
            )
        except (InvalidTemplateError, InvalidColourError, InvalidOpacityError, InvalidHueError) as e:
            return HttpResponseBadRequest(e)

        response = HttpResponse(mimetype="image/png")
        marker.get_marker().save(response, "PNG")

        return response


    def _get_int(self, key, default):

        r = default
        try:
            r = int(self.request.GET.get(key, r))
        except ValueError:
            pass

        return r

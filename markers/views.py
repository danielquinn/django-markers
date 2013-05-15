from __future__ import absolute_import

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View

from .models import Marker
from .exceptions import InvalidTemplateError, InvalidColourError, InvalidOpacityError

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
                text=request.GET.get("text",""),
                position=(self._query_int("x", 0), self._query_int("y", 0)),
                size=self._query_int("size", 11),
                colour=self.request.GET.get("colour", "000000"),
                opacity=opacity
            )
        except (InvalidTemplateError, InvalidColourError, InvalidOpacityError) as e:
            return HttpResponseBadRequest(e)

        response = HttpResponse(mimetype="image/png")
        marker.get_marker().save(response, "PNG")

        return response


    def _query_int(self, key, default):

        r = default
        try:
            r = int(self.request.GET.get(key, r))
        except ValueError:
            pass

        return r

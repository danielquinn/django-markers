from django import template as django_template

from ..exceptions import InvalidTemplateError, InvalidColourError, InvalidOpacityError
from ..models import Marker

register = django_template.Library()

@register.simple_tag
def marker(template=None, opacity=1, text="", x=0, y=0, size=10, colour="000000"):

    try:
        marker = Marker(
            template=template,
            text=text,
            position=(x,y),
            size=size,
            colour=colour,
            opacity=opacity
        )
    except (InvalidTemplateError, InvalidColourError, InvalidOpacityError):
        return ""

    return marker.get_marker_url()

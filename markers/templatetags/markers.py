from django import template as django_template

from ..exceptions import (
    InvalidColourError,
    InvalidOpacityError,
    InvalidTemplateError,
)
from ..models import Marker


register = django_template.Library()


@register.simple_tag
def marker(
    template,
    hue=0,
    opacity=1,
    text="",
    text_x=None,
    text_y=None,
    text_size=10,
    text_colour="000000",
):

    try:
        m = Marker(
            template,
            hue=hue,
            opacity=opacity,
            text=text,
            text_position=(text_x, text_y),
            text_size=text_size,
            text_colour=text_colour,
        )
    except (InvalidTemplateError, InvalidColourError, InvalidOpacityError):
        return ""

    return m.get_marker_url()

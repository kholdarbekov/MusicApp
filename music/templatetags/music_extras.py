from ..models import Genre
from django import template

register = template.Library()


@register.simple_tag
def genres():
    return Genre.objects.all().values()
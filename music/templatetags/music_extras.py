import datetime

from ..models import Genre, Music
from django import template
from django.utils import timezone

register = template.Library()


@register.simple_tag
def genres():
    return Genre.objects.all().values()


@register.simple_tag
def get_new_songs():
    time = timezone.now() - datetime.timedelta(days=7)
    return Music.objects.filter(release_date__gte=time)[:30]
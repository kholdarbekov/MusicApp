import datetime

from ..models import Genre, Music, Album
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


@register.simple_tag
def get_top_albums():
    return Album.objects.order_by('-number_of_views')[:5]


@register.filter(name='playlists')
def get_user_playlists(user):
    if user.is_authenticated:
        return user.playlists.all()
    else:
        return None
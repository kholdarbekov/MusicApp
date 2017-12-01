import datetime

from ..models import Genre, Music, Album, Playlist
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
    return sorted(Album.objects.all(), key=lambda album: album.get_net_value, reverse=True)[:5]


@register.filter(name='playlists')
def get_user_playlists(user):
    if user.is_authenticated:
        return user.playlists.all()
    else:
        return None


@register.simple_tag
def get_top_playlists():
    # reversed
    return sorted(Playlist.objects.all(), key=lambda playlist: playlist.get_net_value, reverse=True)[:8]


@register.simple_tag
def get_last_playlist():
    # reversed
    playlists = sorted(Playlist.objects.all(), key=lambda playlist: playlist.get_net_value, reverse=True)
    return playlists.__getitem__(0)

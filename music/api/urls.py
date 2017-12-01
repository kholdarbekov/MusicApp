from django.conf.urls import url
from .views import PlayListCreate, get_music, TopPlaylists, TopGenres, PlaylistDetail, Search, GetUserLikedMusics, \
    TopAlbums


urlpatterns = [
    url(r'^playlist/create/$', PlayListCreate.as_view()),
    url(r'^getsong/$', get_music, name='get_music'),
    url(r'^api/search/$', Search.as_view()),
    url(r'^top-playlists/$', TopPlaylists.as_view()),
    url(r'^top-genres/$', TopGenres.as_view()),
    url(r'^api/playlist/$', PlaylistDetail.as_view()),
    url(r'^api/get-liked-musics/$', GetUserLikedMusics.as_view()),
    url(r'^api/top-albums/', TopAlbums.as_view())
]

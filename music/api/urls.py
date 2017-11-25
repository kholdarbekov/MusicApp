from django.conf.urls import url
from .views import PlayListCreate, TopPlaylists, TopGenres, PlaylistDetail


urlpatterns = [
    url(r'^playlist/create/$', PlayListCreate.as_view(), name='playlist_create'),
    url(r'^top-playlists/$', TopPlaylists.as_view(), name='top_playlists'),
    url(r'^top-genres/$', TopGenres.as_view(), name='top_genres'),
    url(r'^api/playlist/$', PlaylistDetail.as_view()),
]

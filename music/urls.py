from django.conf.urls import url
from django.views.generic import TemplateView

from .views import autocomplete_view, playListCreateView, AlbumView, PlaylistView, AllAlbumsView, add_to_playlist, search, \
    GenreView, music_like, PerformerView, playlist_follow

urlpatterns = [
    url(r'^autocomplete/', autocomplete_view, name='autocomplete-view'),
    url(r'^create-playlist/$', playListCreateView, name='create_playlist'),
    url(r'^album/(?P<pk>\d+)/$', AlbumView.as_view(), name='album'),
    url(r'^albums/$', AllAlbumsView.as_view(), name='all_albums'),
    url(r'^playlist/(?P<pk>\d+)/$', PlaylistView.as_view(), name='playlist'),
    url(r'^topplaylists/$', TemplateView.as_view(template_name='top_playlist.html'), name='top_playlists'),
    url(r'^add-to-playlist/$', add_to_playlist, name='add_to_playlist'),
    url(r'^genre/(?P<genre_name>.+)/$', GenreView.as_view(), name='genre'),
    url(r'^like/$', music_like, name='music_like'),
    url(r'^follow-playlist/$', playlist_follow, name='follow_playlist'),

    url(r'^artist/(?P<pk>\d+)/$', PerformerView.as_view(), name='performer'),

    url(r'^search/$', search, name='search'),
]

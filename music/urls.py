from django.conf.urls import url
from .views import autocomplete_view, playListCreateView, AlbumView, PlaylistView, AllAlbumsView, add_to_playlist, search

urlpatterns = [
    url(r'^autocomplete/', autocomplete_view, name='autocomplete-view'),
    url(r'^create-playlist/$', playListCreateView, name='create_playlist'),
    url(r'^album/(?P<pk>\d+)/$', AlbumView.as_view(), name='album'),
    url(r'^albums/$', AllAlbumsView.as_view(), name='all_albums'),
    url(r'^playlist/(?P<pk>\d+)/$', PlaylistView.as_view(), name='playlist'),
    url(r'^add-to-playlist/(?P<music_id>\d+)/(?P<playlist_id>\d+)/$', add_to_playlist, name='add_to_playlist'),

    url(r'^search/$', search, name='search'),
]

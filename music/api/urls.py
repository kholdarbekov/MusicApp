from django.conf.urls import url
from .views import PlayListCreate, get_music, TopPlaylists, TopGenres, PlaylistDetail, Search, GetUserLikedMusics, \
    TopAlbums, UserPlaylists, FollowPlaylist, FollowedPlaylists, AddToPlaylist, MusicLike, AlbumDetail, GenreDetail, \
    DeletePlaylist


urlpatterns = [
    url(r'^playlist/create/$', PlayListCreate.as_view()),
    url(r'^getsong/$', get_music, name='get_music'),
    url(r'^api/search/$', Search.as_view()),
    url(r'^top-playlists/$', TopPlaylists.as_view()),
    url(r'^top-genres/$', TopGenres.as_view()),
    url(r'^api/playlist/$', PlaylistDetail.as_view()),
    url(r'^api/get-liked-musics/$', GetUserLikedMusics.as_view()),
    url(r'^api/top-albums/$', TopAlbums.as_view()),
    url(r'^api/user-playlists/$', UserPlaylists.as_view()),
    url(r'^follow-playlist/$', FollowPlaylist.as_view()),
    url(r'^followed-playlist/$', FollowedPlaylists.as_view()),
    url(r'^api/add-to-playlist/$', AddToPlaylist.as_view()),
    url(r'^api/music-like/$', MusicLike.as_view()),
    url(r'^api/album-detail/$', AlbumDetail.as_view()),
    url(r'^api/genre-detail/$', GenreDetail.as_view()),
    url(r'^api/remove-playlist/$', DeletePlaylist.as_view()),

]

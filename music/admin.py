from django.contrib import admin
from .models import Music, Genre, Performer, Album, Playlist, Vote
# Register your models here.


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['name', 'release_date', 'links']
    filter_horizontal = ['artist', 'users_like']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre_name', ]


@admin.register(Performer)
class PerformerAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'release_date']
    filter_horizontal = ['musics',]


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo', 'created_date']
    filter_horizontal = ['musics', ]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'music', 'score']
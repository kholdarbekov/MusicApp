from django.contrib import admin
from .models import Music, Genre, Performer, Album
# Register your models here.


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['name', 'release_date', 'links']
    filter_horizontal = ['artist', ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre_name', ]


@admin.register(Performer)
class PerformerAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'release_date']

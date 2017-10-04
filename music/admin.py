from django.contrib import admin
from .models import Music, Genre
# Register your models here.


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['name', 'link']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre_name', ]

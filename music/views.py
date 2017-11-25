import json

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView
from .models import Music, Album, Playlist
from .forms import PlaylistForm

import os, tempfile, zipfile
from wsgiref.util import FileWrapper

client = settings.ES_CLIENT
CHUNK = 1024
# Create your views here.


def autocomplete_view(request):
    query = request.GET.get('term', '')
    resp = client.suggest(
        index='moozee',
        body={
            'name': {
                "text": query,
                "completion": {
                    "field": 'name',
                }
            }
        }
    )
    options = resp['name'][0]['options']
    data = json.dumps(
        [{'id': i['payload']['pk'], 'value': i['text']} for i in options]
    )
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def playListCreateView(request):
    if request.method == 'POST':
        playlist = PlaylistForm(request.POST, request.FILES)
        if playlist.is_valid():
            playlist = playlist.save(commit=False)
            playlist.creator = request.user
            playlist.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'ko'})


class AlbumView(DetailView):
    model = Album
    context_object_name = 'album'
    template_name = 'listen.html'

    def get_context_data(self, **kwargs):
        context = super(AlbumView, self).get_context_data(**kwargs)
        context['all_albums'] = Album.objects.exclude(pk=self.get_object().pk)
        return context


class AllAlbumsView(TemplateView):
    template_name = 'listen.html'

    def get_context_data(self, **kwargs):
        context = super(AllAlbumsView, self).get_context_data(**kwargs)
        context['albums'] = Album.objects.all()
        return context


class PlaylistView(DetailView):
    model = Playlist
    context_object_name = 'playlist'
    template_name = 'playlist.html'

    def get_queryset(self):
        qs = super(PlaylistView, self).get_queryset()
        return qs.filter(creator__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(PlaylistView, self).get_context_data(**kwargs)
        context['all_playlists'] = self.get_queryset().exclude(pk=self.get_object().pk)
        return context


def add_to_playlist(request, music_id, playlist_id):
    music = get_object_or_404(Music, pk=music_id)
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    contains = False
    for m in playlist.musics.all():
        if m == music:
            contains = True
            break
    if not contains:
        playlist.musics.add(music)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'ko', 'error': 'this song already in the playlist'})

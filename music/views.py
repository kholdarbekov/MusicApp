import json

from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q
from .models import Music, Album, Playlist, Performer
from .forms import PlaylistForm
from authentication.models import Profile
from charts.models import Chart

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


def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('q')
        if len(search_query) >= 2:
            music_results = Music.objects.filter(
                Q(name__icontains=search_query)
            )
            album_results = Album.objects.filter(
                Q(name__icontains=search_query)
            )
            playlist_results = Playlist.objects.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )
            user_results = Profile.objects.filter(
                Q(username__icontains=search_query)
            )
            chart_results = Chart.objects.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )
            performer_results = Performer.objects.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

            return render(request, 'search.html', {'music_results': music_results, 'album_results': album_results,
                                                   'playlist_results': playlist_results, 'query': search_query,
                                                   'user_results': user_results, 'chart_results': chart_results,
                                                   'performer_results': performer_results})
        else:
            return HttpResponse('Minimum length must be 2 characters')
    else:
        return redirect('/')

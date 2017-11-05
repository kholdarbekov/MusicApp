import json
import pyaudio
import wave

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView
from .models import Music, Album, Playlist
from .forms import PlaylistForm

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


def play(request):
    wf = wave.open('aromat.wav', 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()
    return HttpResponse('success')

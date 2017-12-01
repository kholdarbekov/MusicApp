import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q

from common.decorator import ajax_required
from .models import Music, Album, Playlist, Performer, Genre
from .forms import PlaylistForm
from authentication.models import Profile
from charts.models import Chart


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


@login_required
def playListCreateView(request):
    if request.method == 'POST':
        cp = request.POST.get('cp')
        playlist = PlaylistForm(request.POST, request.FILES)
        if playlist.is_valid():
            playlist = playlist.save(commit=False)
            playlist.creator = request.user
            playlist.save()

        if cp:
            try:
                return redirect(cp)
            except:
                return redirect('/')
        else:
            return redirect('/')
    else:
        return JsonResponse({'error': 'This view takes only POST requests'})


class AlbumView(LoginRequiredMixin, DetailView):
    model = Album
    context_object_name = 'album'
    template_name = 'album.html'

    def get_context_data(self, **kwargs):
        context = super(AlbumView, self).get_context_data(**kwargs)
        context['all_albums'] = Album.objects.exclude(pk=self.get_object().pk)
        return context


class AllAlbumsView(LoginRequiredMixin, TemplateView):
    template_name = 'album.html'

    def get_context_data(self, **kwargs):
        context = super(AllAlbumsView, self).get_context_data(**kwargs)
        last = Album.objects.last()
        context['all_albums'] = Album.objects.all().exclude(pk=last.pk)
        context['album'] = last
        return context


class PlaylistView(LoginRequiredMixin, DetailView):
    model = Playlist
    context_object_name = 'playlist'
    template_name = 'playlist.html'

    # def get_queryset(self):
    #     qs = super(PlaylistView, self).get_queryset()
    #     return qs.filter(creator__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(PlaylistView, self).get_context_data(**kwargs)
        context['all_playlists'] = Playlist.objects.filter(creator__in=[self.request.user]).exclude(pk=self.get_object().pk)
        return context


class GenreView(LoginRequiredMixin, DetailView):
    model = Genre
    context_object_name = 'genre'
    template_name = 'genres.html'
    slug_field = 'genre_name'

    def get_object(self, queryset=None):
        if self.kwargs[self.slug_field] == 'All':
            return Genre.objects.last()
        else:
            return Genre.objects.get(genre_name=self.kwargs[self.slug_field])

    def get_context_data(self, **kwargs):
        context = super(GenreView, self).get_context_data(**kwargs)
        if self.kwargs[self.slug_field] == 'All':
            context['musics'] = Music.objects.all()
        else:
            context['musics'] = self.get_object().all_music_in_genre.all()
        context['currnet_genre'] = self.kwargs[self.slug_field]
        return context


@ajax_required
@require_POST
@login_required
def add_to_playlist(request):
    music_id = request.POST.get('music_id')
    playlist_id = request.POST.get('playlist_id')
    if music_id and playlist_id:
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
    return JsonResponse({'status': 'ko', 'error': 'music id or playlist id is missing'})


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

            if not music_results.exists() and not album_results.exists() and not playlist_results.exists() and not user_results.exists() and not chart_results.exists() and not performer_results.exists():
                no_result = True
            else:
                no_result = False

            return render(request, 'search.html', {'music_results': music_results, 'album_results': album_results,
                                                   'playlist_results': playlist_results, 'query': search_query,
                                                   'user_results': user_results, 'chart_results': chart_results,
                                                   'performer_results': performer_results, 'no_result': no_result})
        else:
            return HttpResponse('Minimum length must be 2 characters')
    else:
        return redirect('/')


@ajax_required
@login_required
@require_POST
def music_like(request):
    music_id = request.POST.get('id')
    action = request.POST.get('action')
    if music_id and action:
        try:
            music = Music.objects.get(id=music_id)
            if action == 'like':
                music.users_like.add(request.user)
            else:
                music.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


class PerformerView(LoginRequiredMixin, DetailView):
    template_name = 'artist_profile.html'
    context_object_name = 'performer'
    model = Performer
    slug_field = 'pk'

    # def get_object(self, queryset=None):
    #     return Performer.objects.get(pk=self.kwargs[self.slug_field])

    # def get_context_data(self, **kwargs):
    #     context = super(ProfileView, self).get_context_data(**kwargs)
    #     # context['profile'] = Profile.objects.get(pk=self.request.user.pk)
    #     return context


@ajax_required
@require_POST
@login_required
def playlist_follow(request):
    playlist_pk = request.POST.get('playlist_pk')
    action = request.POST.get('action')
    if playlist_pk and action:
        try:
            playlist = Playlist.objects.get(pk=playlist_pk)

            if action == 'follow':
                playlist.followers.add(request.user)
            else:
                playlist.followers.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Playlist.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})
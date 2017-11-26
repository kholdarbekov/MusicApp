from django.http import Http404
from django.http import JsonResponse
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Playlist, Genre
from .serializers import PlaylistSerializers, GenreSerializer, MusicSerializer
from django.shortcuts import get_object_or_404
from ..models import Music
from .serializers import PlaylistSerializers


class PlayListCreate(APIView):
    http_method_names = ['post', ]
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request):
        serializer = PlaylistSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_music(request):
    if request.method == 'GET':
        music_id = request.GET.get('id', None)
        if music_id:
            music = get_object_or_404(Music, pk=music_id)
            return JsonResponse({'title':music.name, 'artist': music.artist.last().name, 'mp3': music.links})
    return JsonResponse({'error': 'wrong parameters are sent'})


class TopPlaylists(APIView):
    http_method_names = ['post', ]

    def post(self, request):
        playlists = sorted(Playlist.objects.all(), key=lambda playlist: playlist.get_net_value)
        serializer = PlaylistSerializers(playlists, many=True)
        return Response(serializer.data)


class TopGenres(APIView):
    http_method_names = ['post', ]

    def post(self, request):
        genres = Genre.objects.all()[:10]
        serializers = GenreSerializer(genres, many=True)
        return Response(serializers.data)


class PlaylistDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            raise Http404

    def post(self, request):
        pk = request.data.get('pk', None)
        if pk:
            playlist = self.get_object(pk)
            if playlist:
                musics = playlist.musics.all()
                serializer = MusicSerializer(musics, many=True)

                return Response(serializer.data)
            return Response({'error': 'such playlist does not exist!'})
        return Response({'error': 'you should send pk field'})


def get_music(request):
    if request.method == 'GET':
        music_id = request.GET.get('id', None)
        if music_id:
            music = get_object_or_404(Music, pk=music_id)
            return JsonResponse({'title':music.name, 'artist': music.artist.last().name, 'mp3': music.links})
    return JsonResponse({'error': 'wrong parameters are sent'})
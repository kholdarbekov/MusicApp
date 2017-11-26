from rest_framework import serializers
from ..models import Playlist, Genre, Music, Album, Performer


class PlaylistSerializers(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('name', 'description', 'photo', 'pk')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('genre_name', 'photo')


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('name', 'get_links', 'photo', 'file', 'pk')


class AlbumSerializer(serializers.ModelSerializer):
    artist = serializers.CharField(source='artist.name')

    class Meta:
        model = Album
        fields = ('name', 'artist', 'photo', 'pk')


class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performer
        fields = ('name', 'description', 'photo', 'pk')

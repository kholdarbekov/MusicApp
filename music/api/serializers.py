from rest_framework import serializers
from ..models import Playlist, Genre,Music


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
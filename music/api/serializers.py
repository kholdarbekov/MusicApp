from rest_framework import serializers
from ..models import Playlist, Genre


class PlaylistSerializers(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('name', 'description', 'photo')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('genre_name', 'photo')

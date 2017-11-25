from rest_framework import serializers
from ..models import Chart


class DailyChartSerializer(serializers.ModelSerializer):
    music_name = serializers.CharField(source='music.name')
    artist = serializers.CharField(source='music.get_singers')
    genre = serializers.CharField(source='music.genre')
    links = serializers.ListField(source='music.get_links')
    music_pk = serializers.IntegerField(source='music.pk')

    class Meta:
        model = Chart
        fields = ('music_name', 'position', 'num_of_views', 'best_position_ever', 'artist', 'genre', 'links', 'music_pk')
        read_only_fields = ('get_links_field', )
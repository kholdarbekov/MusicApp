from rest_framework import serializers
from ..models import Daily, Weekly, Monthly, Music


class DailyChartSerializer(serializers.ModelSerializer):
    music_name = serializers.CharField(source='music.name')
    link = serializers.URLField(source='music.link')
    artist = serializers.CharField(source='music.artist')
    genre = serializers.CharField(source='music.genre')
    additional_links = serializers.ListField(source='music.links')
    music_pk = serializers.IntegerField(source='music.pk')

    class Meta:
        model = Daily
        fields = ('music_name', 'position', 'num_of_views', 'best_position_ever', 'link', 'artist', 'genre',
                  'additional_links', 'music_pk')
        read_only_fields = ('links_field', )


class WeeklyChartSerializer(serializers.ModelSerializer):
    music_name = serializers.CharField(source='music.name')
    link = serializers.URLField(source='music.link')
    artist = serializers.CharField(source='music.artist')
    genre = serializers.CharField(source='music.genre')

    class Meta:
        model = Weekly
        fields = ('music_name', 'position', 'num_of_views', 'best_position_ever', 'num_of_days_in_this_position',
                  'link', 'artist', 'genre')


class MonthlyChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monthly
        fields = ('music', 'position', 'num_of_views', 'best_position_ever', 'num_of_days_in_this_position')
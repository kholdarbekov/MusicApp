from rest_framework import serializers
from ..models import Chart


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = ('name', 'description', 'photo', 'number_of_songs', 'pk')
from django.core.exceptions import ValidationError
from django.db import models

from authentication.models import Profile
from music.models import Music


# Create your models here.

class Chart(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='charts/', blank=True, null=True)
    number_of_songs = models.PositiveSmallIntegerField()
    musics = models.ManyToManyField('MusicInChart', related_name='charts')
    followers = models.ManyToManyField(Profile, related_name='followed_charts', blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    last_edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


CHART_MUSIC_STATUS = (
    ('-1', 'DOWN'),
    ('0', 'STABLE'),
    ('1', 'UP'),
)


class MusicInChart(models.Model):
    music = models.ForeignKey(Music, related_name='all_related_charts')
    number_of_plays = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=CHART_MUSIC_STATUS)
    last_week = models.PositiveSmallIntegerField()
    peak_position = models.PositiveSmallIntegerField()
    weeks_on_chart = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('number_of_plays', )

    def __str__(self):
        return self.music.name

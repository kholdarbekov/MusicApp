from django.db import models

# Create your models here.


class Genre(models.Model):
    genre_name = models.CharField(max_length=128)

    def __str__(self):
        return self.genre_name


class Music(models.Model):
    name = models.CharField(max_length=256)
    genre = models.ForeignKey(Genre, related_name='all_music_in_genre')
    link = models.URLField(help_text='main link to music')
    additional_links = models.CharField(max_length=4096, blank=True, null=True,
                                        help_text='Space (" ") separated links. '
                                                  'If one does not work the next will be attempted')
    artist = models.CharField(max_length=256)
    release_date = models.DateTimeField()

    def __str__(self):
        return '{} - {}'.format(self.artist, self.name)

    def links(self):
        if self.additional_links:
            return [i for i in self.additional_links.split(' ')]
        else:
            return None

    class Meta:
        unique_together = ('name', 'artist')


class Chart(models.Model):
    music = models.ForeignKey(Music, related_name='daily_chart')
    position = models.PositiveIntegerField()


class Daily(Chart):
    num_of_views = models.PositiveIntegerField(default=0)
    best_position_ever = models.PositiveIntegerField()

    class Meta:
        ordering = ('position', )


class Weekly(Chart):
    num_of_views = models.PositiveIntegerField(default=0)
    best_position_ever = models.PositiveIntegerField()
    num_of_days_in_this_position = models.PositiveIntegerField(default=0)
    starting_date_in_weekly_chart = models.DateTimeField()

    class Meta:
        ordering = ('position', )


class Monthly(Chart):
    num_of_views = models.PositiveIntegerField(default=0)
    best_position_ever = models.PositiveIntegerField()
    num_of_days_in_this_position = models.PositiveIntegerField(default=0)
    starting_date_in_monthly_chart = models.DateTimeField()

    class Meta:
        ordering = ('position',)
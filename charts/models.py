from django.db import models

from music.models import Music


# Create your models here.


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
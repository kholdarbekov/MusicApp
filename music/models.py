from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

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


@receiver(post_save, sender=Music)
def index_post(sender, instance, **kwargs):
    instance.indexing()
import django.db.models.options as options
from django.db import models
from django.core.exceptions import ValidationError
from . import signals

options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'es_index_name', 'es_type_name', 'es_mapping'
)
# Create your models here.


class Genre(models.Model):
    genre_name = models.CharField(max_length=128)

    def __str__(self):
        return self.genre_name


class Performer(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class Music(models.Model):
    name = models.CharField(max_length=256)
    genre = models.ForeignKey(Genre, related_name='all_music_in_genre')
    links = models.CharField(max_length=4096, blank=True, null=True,
                             help_text='Space (" ") separated links. '
                                       'If one does not work the next will be attempted')
    photo = models.ImageField(upload_to='music_photos/', blank=True, null=True)
    file = models.FileField(upload_to='music/', blank=True, null=True)
    artist = models.ManyToManyField(Performer, related_name='all_songs')
    release_date = models.DateField()

    def es_repr(self):
        data = {}
        mapping = self._meta.es_mapping
        data['_id'] = self.pk
        for field_name in mapping['properties'].keys():
            data[field_name] = self.field_es_repr(field_name)
        return data

    def field_es_repr(self, field_name):
        config = self._meta.es_mapping['properties'][field_name]
        if hasattr(self, 'get_es_%s' % field_name):
            field_es_value = getattr(self, 'get_es_%s' % field_name)()
        else:
            if config['type'] == 'object':
                related_object = getattr(self, field_name)
                field_es_value = {}
                field_es_value['_id'] = related_object.pk
                for prop in config['properties'].keys():
                    field_es_value[prop] = getattr(related_object, prop)
            else:
                field_es_value = getattr(self, field_name)
        return field_es_value

    def __str__(self):
        return '{} - {}'.format(self.artist, self.name)

    def get_links(self):
        if self.links:
            return [i for i in self.links.split(' ')]
        else:
            return None

    class Meta:
        es_index_name = 'moozee'
        es_type_name = 'music'
        es_mapping = {
            'properties': {
                'genre': {
                    'type': 'object',
                    'properties': {
                        'genre_name': {'type': 'string', 'index': 'not_analyzed'},
                    }
                },
                'name': {'type': 'string', 'index': 'not_analyzed'},
                'links': {'type': 'string', 'index': 'not_analyzed'},
                'artist': {'type': 'string', 'index': 'not_analyzed'},
                'release_date': {'type': 'date'},
            }
        }

    def save(self, *args, **kwargs):
        similar_musics = self.__class__.objects.filter(name=self.name)
        for music in similar_musics:
            artists = music.artist.all()
            diff = set(artists).difference(set(self.artist))
            if diff:
                raise ValidationError('This song seems to be already created!')

        is_new = self.pk
        super(Music, self).save(*args, **kwargs)
        # signals.music_saved.send(sender=self.__class__, is_new=is_new, instance=self)

    def delete(self, *args, **kwargs):
        prev_pk = self.pk
        super(Music, self).delete(*args, **kwargs)
        # signals.music_delete.send(sender=self.__class__, prev_pk=prev_pk, instance=self)


class Album(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='albums/', blank=True, null=True)
    artist = models.ForeignKey(Performer, related_name='albums')
    musics = models.ManyToManyField(Music, related_name='albums_of_music')
    number_of_views = models.PositiveIntegerField(default=0)
    release_date = models.DateField()

    def __str__(self):
        return '%s by %s' % (self.name, self.artist)

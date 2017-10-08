import django.db.models.options as options
from django.db import models
from . import signals

options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'es_index_name', 'es_type_name', 'es_mapping'
)
# Create your models here.


class Genre(models.Model):
    genre_name = models.CharField(max_length=128)

    def __str__(self):
        return self.genre_name


class Music(models.Model):
    name = models.CharField(max_length=256)
    genre = models.ForeignKey(Genre, related_name='all_music_in_genre')
    links = models.CharField(max_length=4096, blank=True, null=True,
                             help_text='Space (" ") separated links. '
                                       'If one does not work the next will be attempted')
    artist = models.CharField(max_length=256)
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
        unique_together = ('name', 'artist')
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
        is_new = self.pk
        super(Music, self).save(*args, **kwargs)
        # signals.music_saved.send(sender=self.__class__, is_new=is_new, instance=self)

    def delete(self, *args, **kwargs):
        prev_pk = self.pk
        super(Music, self).delete(*args, **kwargs)
        # signals.music_delete.send(sender=self.__class__, prev_pk=prev_pk, instance=self)

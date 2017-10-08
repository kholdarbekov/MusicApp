from django.conf import settings
from django.dispatch import Signal
from django.dispatch import receiver
from django.db.models.signals import post_save

es_client = settings.ES_CLIENT

music_saved = Signal(providing_args=["is_new", "instance"])

music_delete = Signal(providing_args=["prev_pk", "instance"])


def re_index_after_music_save(sender, is_new, instance, **kwargs):
    payload = instance.es_repr()
    if is_new is not None:
        del payload['_id']
        es_client.update(
            index=instance._meta.es_index_name,
            doc_type=instance._meta.es_type_name,
            id=instance.pk,
            refresh=settings.ES_AUTOREFRESH,
            body={
                'doc': payload
            }
        )
    else:
        es_client.create(
            index=instance._meta.es_index_name,
            doc_type=instance._meta.es_type_name,
            id=instance.pk,
            refresh=settings.ES_AUTOREFRESH,
            body={
                'doc': payload
            }
        )

music_saved.connect(re_index_after_music_save)


def re_index_after_music_delete(sender, prev_pk, instance, **kwargs):
    es_client.delete(
        index=instance._meta.es_index_name,
        doc_type=instance._meta.es_type_name,
        id=prev_pk,
        refresh=True,
    )

music_delete.connect(re_index_after_music_delete)


# @receiver(post_save, sender=Genre)
def re_index_after_genre_save(sender, instance, **kwargs):
    for music in instance.all_music_in_genre.all():
        data = music.field_es_repr('genre')
        es_client.update(
            index=music._meta.es_index_name,
            doc_type=music._meta.es_type_name,
            id=music.pk,
            body={
                'doc': {
                    'genre': data
                }
            }
        )
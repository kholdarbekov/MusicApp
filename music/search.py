from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

from charts import models

connections.create_connection(hosts=['localhost'])


class MusicIndex(DocType):
    name = Text()
    release_date = Date()
    artist = Text()

    class Meta:
        index = 'music-index'


def bulk_indexing():
    MusicIndex.init(index='music-index')
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.Music.objects.all().iterator()))


def search(author):
    s = Search().filter('term', name=author)
    response = s.execute()
    return response

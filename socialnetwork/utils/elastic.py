from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch("http://elasticsearch:9200")


def create_update_document(document: dict, index: str):
    if not es.indices.exists(index=index):
        es.indices.create(index=index)

    bulk(es, [document])


def delete_document(id: str, index: str):
    es.delete(index=index, id=id)

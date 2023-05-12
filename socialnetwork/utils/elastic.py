from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch("http://elasticsearch:9200")


def create_update_document(document: dict, index: str) -> None:
    if not es.indices.exists(index=index):
        es.indices.create(index=index)

    bulk(es, [document])


def delete_document(id: str, index: str) -> None:
    es.delete(index=index, id=id)


def search_documents(query: str, index: str) -> None:
    return es.search(index=index, body=query, source=False)

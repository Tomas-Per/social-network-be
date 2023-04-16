from community.models import Community
from socialnetwork.celery import app
from socialnetwork.utils.elastic import create_update_document, delete_document


@app.task(name="sync.community.to.elastic")
def sync_community_to_elastic(community_id):
    community = Community.objects.get(id=community_id)
    document = {
        "_index": "communities",
        "_id": community.id,
        "_source": {
            "name": community.name,
            "description": community.description,
        },
    }
    create_update_document(document, "communities")


@app.task(name="delete.community.from.elastic")
def delete_community_from_elastic(community_id):
    delete_document(community_id, "communities")

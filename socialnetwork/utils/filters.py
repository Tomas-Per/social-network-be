from django.db.models import QuerySet
from django_filters import rest_framework as filters

from community.models import Community
from post.models import Comment, Post
from socialnetwork.utils.elastic import search_documents


class CommunityFilter(filters.FilterSet):
    full_text_search = filters.CharFilter(method="full_text_search_filter", label="search")

    class Meta:
        model = Community
        fields = {
            "name": ["icontains"],
            "description": ["icontains"],
        }

    def full_text_search_filter(self, queryset: QuerySet, _, value: str) -> QuerySet:
        results = get_elastic_results("communities", ["name", "description"], value)
        return queryset.filter(id__in=results)


class PostFilter(filters.FilterSet):
    full_text_search = filters.CharFilter(method="full_text_search_filter", label="search")

    class Meta:
        model = Post
        fields = {
            "title": ["icontains"],
            "content": ["icontains"],
        }

    def full_text_search_filter(self, queryset: QuerySet, _, value: str) -> QuerySet:
        results = get_elastic_results("posts", ["title", "content"], value)
        return queryset.filter(id__in=results)


class CommentFilter(filters.FilterSet):
    full_text_search = filters.CharFilter(method="full_text_search_filter", label="search")

    class Meta:
        model = Comment
        fields = {
            "content": ["icontains"],
        }

    def full_text_search_filter(self, queryset: QuerySet, _, value: str) -> QuerySet:
        results = get_elastic_results("comments", ["content"], value)
        return queryset.filter(id__in=results)


def get_elastic_results(index: str, fields: list, value: str) -> list:
    query = {
        "query": {
            "multi_match": {
                "fields": fields,
                "query": value,
                "fuzziness": "AUTO",
            }
        }
    }
    results = search_documents(query, index)
    return [result["_id"] for result in results["hits"]["hits"]]

from rest_framework import serializers

from post.models import Comment, CommentVote, Post, PostVote
from socialnetwork.utils.mixins import BaseSerializerMixin


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(BaseSerializerMixin):
    replies = RecursiveField(many=True, read_only=True)
    vote_count = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "parent_comment",
            "content",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
            "replies",
            "vote_count",
            "author_username",
        ]

    def get_vote_count(self, obj):
        return obj.get_comment_votes()

    def get_author_username(self, obj):
        return obj.created_by.username


class PostSerializer(BaseSerializerMixin):
    comments = CommentSerializer(many=True, read_only=True)
    vote_count = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    # dont include comments where parent_comment is not null
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["comments"] = CommentSerializer(
            Comment.objects.prefetch_related("replies", "comment_votes").filter(
                post_id=data["id"], parent_comment__isnull=True
            ),
            many=True,
        ).data
        return data

    def get_vote_count(self, obj):
        return obj.get_post_votes()

    def get_author_username(self, obj):
        return obj.created_by.username

    def get_community_name(self, obj):
        return obj.community.name


class PostListSerializer(serializers.ModelSerializer):
    vote_count = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "community",
            "content",
            "created_at",
            "created_by",
            "vote_count",
            "author_username",
            "community_name",
        ]

    def get_vote_count(self, obj):
        return obj.get_post_votes()

    def get_author_username(self, obj):
        return obj.created_by.username

    def get_community_name(self, obj):
        return obj.community.name


class CommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentVote
        fields = "__all__"


class PostVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVote
        fields = "__all__"

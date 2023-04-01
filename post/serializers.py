from rest_framework import serializers

from post.models import Comment, CommentVote, Post, PostVote


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    replies = RecursiveField(many=True, read_only=True)
    vote_count = serializers.SerializerMethodField()

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
        ]

    def get_vote_count(self, obj):
        return (
            obj.comment_votes.filter(vote_type=1).count()
            - obj.comment_votes.filter(vote_type=-1).count()
        )


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    vote_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    # dont include comments where parent_comment is not null
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["comments"] = CommentSerializer(
            Comment.objects.filter(parent_comment__isnull=True), many=True
        ).data
        return data

    def get_vote_count(self, obj):
        return (
            obj.post_votes.filter(vote_type=1).count() - obj.post_votes.filter(vote_type=-1).count()
        )


class CommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentVote
        fields = "__all__"


class PostVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVote
        fields = "__all__"

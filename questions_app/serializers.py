from rest_framework import serializers
from questions_app.models import UserProfile, QuestionCategoryModel, QuestionModel, QuestionCommentModel, \
    QuestionCommentLikeModel


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'photo')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategoryModel
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    question_comments_count = serializers.SerializerMethodField('get_question_comments_count')

    class Meta:
        model = QuestionModel
        fields = [
            "id",
            "author",
            "image",
            "question",
            "question_comments_count",
            "created_time",
        ]
        extra_kwargs = {"image": {"required": False}}

    @staticmethod
    def get_question_comments_count(obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserProfileSerializer(read_only=True)
    replies = serializers.SerializerMethodField('get_replies')
    likes_count = serializers.SerializerMethodField('get_likes_count')
    me_liked = serializers.SerializerMethodField('get_me_liked')

    class Meta:
        model = QuestionCommentModel
        fields = ("id", "author", "likes_count", "comment", "parent", "created_time", "replies", "me_liked")

    def get_replies(self, obj):
        if obj.child.exists():
            serializers = self.__class__(obj.child.all(), many=True, context=self.context)
            return serializers.data
        else:
            return None

    def get_me_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(author=user).exists()
        else:
            return False

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()


class CommentLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserProfileSerializer(read_only=True)

    class Meta:
        model = QuestionCommentLikeModel
        fields = ("id", "author", "comment")


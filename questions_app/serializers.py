from rest_framework import serializers
from questions_app.models import UserModel, QuestionCategoryModel, QuestionModel, QuestionCommentModel, \
    QuestionCommentLikeModel
from users_app.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = UserModel
        fields = ('id', 'username')


class CategorySerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = QuestionCategoryModel
        fields = (
            "id",
            "name",
            "author"
        )


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    question_comments_count = serializers.SerializerMethodField('get_question_comments_count')

    class Meta:
        model = QuestionModel
        fields = [
            "id",
            "author",
            "image",
            "category",
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
    author = UserSerializer(read_only=True)
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
    author = UserSerializer(read_only=True)

    class Meta:
        model = QuestionCommentLikeModel
        fields = ("id", "author", "comment")


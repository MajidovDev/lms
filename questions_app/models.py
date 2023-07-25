from django.db import models
from shared_app.models import BaseModel
from users_app.models import UserModel
from django.core.validators import FileExtensionValidator, MaxLengthValidator


class QuestionCategoryModel(BaseModel):
    name = models.CharField(max_length=51)
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class QuestionModel(BaseModel):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="questions")
    category = models.ForeignKey(QuestionCategoryModel, on_delete=models.CASCADE,
                                 related_name="category")
    image = models.ImageField(null=True, blank=True, upload_to='post_images', validators=[
            FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])
        ])
    question = models.TextField(validators=[MaxLengthValidator(2000)])

    @classmethod
    def create_question_with_category(cls, author, category_name, image=None, question=None):
        category, created = QuestionCategoryModel.objects.get_or_create(name=category_name)
        print(category)
        return cls.objects.create(author=author, category=category["name"], image=image, question=question)

    class Meta:
        db_table = "question"
        verbose_name = "question"
        verbose_name_plural = "questions"

    def __str__(self):
        return f"{self.author}`s question about {self.question}"


class QuestionCommentModel(BaseModel):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    comment = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='child',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.author} commented"


class QuestionCommentLikeModel(BaseModel):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.ForeignKey(QuestionCommentModel, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'comment'],
                name="comment-like"
            )
        ]

    def __str__(self):
        return f"{self.author} liked -> {self.comment}"

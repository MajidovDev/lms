from django.db import models
from shared_app.models import BaseModel
from users_app.models import UserProfile
from django.core.validators import FileExtensionValidator, MaxLengthValidator


class QuestionModel(BaseModel):
  author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="questions")
  image = models.ImageField(null=True, blank=True, upload_to='post_images', validators=[
        FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])
    ])
  question = models.TextField(validators=[MaxLengthValidator(2000)])

  class Meta:
    db_table = "question"
    verbose_name = "question"
    verbose_name_plural = "questions"

  def __str__(self):
    return f"{self.author}`s question about {self.question}"


class QuestionCommentModel(BaseModel):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name="comments")
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
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
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

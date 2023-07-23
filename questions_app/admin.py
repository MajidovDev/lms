from django.contrib import admin
from questions_app.models import QuestionModel, QuestionCommentModel, QuestionCommentLikeModel

admin.site.register(QuestionModel)
admin.site.register(QuestionCommentModel)
admin.site.register(QuestionCommentLikeModel)
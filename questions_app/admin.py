from django.contrib import admin
from questions_app.models import QuestionModel, QuestionCommentModel, QuestionCommentLikeModel, QuestionCategoryModel

admin.site.register(QuestionModel)
admin.site.register(QuestionCategoryModel)
admin.site.register(QuestionCommentModel)
admin.site.register(QuestionCommentLikeModel)
from django.urls import path
from questions_app.views import CategoryListApiView, CategoryCreateApiView, CategoryRetrieveUpdateDestroyApiView, \
    QuestionsListApiView, QuestionCreateApiView, QuestionRetrieveUpdateDestroyApiView,\
    CommentListApiView, CommentCreateApiView, CommentLikesListView, \
    CommentLikesView, AllCommentsListApiView, AllCommentRetrieveUpdateDestroyApiView

urlpatterns = [
    path('category/list/', CategoryListApiView.as_view()),
    path('category/create/', CategoryCreateApiView.as_view()),
    path('category/<uuid:pk>/', CategoryRetrieveUpdateDestroyApiView.as_view()),
    path('list/', QuestionsListApiView.as_view()),
    path('create/', QuestionCreateApiView.as_view()),
    path('<uuid:pk>/', QuestionRetrieveUpdateDestroyApiView.as_view()),
    path('<uuid:pk>/comments/list/', CommentListApiView.as_view()),
    path('<uuid:pk>/comments/create/', CommentCreateApiView.as_view()),

    path('comments/list/', AllCommentsListApiView.as_view()),
    path('comments/<uuid:pk>/create-delete/', AllCommentRetrieveUpdateDestroyApiView.as_view()),
    path('comments/<uuid:pk>/likes/list/', CommentLikesListView.as_view()),
    path('comments/<uuid:pk>/likes/create-delete/', CommentLikesView.as_view()),

]
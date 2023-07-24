from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView

from questions_app.serializers import QuestionSerializer, CategorySerializer, UserProfileSerializer, CommentSerializer, CommentLikeSerializer
from questions_app.models import QuestionModel, QuestionCommentModel, QuestionCommentLikeModel, QuestionCategoryModel
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response


class CategoryListApiView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return QuestionCategoryModel.objects.all()


class CategoryCreateApiView(CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = QuestionCategoryModel.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def put(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.serializer_class(category, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "status": status.HTTP_200_OK,
            "message": "Category successfully UPDATED",
            "data": serializer.data
        })

    def delete(self, request, *args, **kwargs):
        return Response({
            "success": True,
            "status": status.HTTP_204_NO_CONTENT,
            "message": "Category successfully DELETED",
        })


class QuestionsListApiView(ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return QuestionModel.objects.all()


class QuestionCreateApiView(CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class QuestionRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = QuestionModel.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def put(self, request, *args, **kwargs):
        question = self.get_object()
        serializer = self.serializer_class(question, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "status": status.HTTP_200_OK,
            "message": "Question successfully UPDATED",
            "data": serializer.data
        })

    def delete(self, request, *args, **kwargs):
        return Response({
            "success": True,
            "status": status.HTTP_204_NO_CONTENT,
            "message": "Question successfully DELETED",
        })


class CommentListApiView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        question_id = self.kwargs['pk']
        queryset = QuestionCommentModel.objects.filter(question__id=question_id)
        return queryset


class CommentCreateView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        question_id = self.kwargs['pk']
        serializer.save(author=self.request.user, question_id=question_id)


class CommentRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = QuestionCommentModel.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def put(self, request, *args, **kwargs):
        Comment = self.get_object()
        serializer = self.serializer_class(Comment, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "status": status.HTTP_200_OK,
            "message": "Comment successfully UPDATED",
            "data": serializer.data
        })

    def delete(self, request, *args, **kwargs):
        return Response({
            "success": True,
            "status": status.HTTP_204_NO_CONTENT,
            "message": "Comment successfully DELETED",
        })


class CommentLikesListView(ListAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        comment_id = self.kwargs['pk']
        queryset = QuestionCommentLikeModel.objects.filter(comment__id=comment_id)
        return queryset


class CommentLikesView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        try:
            comment_like = QuestionCommentLikeModel.objects.create(
                author=self.request.user,
                comment_id=pk
            )
            serializer = CommentLikeSerializer(comment_like)
            data = {
                "success": True,
                "message": "Comment successfully liked",
                "data": serializer.data
            }
            return Response(data, status.HTTP_201_CREATED)
        except Exception as e:
            data = {
                "success": False,
                "message": f"{e}",
                "data": None
            }
            return Response(data, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            comment_like = QuestionCommentLikeModel.objects.get(
                author=self.request.user,
                comment_id=pk
            )
            comment_like.delete()
            data={
                "success": True,
                "message": "Comment Like successfully DELETED"
            }
            return Response(data, status.HTTP_204_NO_CONTENT)
        except Exception as e:
            data = {
                "success": True,
                "message": f"{e}"
            }
            return Response(data, status.HTTP_400_BAD_REQUEST)
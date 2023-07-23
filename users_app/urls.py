from django.urls import path
from users_app.views import UserCreateAPIView, VerifyAPIView, GetNewVerification, ChangeUserInfoView, ChangeUserPhotoView, LoginView, LoginRefreshView, LogOutView,ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('login/refresh/', LoginRefreshView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('signup/', UserCreateAPIView.as_view()),
    path('verify/', VerifyAPIView.as_view()),
    path('new-verify/', GetNewVerification.as_view()),
    path('change-user-info/', ChangeUserInfoView.as_view()),
    path('change-user-photo/', ChangeUserPhotoView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
]
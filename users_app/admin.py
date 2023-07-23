from django.contrib import admin
from users_app.models import UserModel, UserConfirmationModel, UserProfile


admin.site.register(UserModel)
admin.site.register(UserProfile)
admin.site.register(UserConfirmationModel)

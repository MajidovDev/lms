from django.contrib import admin
from users_app.models import UserModel, UserConfirmationModel


admin.site.register(UserModel)
admin.site.register(UserConfirmationModel)

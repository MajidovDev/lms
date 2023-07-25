import random
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

from shared_app.models import BaseModel
from datetime import datetime, timedelta
from django.core.validators import FileExtensionValidator

TEACHER, ASSISTANT, STUDENT, ADMINISTRATOR = ('tutor', 'assistant', 'student', 'admin')
NEW, CODE_VERIFIED, DONE, PHOTO_DONE = ('new', 'code_verified', 'done', 'photo_done')
VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')


class UserModel(AbstractUser, BaseModel):
    USER_ROLES = (
        (TEACHER, TEACHER),
        (ASSISTANT, ASSISTANT),
        (STUDENT, STUDENT),
        (ADMINISTRATOR,ADMINISTRATOR)
    )
    AUTH_TYPE_CHOICES = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )
    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
        (PHOTO_DONE, PHOTO_DONE)
    )
    user_roles = models.CharField(max_length=31, choices=USER_ROLES, default=STUDENT)
    auth_status = models.CharField(max_length=31, choices=AUTH_STATUS, default=NEW)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'heif'])])
    auth_type = models.CharField(max_length=31, choices=AUTH_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def create_verify_code(self, verify_type):
        code = "".join([str(random.randint(0, 100) % 10) for _ in range(4)])
        UserConfirmationModel.objects.create(
            user_id=self.id,
            verify_type=verify_type,
            code=code
        )
        return code

    def check_username(self):
        if not self.username:
            temp_username = f'lms-{uuid.uuid4().__str__().split("-")[-1]}'
            while UserModel.objects.filter(username=temp_username):
                temp_username = f"{temp_username}{random.randint(0, 9)}"
            self.username = temp_username

    def check_email(self):
        if self.email:
            normalize_email = self.email.lower()
            self.email = normalize_email

    def check_pass(self):
        if not self.password:
            temp_password = f"password-{uuid.uuid4().__str__().split('-')[-1]}"
            self.password = temp_password

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

    def save(self, *args, **kwargs):
        self.clean()
        super(UserModel, self).save(*args, **kwargs)

    def clean(self):
        self.check_email()
        self.check_username()
        self.check_pass()
        self.hashing_password()


class UserProfile(BaseModel):
    user = models.OneToOneField(to=UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"
        

PHONE_EXPIRE = 2


class UserConfirmationModel(BaseModel):
    TYPE_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
    )
    code = models.CharField(max_length=4)
    verify_type = models.CharField(max_length=31, choices=TYPE_CHOICES)
    user = models.ForeignKey('users_app.UserModel', models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())

    def save(self, *args, **kwargs):
        self.expiration_time = datetime.now() + timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmationModel, self).save(*args, **kwargs)

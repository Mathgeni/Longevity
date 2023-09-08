from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import validate_email

from api.managers.users import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, validators=[validate_email, ])
    joined = models.TimeField(default=timezone.now)
    otp = models.CharField(max_length=settings.OTP_LENGTH, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

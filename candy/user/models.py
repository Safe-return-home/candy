from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, kakaoId, userName, password=None, **extra_fields):
        user = self.model(
            kakaoId=kakaoId,
            userName=userName,
        )
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, kakaoId, userName, password=None, **extra_fields):
        superuser = self.create_user(
            kakaoId=kakaoId,
            userName=userName,
            password=password,
        )
        superuser.is_admin = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.is_staff = True
        superuser.save()
        return superuser


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    kakaoId = models.CharField(max_length=100, unique=True)
    userName = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'kakaoId'
    REQUIRED_FIELDS = ['userName']

    def __str__(self):
        return self.userName
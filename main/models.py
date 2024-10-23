from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password as auth_check_password

class UserManager(BaseUserManager):
    def create_user(self, login, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not login:
            raise ValueError('Users must have a login')

        user = self.model(
            login=login,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email, password=None):
        user = self.create_user(
            login=login,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    login = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    is_confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=128, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    passport = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'<User {self.id}>'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def set_password(self, password):
        self.password = make_password(password)
    
    def check_password(self, password):
        return auth_check_password(password, self.password)

    def get_reset_password_token(self, expires_in=600):
        token = jwt.encode(
            {'reset_password': self.pk, 'exp': datetime.utcnow() + timedelta(seconds=expires_in)},
            settings.SECRET_KEY, algorithm='HS256'
        )
        return token

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])['reset_password']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        return User.objects.get(pk=id)

    def generate_confirmation_token(self, expires_in=3600):
        token = jwt.encode(
            {'confirm_email': self.pk, 'exp': datetime.utcnow() + timedelta(seconds=expires_in)},
            settings.SECRET_KEY, algorithm='HS256'
        )
        return token

    @staticmethod
    def verify_confirmation_token(token):
        try:
            id = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])['confirm_email']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        return User.objects.get(pk=id)
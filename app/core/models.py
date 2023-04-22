"""
Database models
"""
from django.db import models
from django.contrib.auth.models import (
     AbstractBaseUser,
     BaseUserManager,
     PermissionsMixin,
)


class UserManager(BaseUserManager):
    """ Manager for Users """
    def create_user(self, email, password=None, **extra_field):
        """ Create, save & return a new user """
        user = self.model(email=email, **extra_field)
        user.set_password(password)  # this will also encrypt
        user.save(using=self._db)  # support for multiple DBs - in case only

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # Django assignment of UserManager

    USERNAME_FIELD = 'email'

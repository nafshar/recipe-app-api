"""
Database models
"""
from django.conf import settings
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
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)  # this will also encrypt
        user.save(using=self._db)  # support for multiple DBs - in case only

        return user

    def create_superuser(self, email, password):
        """ Create and return a new superuser """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # Django assignment of UserManager

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipe object """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')

    # String representation of the object is just its title
    def __str__(self):
        return self.title


class Tag(models.Model):
    """ Tag for filtering recipes """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Ingredient for recipe. """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

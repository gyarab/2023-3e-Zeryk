from django.db import models
from django.contrib.auth.models import AbstractUser, Permission

# Create your models here.
class AUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics', default='default.png')

    class Meta:
        permissions = {'verbose_name': 'user', 'verbose_name_plural': 'users'}
        abstract = False
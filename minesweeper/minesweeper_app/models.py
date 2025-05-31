from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class CustomUser(AbstractUser):
    number_of_titles = models.IntegerField(default=0)
    number_of_flags = models.IntegerField(default=0)


class Results(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    won = models.BooleanField(default=False)
    time = models.IntegerField(default=0)
    
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workspaces_number = models.IntegerField(default=1)
    files_number = models.IntegerField(default=3)

    def __str__(self):
        return f'{self.user.username} Profile'


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

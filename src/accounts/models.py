import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


def generate_img_path(instance, filename) -> str:
    extension = os.path.splitext(filename)[1]
    return f"users_pics/{instance.user.username}{extension}"


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True, null=False)

    def __str__(self) -> str:
        return self.username
    

class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)   #####
    title = models.CharField(max_length=250, blank=True)
    picture = models.ImageField(upload_to=generate_img_path, default="users_pics/default.png"
                                , max_length= 160)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.user.username






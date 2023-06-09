import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


def generate_img_path(instance, filename) -> str:
    extension = os.path.splitext(filename)[1]
    return f"users_pics/{instance.user.username}{extension}"


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True, null=False)


    first_name = None
    last_name = None

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
    
    def get_absolute_url(self) -> str:
        return reverse("accounts:profile", args=[self.user.id])

    def __str__(self) -> str:
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



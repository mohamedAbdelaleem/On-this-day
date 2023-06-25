from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

class Article(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=350)
    date = models.DateField(auto_now_add=True)
    contents = RichTextUploadingField()
    slug = models.SlugField(unique=True, blank=True, null=True)


    def get_absolute_url(self) -> str:
        return reverse("blog:display_article", args=[self.slug])

    def __str__(self) -> str:
        return self.slug


@receiver(post_save, sender=Article)
def create_slug(sender, instance: Article, **kwargs):
    new_slug = slugify(f"{instance.title}_{instance.id}")
    if instance.slug != new_slug:
        instance.slug = new_slug
        instance.save()


# class Report(models.Model):
#     pass


# class Reaction(models.Model):
#     pass


# class Comment(models.Model):
#     pass

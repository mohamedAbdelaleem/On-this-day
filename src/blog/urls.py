from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.list_articles, name='list_articles'),
    path('<slug:slug>', views.display_article, name='display_article'),
]

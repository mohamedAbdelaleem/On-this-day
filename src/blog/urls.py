from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.list_articles, name='list_articles'),
    path('add_article', views.add_article, name='add_article'),
    path('edit_article/<slug:slug>', views.edit_article, name='edit_article'),
    path('delete_article/<slug:slug>', views.delete_article, name='delete_article'),
    path('<slug:slug>', views.display_article, name='display_article'),
]

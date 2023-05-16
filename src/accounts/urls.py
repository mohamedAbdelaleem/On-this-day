from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:profile_id>/', views.display_profile_view, name='profile'),
    path('edit_profile/<int:profile_id>/', views.edit_profile, name='edit_profile'),
]

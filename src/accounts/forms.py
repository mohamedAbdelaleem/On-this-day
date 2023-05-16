from django import forms
from django.contrib.auth import forms as auth_forms
from .models import CustomUser, Profile


class RegisterForm(auth_forms.UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ("email", "username",)



class CustomUserChangeForm(auth_forms.UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email", "username",)


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ("user", )


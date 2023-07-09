from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from allauth.account import forms as allauth_forms
from .models import Profile, CustomUser
from .forms import ProfileForm
from utils.http_util import generate_redirect_destination


def register(request: HttpRequest) -> HttpResponse:

    redirect_to = generate_redirect_destination(request)
    response = redirect(redirect_to)

    if request.method == "POST":
        form = allauth_forms.SignupForm(data=request.POST)
        if form.is_valid():
            form.save(request)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=email, password=password)
            login(request, user)
        
        else:
            field_errors = list(form.errors.values())[0]
            for error in  field_errors:
                messages.error(request, error)
            
            response.set_cookie("redirected_from", "signup")        ####
                        

    return response
        

def login_view(request: HttpRequest) -> HttpResponse:

    redirect_to = generate_redirect_destination(request)
    response = redirect(redirect_to)

    if request.method == "POST":
        form = allauth_forms.LoginForm(request=request, data=request.POST)
        if form.is_valid():
            form.login(request)
            storage = messages.get_messages(request)
            storage.__iter__()                                      #####
        
        else:
            field_errors = list(form.errors.values())[0]
            for error in  field_errors:
                messages.error(request, error)
            
            response.set_cookie("redirected_from", "login")         #####
            
    return response


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        logout(request)
    
    redirect_to = generate_redirect_destination(request)

    return redirect(redirect_to)


def display_profile_view(request: HttpRequest, profile_id: int) -> HttpResponse:

    profile = get_object_or_404(Profile, user_id=profile_id)
    return render(request, "profile.html", {"profile": profile})


def can_user_edit_profile(user: CustomUser, profile_id: int) -> bool:
    if user.is_authenticated:
        return user.id == profile_id

    return False

def edit_profile(request: HttpRequest, profile_id: int) -> HttpResponse:
    
    if not can_user_edit_profile(request.user, profile_id):
        raise PermissionDenied()

    
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', profile.user_id)
    

    context = {
        "form":form,
        "profile": profile,
    }
    return render(request, "edit_profile.html", context)




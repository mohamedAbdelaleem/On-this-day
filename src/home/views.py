from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib import messages 
# Create your views here.


def home(request: HttpRequest) -> HttpResponse:



    
    redirected_from = request.COOKIES.get("redirected_from")
    context = {
        "redirected_from": redirected_from
    }
    response = render(request, 'index.html', context)
    if redirected_from:
        response.delete_cookie("redirected_from")

    return response

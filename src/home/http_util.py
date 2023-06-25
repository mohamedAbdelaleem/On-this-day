from typing import Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def handle_redirected_cookies(request: HttpRequest, context: Dict) -> None:

    redirected_from = request.COOKIES.get('redirected_from')
    if redirected_from:
        context['redirected_from'] = redirected_from


def delete_redirected_cookie(response: HttpResponse) -> None:
    response.delete_cookie('redirected_from')


def generate_response(request: HttpRequest, template_name: str, context: Dict) -> HttpResponse:
    """
    Generate the response After Handling the cookie redirected from 
    Authentication Views (register, login_view, logout_view) to support
    better user experience
    """
    handle_redirected_cookies(request, context)
    response = render(request, template_name, context)
    delete_redirected_cookie(response)

    return response


def generate_redirect_destination(request: HttpRequest, default: str='/') -> str:

    redirect_to = default
    referrer = request.META.get("HTTP_REFERER")
    if referrer:
        redirect_to = referrer
    
    return redirect_to




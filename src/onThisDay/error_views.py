from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect



def permission_denied_view(request: HttpRequest, exception) -> HttpResponse:

    return redirect("/")



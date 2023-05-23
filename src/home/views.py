from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib import messages 
from django.core.paginator import Paginator
from django.contrib.gis.geoip2 import GeoIP2
from .fetch_api import fetch_on_this_day_events, convert_on_this_day_data
from .timezones_util import get_user_timezone, convert_utc_to_timezone


# Create your views here.

events = fetch_on_this_day_events(datetime.today())
selected_events = convert_on_this_day_data(events['selected'])

def home(request: HttpRequest) -> HttpResponse:

    curr_date = datetime.utcnow()
    user_timezone = get_user_timezone(request)
    if user_timezone:
        curr_date = convert_utc_to_timezone(user_timezone)
    
    print(curr_date)

    paginator = Paginator(selected_events, 7)
    page_num = request.GET.get('page', 1)

    events_page = paginator.get_page(page_num)
    
    redirected_from = request.COOKIES.get("redirected_from")

    context = {
        "redirected_from": redirected_from,
        "events_page": events_page,
    }
    response = render(request, 'index.html', context)
    if redirected_from:
        response.delete_cookie("redirected_from")

    return response

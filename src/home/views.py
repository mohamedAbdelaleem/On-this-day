from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.core.cache import cache
from .fetch_api import fetch_on_this_day_events, convert_on_this_day_data
from utils.timezones_util import get_user_timezone, convert_utc_to_timezone
from utils.http_util import generate_response


def home(request: HttpRequest) -> HttpResponse:


    curr_date = datetime.utcnow()
    user_timezone = get_user_timezone(request)
    if user_timezone:
        curr_date = convert_utc_to_timezone(curr_date ,user_timezone)
    
    today = curr_date.strftime('%m/%d')
    events = cache.get(today)
    if not events:
        events = fetch_on_this_day_events(curr_date)
        cache.set(today, events, 27 * 60*60)

    selected_events = convert_on_this_day_data(events['selected'])


    paginator = Paginator(selected_events, 7)
    page_num = request.GET.get('page', 1)
    events_page = paginator.get_page(page_num)    

    context = {
        "events_page": events_page,
        "today": today,
    }
    
    response = generate_response(request, "index.html", context)
    return response

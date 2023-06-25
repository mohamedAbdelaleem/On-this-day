from datetime import datetime
from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpRequest
import timezonefinder
import pytz


def get_user_timezone(request: HttpRequest) -> str | None:

    ip_address = request.META.get('REMOTE_ADDR')
    if ip_address:
        geo_ip = GeoIP2()
        try:
            longitude, latitude = geo_ip.coords(ip_address)
        except:
            return None
        tz = timezonefinder.TimezoneFinder()
        user_timezone = tz.timezone_at(lng=longitude,lat=latitude)

        return user_timezone


def convert_utc_to_timezone(utc_date: datetime, timezone: str) -> datetime:

    timezone_obj = pytz.timezone(timezone)
    timezone_offset = utc_date.astimezone(timezone_obj).utcoffset()
    date = datetime.utcnow() + timezone_offset

    return date


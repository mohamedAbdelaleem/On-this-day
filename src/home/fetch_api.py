import datetime
import requests
from typing import Dict, List
import sys
import os

current_dir = os.path.abspath('.')
sys.path.append(current_dir + '\src')
from onThisDay import local_settings

def fetch_on_this_day_events(date: datetime.datetime) -> Dict:
    
    date = date.strftime('%m/%d')

    url = 'https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all/' + date

    headers = {
      'Authorization': local_settings.wiki_token,
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return data


def convert_on_this_day_data(events: List) -> List:
    """
    Convert the list of the events returned from wikimedia api to another simplified formate.

    Args:
        events (list): A list of dictionaries representing events from the Wikimedia API.

    Returns:
        new_events (list): A simplified list of events, where each event is represented as
                    a dict with the following keys('text', 'img_src', 'url')
    """

    new_events = []

    for event in events:
        s_event = {}
        s_event['text'] = event['text']
        s_event['img_src'] = None
        s_event['url'] = None
        event_page = event['pages'][0]

        if "originalimage" in event_page:
            s_event['img_src'] = event_page['originalimage']['source']
        
        if "content_urls" in event_page:
            s_event['url'] = event_page['content_urls']['desktop']['page']
        new_events.append(s_event)
    
    return new_events

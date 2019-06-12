from .utils import RequestHandler, HTTPException, send_newsletter
from .controllers import get_users, get_events_next_days
import json


class Newsletter(RequestHandler):

    def get(self):
        users = get_users();
        events = get_events_next_days()
       
        if len(events) > 0:
            event1 = events[0]

        event2 = None
        if len(events) > 1:
            event2 = events[1]

        send_newsletter(users, event1, event2)
        return {}

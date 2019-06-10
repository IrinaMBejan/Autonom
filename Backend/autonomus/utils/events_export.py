from ics import Calendar, Event 
from autonomus.controllers import get_user_events
import csv


def export_events_ical(events):
    calendar = Calendar()
    
    for event_key in events:
        event = event_key.get()

        e = Event()
        e.name = event.title
        e.begin = event.date
        e.description = event.description
        e.location = event.location

        calendar.events.add(e)   
  
    return str(calendar)



def export(urlsafe):
    events = get_user_events(urlsafe)

    return export_events_ical(events)

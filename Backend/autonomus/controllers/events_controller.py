from autonomus.models import Event


def get_all_events():
    events = Event.all()

    return events


def get_event(urlsafe):
    return Event.get(urlsafe)

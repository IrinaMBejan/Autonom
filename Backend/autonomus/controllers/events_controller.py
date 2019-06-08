from autonomus.models import Event


def get_all_events():
    events = Event.all()

    return events


def get_event(urlsafe):
    return Event.get(urlsafe)


def getEvent(title):
    query = Event.query()
    query.add_filter('title', '=', title)
    query_it = query.fetch()
    for ent in query_it:
        if ent is None:
            return None
        else :
            return ent

    return None
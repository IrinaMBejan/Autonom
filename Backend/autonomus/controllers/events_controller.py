from autonomus.models import Event
from .tags_controller import add_tag


def get_all_events(tags=None):
    events = Event.all()
    
    if tags is None:
        return events
    
    print(tags)
    events_returned = []
    for event in events:
        for tag in event.tags:
            if tag in tags:
                events_returned.append(event)
                break

    return events_returned


def get_event(urlsafe):
    return Event.get(urlsafe)


def update_event(urlsafe, field_name, modification):
    event = get_event(urlsafe)

    if field_name == 'title':
        event.title = modification
    elif field_name == 'image_link':
        event.image_link = modification
    elif field_name == 'description':
        event.description = modification
    elif field_name == 'location':
        event.location = modification
    elif field_name == 'new tag':
        tag = add_tag(modification)
        #dup
        event.tags.append(tag)

    event.put()


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

def get_events_next_days():
    date_now = datetime.datetime.now()
    limit = 2

    events_gather = []

    events = Event.all()
    for event in events:
        diff = date_now - event.date
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600

        if hours < 60:
            events_gather.append(event)
            limit = limit -1 
        
        if limit <= 0:
            return events_gather

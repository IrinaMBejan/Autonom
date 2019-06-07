from autonomus.models import Event
from .tags_controller import add_tag


def get_all_events():
    events = Event.all()

    return events


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

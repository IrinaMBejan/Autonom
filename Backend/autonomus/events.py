from .utils import RequestHandler, HTTPException, role_admitted
from .controllers import Roles
from .controllers import get_event, get_all_events

import json


class Events(RequestHandler):


    @role_admitted(Roles.USER, Roles.ADMIN)
    def get(self):
        events = get_all_events()
        event_data = []

        for event in events:
            event_dict = {}
            
            event_dict["id"] = event.urlsafe
            event_dict["title"] = event.title
            event_dict["image_link"] = event.image_link
            event_dict["description"] = event.description
            event_dict["location"] = event.location
            event_dict["date"] = event.date.strftime("%Y-%m-%d %H:%M")

            event_data.append(event_dict)

        json_data = json.dumps(event_data)
        return json_data


class EventInfo(RequestHandler):

    @role_admitted(Roles.USER, Roles.ADMIN)
    def get(self):  
        urlsafe = self.request.args["event_id"]
        event = get_event(urlsafe)
        
        event_dict = {}

        event_dict["id"] = event.urlsafe
        event_dict["title"] = event.title
        event_dict["image_link"] = event.image_link
        event_dict["description"] = event.description
        event_dict["location"] = event.location
        event_dict["date"] = event.date.strftime("%Y-%m-%d %H:%M")
            
        tag_names = []
            
        for tag in event.tags:
            tag_entity = tag.get()
            tag_names.append(tag_entity.name)

        event_dict["tags"] = tag_names

        return event_dict


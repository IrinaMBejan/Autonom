from .utils import RequestHandler, HTTPException, role_admitted, scanAllLinks
from .controllers import Roles, add_event_to_user, verify_token, remove_event_from_user
from .controllers import get_event, get_all_events, update_event, get_user_events
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

 
    @role_admitted(Roles.USER, Roles.ADMIN)
    def post(self):
        event_urlsafe = self.request.payload.get("event_id")
        field_name = self.request.payload.get("field_name")
        modification = self.request.payload.get("modification")

        if not event_urlsafe or field_name or modification:
            raise HTTPException("400", "Please specify all fields")


        update_event(event_urlsafe, field_name, modification)
 
        return {}


class EventInfo(RequestHandler):


    @role_admitted(Roles.USER, Roles.ADMIN)
    def get(self):  
        urlsafe = self.request.args["event_id"]
        
        if not urlsafe:
            raise HTTPException("400", "Please specify event id")

        event = get_event(urlsafe)
        
        event_dict = {}

        event_dict["id"] = event.urlsafe
        event_dict["title"] = event.title
        event_dict["image_link"] = event.image_link
        event_dict["description"] = event.description
        event_dict["location"] = event.location
        event_dict["date"] = event.date.strftime("%Y-%m-%d %H:%M")
        if event.price:
            event_dict["price"] = event.price
        else:
            event_dict["price"] = "-"
        
        
        if event.capacity:
            event_dict["capacity"] = event.capacity
        else:
            event_dict["capacity"] = "-"

        tag_names = []
            
        for tag in event.tags:
            tag_entity = tag.get()
            tag_names.append(tag_entity.name)

        event_dict["tags"] = tag_names

        return event_dict


class MyEvents(RequestHandler):

    
    @role_admitted(Roles.USER, Roles.ADMIN)
    def get(self):
        event_data = []
        
        token = self.request.headers['HTTP_AUTHORIZATION']
        user_urlsafe = verify_token(token)
        events = get_user_events(user_urlsafe)

        for event_key in events:

            event = event_key.get()
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


    @role_admitted(Roles.USER, Roles.ADMIN)
    def put(self):
        event_urlsafe = self.request.payload.get('event_id')
  
        if not event_urlsafe:
            raise HTTPException("400", "Please specify event id")
        event = get_event(event_urlsafe)
        
        token = self.request.headers['HTTP_AUTHORIZATION']
        user_urlsafe = verify_token(token)

        add_event_to_user(user_urlsafe, event.key)
        return {'status':'200', 'message':'Event heart succesfully added'}


    @role_admitted(Roles.USER, Roles.ADMIN)
    def delete(self):
        event_urlsafe = self.request.payload.get('event_id')
  
        if not event_urlsafe:
            raise HTTPException("400", "Please specify event id")
        event = get_event(event_urlsafe)
        
        token = self.request.headers['HTTP_AUTHORIZATION']
        user_urlsafe = verify_token(token)

        remove_event_from_user(user_urlsafe, event.key)
        return {'status':'200', 'message':'Event heart succesfully removed'}


class EventsCrawl(RequestHandler):

    def get(self):
        scanAllLinks() 
        return {}

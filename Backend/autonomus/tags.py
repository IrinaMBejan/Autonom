from .utils import RequestHandler, HTTPException, role_admitted
from .controllers import Roles
from .controllers import get_tag, get_all_tags, verify_token
from .controllers import remove_tag_from_user, add_tag_to_user
from .models import User

import json


class Tags(RequestHandler):


    @role_admitted(Roles.USER, Roles.ADMIN)
    def get(self):
        tags = get_all_tags()
        tags_data = []

        token = self.request.headers['HTTP_AUTHORIZATION']
        user_urlsafe = verify_token(token)
        user = User.get(user_urlsafe)

        for tag in tags:
            tag_dict = {}

            tag_dict["id"] = tag.urlsafe
            tag_dict["name"] = tag.name
    
            if tag.key in user.tags: 
                tag_dict["selected"] = "true"
            else:
                tag_dict["selected"] = "false"

            tags_data.append(tag_dict)

        json_data = json.dumps(tags_data)
        return json_data

    
    @role_admitted(Roles.USER, Roles.ADMIN)
    def put(self):
        tag_urlsafe = self.request.payload.get('tag_id')
  
        if not tag_urlsafe:
            raise HTTPException("400", "Please specify tag_id")
        tag = get_tag(tag_urlsafe)
        
        token = self.request.headers['HTTP_AUTHORIZATION']
        user_urlsafe = verify_token(token)

        add_tag_to_user(user_urlsafe, tag.key)
        return {'status':'200', 'message':'Tag succesfully added'}


    @role_admitted(Roles.USER, Roles.ADMIN)
    def delete(self):
        tag_urlsafe = self.request.payload.get('tag_id')
  
        if not tag_urlsafe:
            raise HTTPException("400", "Please specify tag_id")
        tag = get_tag(tag_urlsafe)
        
        token = self.request.headers['HTTP_AUTHORIZATION']
        user_urlsafe = verify_token(token)

        remove_tag_from_user(user_urlsafe, tag.key)
        return {'status':'200', 'message':'Tag succesfully removed`'}



 
 

from .utils import RequestHandler, HTTPException, role_admitted
from .controllers import *
from autonomus.models import Link,Token
from autonomus.controllers import links_controller as ctrl
import json
from autonomus.controllers import users_controller

class Links(RequestHandler):

    @role_admitted(Roles.ADMIN)
    def post(self):
        nouLink = self.request.payload.get("Link")

        if not nouLink:
            raise HTTPException("400", "Please specify the link")

        ExistLink=ctrl.exists_link(nouLink)

        if ExistLink != None:
            raise HTTPException("409", "This link already exist ")
        else:
            if  'meetup.com/' not in nouLink and   'eventbrite.com' not in nouLink  and 'facebook.com' not in nouLink:
                raise HTTPException("400", "We can't get events from this link")

            if ctrl.check_link(nouLink)== False:
                raise HTTPException("400", "This link is invalid ")

            else:
                dbLink=Link()
                dbLink.follow_link=nouLink
                dbLink.put()
                return {
                    'status': '201',
                    'message': 'Link succesfully added'
                }


    @role_admitted(Roles.ADMIN)
    def delete(self):
        deleteLink = self.request.payload.get("Link")

        if not deleteLink:
            raise HTTPException("400", "Please specify the link")

        exist =ctrl.exists_link(deleteLink)

        if exist == None:
            raise HTTPException("400", "This link doesn't exist ")
        else:
            exist.remove()
            return {
                'status': '200',
                'message': 'Link removed'
            }

    @role_admitted(Roles.ADMIN)
    def get(self):

        linkuri = Link.all()
        if len(linkuri) == 0:
            raise HTTPException("204", "No links")
        else:
            last = []
            for l in linkuri:
                last.append(l.follow_link)

            return {
                'status': '200',
                'links':last
            }


class LinksCleaner(RequestHandler):

    def get(self):
        for one in Token.all():
           if not users_controller.is_token_expired(one.token):
               one.remove()


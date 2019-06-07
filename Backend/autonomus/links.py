from .utils import RequestHandler, HTTPException, role_admitted
from .controllers import Roles
from .controllers import *
from autonomus.models import link
import requests
import json

def exists_link(data_link):
    """Verify if a link exists in the datastore"""
    query = link.Link.query()
    query.add_filter('follow_link', '=', data_link)
    query_it = query.fetch()
    for ent in query_it:
        if ent is None:
            return None
        else :
            return ent

    return None

def check_link(data_link):
    request = requests.get(data_link)
    if request.status_code == 200:
        return True
    else:
        return False

class Links(RequestHandler):

    @role_admitted(Roles.ADMIN)
    def post(self):
        nouLink = self.request.payload.get("Link")

        if not nouLink:
            raise HTTPException("400", "Please specify the link")

        ExistLink=exists_link(nouLink)

        if ExistLink != None:
            raise HTTPException("409", "This link already exist ")
        else:
            if check_link(nouLink)== False:
                raise HTTPException("400", "This link is invalid ")
            else:
                dbLink=link.Link()
                dbLink.follow_link=nouLink;
                dbLink.put()
                return {
                    'status': '200',
                    'message': 'Link succesfully added'
                }


    @role_admitted(Roles.ADMIN)
    def delete(self):
        deleteLink = self.request.payload.get("Link")

        if not deleteLink:
            raise HTTPException("400", "Please specify the link")

        exist = exists_link(deleteLink)

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
        linkuri = list( link.Link.all())
        if len(linkuri)== 0:
            raise HTTPException("204", "No links")
        else:
            return {
                'status': '200',
                'links': json.dumps(linkuri)
            }



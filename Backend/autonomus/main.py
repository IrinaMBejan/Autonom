from .utils import API, RequestHandler, HTTPException, role_admitted
from .auth import Login, Register, Logout
from .events import Events, EventInfo, MyEvents, EventsCrawl
from .controllers import Roles
from .links import Links
from .api_requests import Api_Requests
from .tags import Tags

class Base(RequestHandler):

    @role_admitted(Roles.NEWBIE)
    def get(self):
        return { 
            "message": "Nothing to do here, check out the docs!" 
        }


class AutonomusAPI(API):
    headers = [
            ("Access-Control-Allow-Origin", "*"),
            ("Access-Control-Allow-Credentials", "true")
        ]
    
    routes = [
        ("/", Base()),
        ("/login", Login()),
        ("/register", Register()),
        ('/logout', Logout()),
        ('/events', Events()),
        ('/events/details', EventInfo()),
        ('/events/crawl', EventsCrawl()),
        ('/links', Links()),
        ('/requests',Api_Requests()),
        ('/tags', Tags()),
        ('/myevents',MyEvents())
    ]

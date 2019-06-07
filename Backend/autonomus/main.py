from .utils import API, RequestHandler, HTTPException, role_admitted
from .auth import Login, Register, Logout
from .events import Events, EventInfo
from .controllers import Roles
from .links import Links


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
        ('/links', Links())
    ]

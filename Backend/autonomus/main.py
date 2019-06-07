from .utils import API, RequestHandler, HTTPException, role_admitted
from .auth import Login, Register, Logout
from .controllers import Roles

class Base(RequestHandler):

    @role_admitted(Roles.NEWBIE)
    def get(self):
        return { 
            "message": "Nothing to do here, check out the docs!" 
        }


class AutonomusAPI(API):
    routes = [
        ("/", Base()),
        ("/login",Login()),
        ("/register",Register()),
        ('/logout', Logout())
    ]

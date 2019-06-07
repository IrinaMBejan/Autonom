from .utils import API, RequestHandler


class Base(RequestHandler):

    def get(self):
        return { 
            "message": "Bad luck, try something else!" 
        }


class Login(RequestHandler):
    
    def put(self):
        return {
        }


class Register(RequestHandler):


    def put(self):
        return {
        }

class AutonomusAPI(API):
    routes = [
        ("/", Base()),
        ("/login",Login()),
        ("/register",Register())
    ]

from .utils import API, RequestHandler


class Base(RequestHandler):

    def get(self):
        return { 
            "message": "Bad luck, try something else!" 
        }


class AutonomusAPI(API):
    routes = [
        ("/", Base())
    ]

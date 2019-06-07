import json
import re


from .http_exception import HTTPException
from .request import Request
from .response import Response


class API:
    """
    This is a WSGI object required for the server run and is used as a base
    class for any restful api.
    """
    
    routes = []
    headers = None

  
    def __init__(self, environ, start_response):
        
        path = self.__remove_last_slash(environ["PATH_INFO"])

        self.request = Request(
            path=path,
            method=environ["REQUEST_METHOD"],
            environ=environ
        )

        self.response = Response(
            status_code = 200
        )

        self.environ = environ
        self.start = start_response
       
           
    def __remove_last_slash(self, path):
        """Removes the last slash if it exists"""
        if len(path) > 1 and path.endswith("/"):
            path = path[0:-1]

        return path


    def __iter__(self):
        headers = [("Content-Type", "application/json")]
        if self.headers:
            headers += self.headers
            
        try:
            resp = self.run_match()
            self.start(str(self.response.status_code), headers)
        except HTTPException as exception:
            self.response.status_code = exception.status_code
            self.start(str(self.response.status_code), headers)
            resp = exception.response()
        except Exception as err:
            print(err)
            
            self.start("500", headers)
            resp = { "error": "Internal server error :(." }
        return self.__to_iterable_json(resp)


    def __to_iterable_json(self, resp):
        """Converts existing response to an iterable object"""
        
        if isinstance(resp, (dict, list)):
            try:
                json_resp = json.dumps(resp)
            except Exception as err:
                msg = "Something crashed, we don't know what >.<."
                json_resp = json.dumps({ "error": msg })
            return iter([json_resp.encode('utf-8')])
        elif isinstance(resp, str):
            return iter([resp.encode('utf-8')])
        return iter(resp)


    def run_match(self):
        """Searches for a handler to match and returns the response"""
        
        path = self.request.path
        method = self.request.method
                
        for pattern, handler in self.routes:
            # Default request & response
            handler.request = self.request
            handler.response = self.response

            # Looks for a match with the given path
            print('^'+pattern+'$')
            print(path)

            result = re.match('^' + pattern + '$', path)
            print(result)
            if result:
                # Retrieves all params matched
                params = result.groups()

                # Checks whether our handler defined the given method
                # ex (get/put..)
                function_name = method.lower()
                try:
                    function = getattr(handler, function_name)
                except AttributeError:
                    raise HTTPException(
                            "405", "Method %s not allowed"%(method.upper()))

                return function(*params)
                               
        raise HTTPException("404","Path %s is nowhere to be found. "%(path))


class RequestHandler(object):
    """
    Base class for any request handler

    It may define a get, put, post, delete function to handle the coresspondent
    methods.
    """

    request = None
    response = None 

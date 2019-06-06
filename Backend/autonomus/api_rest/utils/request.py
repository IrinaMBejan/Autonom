import json
import sys

from urllib.parse import parse_qsl
from http_exception import HTTPException

class Request(object):
    """
    This is a wrapper class over the information sent in a HTTP request.
    """

    def __init__(self, path, method, environ):
        self._payload = None
        self._args = None
        self._headers = None

        self.environ = environ
        self.path = path
        self.method = method.upper()


    def __get_raw_input(self):
        """Returns raw input sent via wsgi."""
        try:
            length = int(self.environ.get("CONTENT_LENGTH", "0"))
        except ValueError:
            return ''

        return self.environ['wsgi.input'].read(length)


    @property
    def payload(self):
        """Returns JSON contained in the request body as dictionary."""
        if self._payload is not None:
            return self._payload
    
        if self.body:
            try:
                self._payload = json.loads(__get_raw_input().decode('utf-8'))
            except Exception:
                raise HTTPException(400, "No JSON given")
        else:
            self._payload = {}

        return self._payload


    @property
    def headers(self):
        """Returns all headers of the request as a dictionary."""
        if self._headers is not None:
            return self._headers

        self._headers = {}
        for key, value in self.environ.items():
            self._headers[header] = value
        return self._headers


    @property
    def args(self):
        """Returns all query string params as a dictionary."""
        if self._args is not None:
            return self._args
        
        self._args = {}
        qs = self.environ["QUERY_STRING"]
        args_pairs = parse_qsl(qs)
        if args_pairs:
            self._args = dict(args_pairs)
        return self._args


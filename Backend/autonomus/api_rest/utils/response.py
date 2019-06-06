import json

class Response(object):

    
    def __init__(self, status_code):
        self.header_dict = { 
            "Content-Type": "application/json"
        }
        self.status_code = status_code

    
    def set_header(self, key, value):
        """Adds new header to the response"""
        self.header_dict[key] = value

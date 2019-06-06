class HTTPException(Exception):

    def __init__(self, status_code, error_message, payload=None, headers=[]):
        self.status_code = status_code
        self.error_message = error_message
        self.payload = payload
        self.headers = headers


    def response(self):
        return {
            "status_code" : status_code,
            "error": self.error_message,
            "payload": self.payload
        }

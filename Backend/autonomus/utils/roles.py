from .request import Request
from .http_exception import HTTPException
from autonomus.controllers import Roles, verify_token, get_user_role

from functools import wraps

def get_request_role(request):
    headers = request.headers
    if "HTTP_AUTHORIZATION" in headers:
        token = headers["HTTP_AUTHORIZATION"]
        if token is None:
            return Roles.NEWBIE

        user_urlsafe = verify_token(token)
        if user_urlsafe is None:
            return Roles.NEWBIE

        return get_user_role(user_urlsafe)

    return Roles.NEWBIE 


def role_admitted(*roles):
    def authorization(f):
        @wraps(f)
        def authorize(*args, **kwargs):
            if get_request_role(args[0].request) not in roles:
                raise HTTPException(
                        "401", 
                        "You don't have enough rights to do this operation")
            return f(*args, **kwargs)
        return authorize
    return authorization



from .utils import RequestHandler, HTTPException, role_admitted
from .controllers import Roles
from .controllers import *


class Login(RequestHandler):
   

    @role_admitted(Roles.NEWBIE)
    def post(self):
        email = self.request.payload.get("email")
        password = self.request.payload.get("password")
        
        if not email or not password:
            raise HTTPException("400", "Please specify email and password")

        print(email)
        print(password)
        user = exists_user(email.lower(), password)
        if user != None:
            jwt_token = generate_token(user)
            update_token(jwt_token, user)
            return {
                'status': '200',
                'message': 'Succesfully logged in',
                'token': jwt_token.decode("utf-8"),
                'type': user.type
                }
        else:
            raise HTTPException("401", "Invalid email or pass")
    
        return {}


class Register(RequestHandler):

    @role_admitted(Roles.NEWBIE)
    def post(self):
        print(self.request.payload)
        password = self.request.payload.get("password")
        email = self.request.payload.get("email")
        username = self.request.payload.get("username")
        confirmation_password = self.request.payload.get("confirmation_password")
        phone_number = self.request.payload.get("phone_number")
        
        if not username or not password or not email or not confirmation_password:
            raise HTTPException("400", "Please specify all required fields")
 
        if len(username) < 3:
            raise HTTPException(
                    "401", 
                    "The username should be at least three letters long."
                    )
        elif len(password) < 6:
            raise HTTPException(
                    "401", 
                    "The password should be longer than 6 chars."
                    )
        elif password != confirmation_password:
            raise HTTPException(
                    "401", 
                    "The password and the confirmation password don't match."
                    )
        else:
            if exists_user(email, password) == None:
                add_user(username, password, email, phone_number)
                return {'status': "200", 'message': "Succesfully registered user"}
            else:
                raise HTTPException(
                        "409",
                        "The email is already in our database."
                        )


class Logout(RequestHandler):
    """Clears user session data (token)"""    

    @role_admitted(Roles.USER, Roles.ADMIN)
    def post(self):
        token = self.request.headers["HTTP_AUTHORIZATION"]
        user_urlsafe = verify_token(token)
        remove_token(user_urlsafe)

        return {
            "status":"200",
            "message":"Logged out succesfully!" 
            }



from .utils import RequestHandler, HTTPException, role_admitted
from .controllers import Roles,users_controller,events_controller,requests_controller
from .models import RequestDB,User,Event
import json

class Api_Requests (RequestHandler):

    @role_admitted(Roles.ADMIN)
    def get(self):
        req = list(RequestDB.all())
        if len(req) == 0:
            raise HTTPException("204", "No requests")
        else:
            last = []
            for r in req:
                if r.state=="pending":
                    cerere = {}
                    cerere['id']=r.urlsafe
                    utilizator= User.get( r.user )
                    eveniment = Event.get(r.event)
                    cerere['event']=eveniment.urlsafe
                    cerere['user']= utilizator.username
                    cerere['field']=r.field
                    cerere['modification']=r.modification


                    last.append(cerere)


            return json.dumps(last)



    @role_admitted(Roles.ADMIN,Roles.USER)
    def post(self):
        user = self.request.payload.get("user")
        event = self.request.payload.get("event")
        field = self.request.payload.get("field")
        modification = self.request.payload.get("modification")

        if not user:
            raise HTTPException("400", "Please specify the user")
        if not event:
            raise HTTPException("400", "Please specify the event")
        if not field:
            raise HTTPException("400", "Please specify the field")
        if not modification:
            raise HTTPException("400", "Please specify the modification")

        user_urlsafe =users_controller.verify_token(user)
        utilizator = User.get(user_urlsafe)
        if utilizator ==  None:
            raise HTTPException("400", "Wrong user")

        eveniment= Event.get(event)
        if eveniment ==None:
            raise HTTPException("400", "Wrong eveniment")

        if field not in ['title','image_link' ,'description', 'location' ,'date','price','capacity','tags']:
            raise HTTPException("400", "Wrong field")

        newRequest = RequestDB()
        newRequest.user= utilizator.key
        newRequest.event=eveniment.key
        newRequest.field=field
        newRequest.modification=modification
        newRequest.state='pending'
        newRequest.put()

        return {
            'status': '201',
            'message': 'Request succesfully added'
        }

    @role_admitted(Roles.ADMIN)
    def put(self):
        id = self.request.payload.get("id")
        newState = self.request.payload.get("state")

        if not id :
            raise HTTPException("400", "Please specify the id")

        if not newState:
            raise HTTPException("400", "Please specify the state")

        if newState not in ['Accepted','Denied']:
            raise HTTPException("400", "Please specify the state('Accepted','Denied')")

        req = RequestDB.get(id)
        if req == None:
            raise HTTPException("400", "This id doesn't exist")

        requests_controller.solveRequest(id,newState)

        return {
            'status': '200',
            'message': 'Job Done'
        }


from google.cloud import datastore
from autonomus.controllers import tags_controller
from autonomus.models import RequestDB,User,Event
import os
import json
from autonomus.controllers import  events_controller, users_controller, requests_controller

def get():
        req = list(RequestDB.all())
        if len(req) == 0:
            return {'status':'204','message': "No requests"}
        else:
            last = []
            for r in req:
                cerere = {}
                cerere['id']=r.urlsafe
                utilizator= User.get(  r.user )
                eveniment = Event.get(r.event)
                cerere['event']=eveniment.title
                cerere['user']= utilizator.username
                cerere['field']=r.field
                cerere['modification']=r.modification
                cerere['state']=r.state

                last.append(cerere)


            return {
                'status': '200',
                'links':json.dumps(last)
            }

def post(user,event,field,modification):


        if not user:
            return ("400", "Please specify the user")
        if not event:
            return ("400", "Please specify the event")
        if not field:
            return ("400", "Please specify the field")
        if not modification:
            return ("400", "Please specify the modification")

        utilizator = users_controller.get_user(user)
        if utilizator ==  None:
            return ("400", "Wrong user")

        eveniment= events_controller.getEvent(event)
        if eveniment ==None:
            return ("400", "Wrong eveniment")

        if field not in ['title','image_link' ,'description', 'location' ,'date','price','capacity','tags']:
            return ("400", "Wrong field")

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

def put(id,newState):

        if not id :
            return ("400", "Please specify the id")

        if not newState:
            return ("400", "Please specify the state")

        if newState not in ['Accepted','Denied']:
            return ("400", "Please specify the state('Accepted','Denied')")

        req = RequestDB.get(id)
        if req == None:
            return ("400", "This id doesn't exist")

        requests_controller.solveRequest(id,newState)

        return {
            'status': '200',
            'message': 'Job Done'
        }

def main():


    global client
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/andrei/autonomus.json"
    client = datastore.Client(project="autonomus", namespace="development")

    # print(post('Irina Bejan','Cenușăreasa','capacity','12'))
    print(get())
    print(put('aglhdXRvbm9tdXNyFgsSCVJlcXVlc3REQhiAgID4kKedCgyiAQtkZXZlbG9wbWVudA','Accepted') )
    print(get())



main()
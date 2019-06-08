from autonomus.models import User,Event,RequestDB
from autonomus.controllers import tags_controller

def solveRequest(id , newState):
    req = RequestDB.get(id)
    if req != None and newState in ['Accepted','Denied']:
        if req.state == 'pending':
            req.state= newState
            req.put()
            if newState == 'Accepted':
                editEvent= Event.get(req.event)
                if req.field == 'title':
                    editEvent.title=req.modification
                elif req.field == 'image_link':
                    editEvent.image_link=req.modification
                elif req.field == 'description':
                    editEvent.description=req.modification
                elif req.field == 'location':
                    editEvent.location=req.modification
                # elif req.field == 'date':
                #     editEvent.image_link=req.modification
                elif req.field == 'price':
                    editEvent.price= float(req.modification)
                elif req.field == 'capacity':
                    editEvent.capacity= int(req.modification)
                elif req.field == 'tags':
                    editEvent.price= tags_controller.get_Tags(req.modification)

                editEvent.put()

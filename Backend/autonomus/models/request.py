from autonomus.models.base import BaseModel, ndb
from . import User


class Request(BaseModel):

    """Tags added manually or extracted with events."""
    user = ndb.KeyProperty(kind=User)
    field = ndb.StringProperty(required=True)
    modification = ndb.StringProperty(required=True)
    state = ndb.StringProperty(required=True)

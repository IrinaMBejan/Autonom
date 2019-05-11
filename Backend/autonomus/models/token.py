from autonomus.models.base import BaseModel, ndb

from . import User

class Token(BaseModel):

    """The token of a logged in user."""

    token = ndb.StringProperty()
    user = ndb.KeyProperty(kind=User,required=True)

from autonomus.models.base import BaseModel, ndb

from . import Event, Tag

class User(BaseModel):

    """The user account metadata."""

    username = ndb.StringProperty()
    password = ndb.StringProperty()
    email = ndb.StringProperty()
    type = ndb.StringProperty()
    tags = ndb.KeyProperty(kind=Tag, repeated=True)
    events = ndb.KeyProperty(kind=Event, repeated=True)

from autonomus.models.base import BaseModel, ndb

from . import Tag

class Event(BaseModel):

    """An extracted event and information regarding it."""

    title = ndb.StringProperty(required=True)
    image_link = ndb.StringProperty(required=True)
    description = ndb.StringProperty(indexed=False)
    location = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True)
    price = ndb.FloatProperty()
    capacity = ndb.IntegerProperty()
    tags = ndb.KeyProperty(kind=Tag,repeated=True)


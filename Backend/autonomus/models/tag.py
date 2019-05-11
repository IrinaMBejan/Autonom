from autonomus.models.base import BaseModel, ndb


class Tag(BaseModel):

    """Tags added manually or extracted with events."""

    name = ndb.StringProperty(required=True)

from autonomus.models.base import BaseModel, ndb


class Link(BaseModel):

    """Links which are being monitored for events extraction."""

    follow_link = ndb.StringProperty(required=True)

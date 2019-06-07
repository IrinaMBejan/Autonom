from autonomus.models import Tag


def add_tag(tag_name):
    tag = Tag(name=tag_name)
    return tag.put()

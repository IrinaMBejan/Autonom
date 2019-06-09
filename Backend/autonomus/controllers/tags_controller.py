from autonomus.models import Tag

import re

def add_tag(tag_name):
    tag = Tag(name=tag_name)
    return tag.put()

def get_Tags(text):
    tags = Tag.all()
    dictionar = {}
    for someShit in tags:
        list=[]
        for word in re.findall(r'\w+',someShit.name):
            list.append(word.lower())

        dictionar[someShit.urlsafe]=list.copy()

    listaTaguri=[]
    text= str(text).lower()

    for k,v in dictionar.items():
        if any(x in text for x in v):
            listaTaguri.append( Tag.get( k) .key)

    return listaTaguri


def get_all_tags():
    return Tag.all()


def get_tag(urlsafe):
    return Tag.get(urlsafe)

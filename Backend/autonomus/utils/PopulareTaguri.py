import json
from urllib.request import Request, urlopen
from autonomus.models import Tag

class JsonObject(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)

def getTagKey(name):
    query = Tag.query()
    query.add_filter('name', '=', name)
    query_list = query.fetch()


    for x in query_list:
        return x.key


    tag = Tag(name=name)
    key = tag.put()
    return key


def populareTaguri():
    headers = {
        'Authorization': 'Bearer UQX3SCD7LBHRUIATU5BC',
        'Content-Type': 'application/json'
    }
    request= Request('https://www.eventbriteapi.com/v3/categories/',headers=headers)
    response_body = urlopen(request).read()
    tags = JsonObject(response_body)

    for tag in tags.categories:
        if tag['name'] != 'Other':
            print(tag['name'],getTagKey(tag['name']))


populareTaguri()
import datetime
import pytz
import json
import string
from urllib.request import Request, urlopen
from autonomus.models import Tag, Event, Link,User
from dateutil import parser
from autonomus.controllers import tags_controller, events_controller
import requests
import re
from autonomus.utils import sms

class JsonObject(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)

meetUpHeaders = {
        'Authorization': 'Bearer 48bafed7ddb40e635bf562959a48d0ba',
        'Content-Type': 'application/json'
    }

eventBrideHeaders = {
    'Authorization': 'Bearer UQX3SCD7LBHRUIATU5BC',
    'Content-Type': 'application/json'
}

def addEventBrite(event):

        newEveniment = Event()
        if 'start' in event and type(event['start']) is dict and 'utc' in event['start']:
            newEveniment.date = parser.parse(event['start']['utc'])
            utc = pytz.UTC
            if datetime.datetime.now().replace(tzinfo=utc) < newEveniment.date.replace(tzinfo=utc):
                if 'name' in event:
                    if type(event['name']) is dict and 'text' in event['name']:
                        if not events_controller.getEvent(event['name']['text']):
                            newEveniment.title = event['name']['text']
                            newEveniment.tags = tags_controller.get_Tags(newEveniment.title)

                            if 'description' in event:
                                if 'text' in event['description']:
                                    description = event['description']['text']

                                    newEveniment.description = description
                                    newEveniment.tags += tags_controller.get_Tags(description)

                            newEveniment.image_link = 'N/A'
                            if 'logo' in event:
                                if type(event['logo']) is dict:
                                    if 'url' in event['logo']:
                                        newEveniment.image_link = event['logo']['url']


                            if 'is_free' in event:
                                if event['is_free']:
                                    newEveniment.price = 0.0
                                else:
                                    newEveniment.price = 1.0

                            newEveniment.location = 'N/A'
                            if 'venue' in event:
                                if type(event['venue']) is dict:
                                    if 'address' in event['venue']:
                                        if 'localized_address_display' in event['venue']['address']:
                                            newEveniment.location = event['venue']['address'][
                                                'localized_address_display']
                                        elif 'localized_area_display' in event['venue']['address']:
                                            newEveniment.location = event['venue']['address'][
                                                'localized_area_display']
                                        elif 'address_1' in event['venue']['address']:
                                            newEveniment.location = event['venue']['address']['address_1']

                            # print(newEveniment.location)

                            if 'category_id' in event and event['category_id'] != None:
                                newEveniment.tags += tags_controller.get_Tags(event['category_id'])

                            newEveniment.put()
                            return True

        return False

def eventBrite():


    page_number = 1

    while (True):

        request = Request('https://www.eventbriteapi.com/v3/events/search/?expand=venue&page=' + str(page_number),
                          headers=eventBrideHeaders)

        response_body = urlopen(request).read()

        jsonResponse = JsonObject(response_body)

        for event in jsonResponse.events:
            addEventBrite(event)

        if 'page_number' not in jsonResponse.pagination or 'page_count' not in jsonResponse.pagination:
            break

        page_number = jsonResponse.pagination['page_number'] + 1
        page_count = jsonResponse.pagination['page_count']

        if (page_number > page_count):
            break

def addMeetUpEvent(event):
    newEvent = Event()
    if 'name' in event:
        if not events_controller.getEvent(event['name']):
            newEvent.title = event['name']
            newEvent.tags = tags_controller.get_Tags(newEvent.title)

            if 'description' in event:
                newEvent.description = event['description']
                newEvent.tags += tags_controller.get_Tags(newEvent.description)

            newEvent.location = ''
            if 'venue' in event:

                if 'localized_country_name' in event['venue']:
                    newEvent.location += event['venue']['localized_country_name'] + ' '
                if 'city' in event['venue']:
                    newEvent.location += event['venue']['city'] + ' '
                if 'address_1' in event['venue']:
                    newEvent.location += event['venue']['address_1'] + ' '

            elif 'how_to_find_us' in event:
                newEvent.location += event['how_to_find_us']

            newEvent.image_link = 'N/A'
            if 'photo_url' in event:
                newEvent.image_link = event['photo_url']

            if 'time' in event:
                newEvent.date = datetime.datetime.utcfromtimestamp(event['time'] // 1000).replace(
                    microsecond=event['time'] % 1000 * 1000)

            newEvent.put()
            return True

    return False

def meetUp():


    for caract in string.ascii_lowercase:

        request = Request('https://api.meetup.com/2/open_events?&sign=true&photo-host=public&text='+caract+'&page=200000000',headers=meetUpHeaders)
        response_body = urlopen(request).read()
        response = JsonObject(response_body)

        for event in response.results:
           addMeetUpEvent(event)

def scanMeetUpPage(url):
    # a meetup group
    if 'meetup.com' in url:
        groupName= url.split('meetup.com/')[1].replace('/',"")
#         verificam daca este un grup valid, daca nu este marcam acest link pentru stergere

        request = requests.get('https://api.meetup.com/'+groupName,headers=meetUpHeaders)
        if request.status_code ==404:
            return -1

#         linkul este corect , colectam evenimente
        request = requests.get('https://api.meetup.com/' + groupName + '/events?&sign=true&photo-host=public&page=200000000', headers=meetUpHeaders)
        events= request.json()
        nrEvenimenteAdaugate = 0
        for event in events:
            if addMeetUpEvent(event):
                nrEvenimenteAdaugate += 1

        return nrEvenimenteAdaugate

    return 0

def scanEventBritePage(url):
    if 'eventbrite.com' in url:
        request = requests.get(url, headers=eventBrideHeaders)

        links= re.findall(r'(https?://\S+)', request.text)

        res = [k for k in links if 'eventbrite.com' in k]
        nrEvenimenteAdaugate=0
        util = False
        for el in res:
            sp= el.split('?aff')
            eventLink= sp[0].split('"')
            eventNr= eventLink[0].rsplit('-',1)
            if len(eventNr) > 1:
                    if eventNr[1].isdigit():
                        util = True
                        request = requests.get('https://www.eventbriteapi.com/v3/events/'+eventNr[1]+'/?expand=venue' ,
                            headers = eventBrideHeaders)

                        response_body = request.text
                        if addEventBrite(dict(json.loads (response_body))):
                            nrEvenimenteAdaugate += 1


        if util:
            return nrEvenimenteAdaugate

        return -1

    return 0

def scanAllLinks():
    links = Link.all()
    nrEvents = 0
    for l in links:
        if 'meetup.com' in l.follow_link:
            nrEvenimenteAdaugate = scanMeetUpPage(l.follow_link)
            if nrEvenimenteAdaugate == -1:
                l.remove()
            else:
                nrEvents+=nrEvenimenteAdaugate

        elif 'eventbrite.com' in l.follow_link:
            nrEvenimenteAdaugate = scanEventBritePage(l.follow_link)
            if nrEvenimenteAdaugate==-1:
                l.remove()
            else:
                nrEvents+=nrEvenimenteAdaugate

    if nrEvents >1:
        allEvents= Event.all();
        for event in allEvents:
            if event.title != None and event.date!=None and event.location != None:
                users= User.all()
                for user in users:
                    if user.phone != None:
                        sms.send_sms(user.phone, "Did you see the "+event.title+ "It's on " +event.date.strftime("%Y-%m-%d %H:%M")+" at "+event.location+"! Join our platform, there are "+str(+ nrEvents)+" new events!")
                return 'Mesaje trimise'


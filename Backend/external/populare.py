import datetime
import pytz
import json
import string
from urllib.request import Request, urlopen
from autonomus.models import Tag, Event
from google.cloud import datastore
from dateutil import parser
from webbot import Browser

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

def existEvent(name):
    query = Event.query()
    query.add_filter('title', '=', name)
    query_list = query.fetch()

    for x in query_list:
        return True

    return False

def identificaTaguri (text) :
    result = []
    copy =text.lower()
    if 'music' in copy:
        result.append('103')
    if 'business' in copy or 'professional' in copy:
        result.append('101')
    if 'food' in copy or 'drink' in copy:
        result.append('110')
    if 'community' in copy or 'culture' in copy:
        result.append('113')
    if 'visual' in copy or 'art' in copy:
        result.append('105')
    if 'film' in copy or 'media' in copy or 'entertainment' in copy:
        result.append('104')
    if 'sport' in copy or 'fitness' in copy:
        result.append('108')
    if  'health' in copy or 'wellness' in copy:
        result.append('107')
    if 'science' in copy or 'technology' in copy:
        result.append('102')
    if 'travel' in copy or 'outdoor' in copy:
        result.append('109')
    if 'charity' in copy or 'causes' in copy:
        result.append('111')
    if 'god' in copy or 'religion' in copy or 'church' in copy or 'spirituality' in copy:
        result.append('114')
    if 'family' in copy or 'education' in copy :
        result.append('115')
    if 'holiday' in copy or 'seasonal' in copy:
        result.append('116')
    if 'government' in copy or 'politic' in copy:
        result.append('112')
    if 'fashion' in copy or 'beauty' in copy:
        result.append('106')
    if 'home' in copy or 'life' in copy:
        result.append('117')
    if 'auto' in copy or 'air' in copy or 'boat' in copy:
        result.append('118')
    if 'hobbie' in copy or 'interest' in copy:
        result.append('119')
    if 'school' in copy :
        result.append('120')

    return result

def creazaListaFinalaDeTaguri(lista):
    result = []
    for category in lista:
        if category == '103':
            result.append(getTagKey('Music'))
        elif category == '101':
            result.append(getTagKey('Business & Professional'))
        elif category == '110':
            result.append(getTagKey('Food & Drink'))
        elif category == '113':
            result.append(getTagKey('Community & Culture'))
        elif category == '105':
            result.append(getTagKey('Performing & Visual Arts'))
        elif category == '104':
            result.append(getTagKey('Film, Media & Entertainment'))
        elif category == '108':
            result.append(getTagKey('Sports & Fitness'))
        elif category == '107':
            result.append(getTagKey('Health & Wellness'))
        elif category == '102':
            result.append(getTagKey('Science & Technology'))
        elif category == '109':
            result.append(getTagKey('Travel & Outdoor'))
        elif category == '111':
            result.append(getTagKey('Charity & Causes'))
        elif category == '114':
            result.append(getTagKey('Religion & Spirituality'))
        elif category == '115':
            result.append(getTagKey('Family & Education'))
        elif category == '116':
            result.append(getTagKey('Seasonal & Holiday'))
        elif category == '112':
            result.append(getTagKey('Government & Politics'))
        elif category == '106':
            result.append(getTagKey('Fashion & Beauty'))
        elif category == '117':
            result.append(getTagKey('Home & Lifestyle'))
        elif category == '118':
            result.append(getTagKey('Auto, Boat & Air'))
        elif category == '119':
            result.append(getTagKey('Hobbies & Special Interest'))
        elif category == '120':
            result.append(getTagKey('School Activities'))

    if len(result) == 0:
        result.append(getTagKey('Other'))

    return result

def eventBrite():
    headers = {
        'Authorization': 'Bearer UQX3SCD7LBHRUIATU5BC',
        'Content-Type': 'application/json'
    }

    page_number = 1

    while (True):

        request = Request('https://www.eventbriteapi.com/v3/events/search/?expand=venue&page=' + str(page_number),
                          headers=headers)

        response_body = urlopen(request).read()

        test1 = JsonObject(response_body)

        for event in test1.events:

            newEveniment = Event()

            if 'start' in event and type(event['start']) is dict and 'utc' in event['start']:
                newEveniment.date = parser.parse(event['start']['utc'])
                utc = pytz.UTC
                if datetime.datetime.now().replace(tzinfo=utc) < newEveniment.date.replace(tzinfo=utc):
                    if 'name' in event:
                        if type(event['name']) is dict and 'text' in event['name']:
                            if not existEvent(event['name']['text']):
                                newEveniment.title = event['name']['text']

                                taguri = identificaTaguri(newEveniment.title)

                                if 'description' in event:
                                    if 'text' in event['description']:
                                        description = event['description']['text']

                                        newEveniment.description = description
                                        taguri += identificaTaguri(newEveniment.description)


                                newEveniment.image_link = 'N/A'
                                if 'logo' in event:
                                    if type(event['logo']) is dict:
                                        if 'url' in event['logo']:
                                            newEveniment.image_link = event['logo']['url']
                                            # print(newEveniment.image_link)  # image link

                                # if 'capacity' in event:
                                #     capacity = event['capacity']
                                #     if(capacity==None):
                                #         capacity=0
                                #     newEveniment.capacity=capacity

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

                                    taguri += event['category_id']



                                newEveniment.tags = creazaListaFinalaDeTaguri(set(taguri))

                                newEveniment.put()


        if 'page_number' not in test1.pagination or 'page_count' not in test1.pagination:
            break

        page_number = test1.pagination['page_number'] + 1
        page_count = test1.pagination['page_count']

        if (page_number > page_count):
            break

def populareTaguri():
    headers = {
        'Authorization': 'Bearer UQX3SCD7LBHRUIATU5BC',
        'Content-Type': 'application/json'
    }
    request= Request('https://www.eventbriteapi.com/v3/categories/',headers=headers)
    response_body = urlopen(request).read()
    tags = JsonObject(response_body)

    for tag in tags.categories:
        print(tag['name'],getTagKey(tag['name']))

def meetUp():

    meetUpHeaders = {
        'Authorization': 'Bearer 48bafed7ddb40e635bf562959a48d0ba',
        'Content-Type': 'application/json'
    }

    for caract in string.ascii_lowercase:

        request = Request('https://api.meetup.com/2/open_events?&sign=true&photo-host=public&text='+caract+'&page=200000000',headers=meetUpHeaders)
        response_body = urlopen(request).read()
        response = JsonObject(response_body)

        for event in response.results:
            newEvent = Event()
            if 'name' in event:
                if not existEvent(event['name']):
                    newEvent.title = event['name']
                    taguri = identificaTaguri(newEvent.title)


                    if 'description' in event:
                        newEvent.description=event['description']
                        taguri += identificaTaguri(newEvent.description)


                    newEvent.location =''
                    if 'venue' in event:

                        if 'localized_country_name' in event['venue']:
                            newEvent.location += event['venue']['localized_country_name'] + ' '
                        if 'city' in event['venue']:
                            newEvent.location += event['venue']['city'] + ' '
                        if 'address_1' in event['venue']:
                            newEvent.location += event['venue']['address_1'] + ' '

                    elif 'how_to_find_us' in event:
                        newEvent.location+=event['how_to_find_us']


                    newEvent.image_link = 'N/A'
                    if 'photo_url' in event:
                        newEvent.image_link=event['photo_url']


                    if 'time' in event:
                        newEvent.date= datetime.datetime.utcfromtimestamp(event['time'] // 1000).replace(microsecond=event['time'] % 1000 * 1000)



                    newEvent.tags = creazaListaFinalaDeTaguri(set(taguri))
                    print(newEvent.tags)
                    newEvent.put()

def facebookEventLinks():
    url='https://www.facebook.com/directory/events_links/city/101882609853782/'
    web=Browser()
    web.go_to(url)
    try:
        pagina = web.find_elements(id='content')

        for elem in pagina[0].find_elements_by_tag_name('a'):
            if elem.get_attribute('href'):
                getEvent( elem.get_attribute('href'))

    except:
        print("Nu am putut colecta toate datele")


def facebookEventDiscovery():
    url='https://www.facebook.com/events/discovery/?city_id=101882609853782'
    web = Browser()
    web.go_to(url)
    try:
        pagina = web.find_elements(id='content')

        for elem in pagina[0].find_elements_by_tag_name('a'):
            if elem.get_attribute('href'):
                getEvent(elem.get_attribute('href'))

    except:
        print("Nu am putut colecta toate datele")


def getEvent(url):

    if 'facebook.com/events/' in url:
        web = Browser()
        web.go_to(url)
        try:
            newEvent = Event()
            pagina = web.find_elements(id='content_container')

            eventHead= pagina[0].find_element_by_id('event_header')
            primary= eventHead.find_element_by_id('event_header_primary')
            link= primary.find_element_by_tag_name('img').get_attribute('src')
            titlu= primary.find_element_by_id('seo_h1_tag').text
            newEvent.title=titlu

            taguri = identificaTaguri(newEvent.title)

            newEvent.image_link=link

            sumar= eventHead.find_element_by_id('event_summary')
            data= sumar.find_element_by_id('event_time_info')

            for x in data.find_elements_by_css_selector("*"):
               if x.get_attribute('content'):
                    y = x.get_attribute('content').split('to')
                    newEvent.date = parser.parse(y[0])

            x= data.find_element_by_xpath("./following-sibling::li")
            location= x.text[x.text.find('\n'):x.text.rfind('\n')]
            newEvent.location=location


            detalii=pagina[0].find_element_by_id('reaction_units')
            for elem in detalii.find_elements_by_css_selector("*"):
                if elem.get_attribute('data-testid') == 'event-permalink-details':
                    newEvent.description = elem.text
                    taguri += identificaTaguri(newEvent.description)

            if detalii.find_element_by_tag_name('ul'):
                taguri += identificaTaguri (detalii.find_element_by_tag_name('ul').text)

            newEvent.tags = creazaListaFinalaDeTaguri(set(taguri))

            newEvent.put()

            web.close_current_tab()

        except :
            print("Nu am putut colecta toate datele")
    else:
        print('Bad url')



def main():


    global client
    client = datastore.Client(project="autonomus", namespace="development")


    # eventBrite()
    # meetUp()
    # facebookEventDiscovery()
    facebookEventLinks()


if __name__ == "__main__":
    main()

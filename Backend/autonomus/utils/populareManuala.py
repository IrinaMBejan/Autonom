from autonomus.models import Event
from dateutil import parser
from webbot import Browser
from autonomus.controllers import tags_controller
from autonomus.models import Link
import os
from google.cloud import datastore


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

            newEvent.tags= tags_controller.get_Tags(newEvent.title)

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
                    newEvent.tags+= tags_controller.get_Tags(newEvent.description)

            if detalii.find_element_by_tag_name('ul'):
                newEvent.tags += tags_controller.get_Tags(detalii.find_element_by_tag_name('ul').text)

            newEvent.put()

            web.close_current_tab()

        except :
            print("Nu am putut colecta toate datele")
    else:
        print('Bad url')

def scanFacebookPage(url):
    if 'facebook.com' in url:
        web = Browser()
        web.go_to(url)
        try:
            pagina = web.find_elements(id='content')

            for elem in pagina[0].find_elements_by_tag_name('a'):
                if elem.get_attribute('href'):
                    getEvent(elem.get_attribute('href'))

        except:
            print(url,"Nu am putut colecta toate datele")


def scanLinksOnFacebook():
    links = Link.all()
    for l in links:
        if 'facebook.com' in l.follow_link:
            scanFacebookPage(l.follow_link)


def main():

    global client
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/andrei/autonomus.json"
    client = datastore.Client(project="autonomus", namespace="development")

    # scanFacebookPage('https://www.facebook.com/events/discovery/?city_id=101882609853782')
    # scanFacebookPage('https://www.facebook.com/directory/events_links/city/101882609853782/')
    # scanLinksOnFacebook()
    nrEvents =10
    if nrEvents >0:
        for event in Event.all():
            if event.title != None and event.date!=None and event.location != None:
                print( "Did you see the "+event.title+ "It's on " +event.date.strftime("%Y-%m-%d %H:%M")+" at "+event.location+"! Join our platform, there are "+str(+ nrEvents)+" new events!")
                break

if __name__ == '__main__':
    main()
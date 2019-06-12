from autonomus.models import Event
from dateutil import parser
from webbot import Browser
from autonomus.controllers import tags_controller, links_controller
from autonomus.models import Link



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



scanLinksOnFacebook()



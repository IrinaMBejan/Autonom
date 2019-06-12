from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Substitution

API_KEY = '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'
API_KEY_ID = 'egd1yywWRbeVF2gcGhTH2Q'

ENCODING = "utf-8"
DEFAULT_MAIL="irinam.bejan@gmail.com"


def link(urlsafe):
    return "https://develop-dot-autonomus.appspot.com/events/details?event_id=" + urlsafe


def send_newsletter(users, event1, event2):
    for user in users:
        send_mail(DEFAULT_MAIL, user.username, user.email, event1, event2)


def send_mail(from_mail, username, to_mails, event1, event2):
    message = Mail(
        from_email=from_mail,
        to_emails=to_mails
    )
    
    message.dynamic_template_data = {
    'name': username,
    'title1' : event1.title,
    'src1' : link(event1.urlsafe),
    'loc1': event1.location,
    'date1': event1.date.strftime('%d-%m-%Y %H:%M'),
    'title2' : event2.title,
    'src2' : link(event2.urlsafe),
    'loc2': event2.location,
    'date2': event2.date.strftime('%d-%m-%Y %H:%M')
    }
   
    print('before')
    message.template_id = 'd-6607926b2aba4f8fba984dccdaa9ece6'
    client = SendGridAPIClient(API_KEY)
    response = client.send(message)
    code = response.status_code
    print('after')
    was_successful = lambda ret_code: ret_code // 100 in (2, 3)
    if not was_successful(code):
        raise Exception("Couldn't send e-mail: {} {}".format(code, response.body))


from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Substitution

API_KEY = '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'
API_KEY_ID = 'egd1yywWRbeVF2gcGhTH2Q'

ENCODING = "utf-8"
DEFAULT_MAIL="irinam.bejan@gmail.com"


def send_mail(from_mail, to_mails, subject, text_content, html_content=None):
    html_content = html_content or text_content
    message = Mail(
        from_email=from_mail,
        to_emails=to_mails,
        subject=subject,
        plain_text_content=text_content,
        html_content=html_content
    )
    
    message.dynamic_template_data = {
    'name': 'Testing Templates & Stuff',
    }
    
    message.template_id = 'd-6607926b2aba4f8fba984dccdaa9ece6'
    client = SendGridAPIClient(API_KEY)
    response = client.send(message)
    code = response.status_code

    was_successful = lambda ret_code: ret_code // 100 in (2, 3)
    if not was_successful(code):
        raise Exception("Couldn't send e-mail: {} {}".format(code, response.body))


send_mail(DEFAULT_MAIL, DEFAULT_MAIL, "Ana", "Bla bla")

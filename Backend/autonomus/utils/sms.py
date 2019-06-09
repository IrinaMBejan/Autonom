from twilio.rest import Client


account_sid = 'AC27aa1654af63e7e0d8ab28abe49685df'
auth_token = '0be78ee66213ccee2a361dd674e48505'
client = Client(account_sid, auth_token)

def send_sms(to, body):
    message = client.messages \
                    .create(
                         body=body,
                         from_='+19564460231',
                         to=to
                    )


if __name__ == "__main__":
    send_sms('+40757051062', "Sms-ul a mers")

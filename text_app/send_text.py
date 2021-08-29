import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

load_dotenv()


def send_text(body: str,
              to_number: str) -> dict:
    account_sid = os.environ.get('ACCOUNT_SID')
    auth_token = os.environ.get('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_=os.environ.get('PHONE_NUMBER'),
        to=to_number
    )

    if message.error_code:
        return_dict = {'message': 'error',
                       'sent': False,
                       message.error_code: message.error_message}
    else:
        return_dict = {'message': 'success',
                       'sent': True}

    return return_dict


if __name__ == "__main__":
    send_text("Ridge test", os.environ.get('TO_NUMBER'))

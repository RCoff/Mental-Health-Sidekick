import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

load_dotenv()


def send_text(form_link: str,
              user_first_name: str,
              to_number: str) -> dict:
    account_sid = os.environ.get('ACCOUNT_SID')
    auth_token = os.environ.get('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Hi, {user_first_name}\n"
             f"I hope you're having a great day today\n"
             f"Please tell me how you're feeling:\n"
             f"{form_link}",
        from_=os.environ.get('PHONE_NUMBER'),
        to=to_number
    )

    # print(message.sid)

    if message.error_code:
        return_dict = {'Status': 'Error',
                       message.error_code: message.error_message}
    else:
        return_dict = {'message': 'Success'}

    return return_dict


if __name__ == "__main__":
    send_text("test", "Ridge", os.environ.get('TO_NUMBER'))

from django.shortcuts import render
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

from rest_framework import viewsets
from rest_framework import permissions

from .serializers import ResponseSerializer
from .models import ResponseModel

load_dotenv()


# Create your views here.
def send_text():
    account_sid = os.environ.get('ACCOUNT_SID')
    auth_token = os.environ.get('AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="This is an automated text message",
        from_=os.environ.get('PHONE_NUMBER'),
        to=os.environ.get('TO_NUMBER')
    )

    print(message.sid)


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.AllowAny]


if __name__ == "__main__":
    send_text()


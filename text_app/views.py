# Standard Imports
import os

# 3rd Party Imports
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Django Imports
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import View
from django.core import signing
from rest_framework import viewsets
from rest_framework import permissions

# Local Imports
from .serializers import ResponseSerializer
from .models import ResponseModel
from .forms import ResponseForm
from .send_text import send_text

load_dotenv()


# Create your views here.
class ResponseFormView(View):
    template_name = 'response_form.html'
    form_class = ResponseForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            signer = signing.Signer()
            form_response = ResponseModel(response=form.cleaned_data['response'],
                                          text_response=signer.sign_object({'text_response': str(form.cleaned_data['text_response'])}))
            form_response.save()

            return HttpResponseRedirect(reverse('success'))


class ResponseFormSuccess(View):
    template_name = 'success.html'

    def get(self, request):
        return render(request, self.template_name)


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.AllowAny]

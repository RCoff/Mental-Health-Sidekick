# Standard Imports
import datetime
import os

# 3rd Party Imports
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import requests

# Django Imports
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import View
from django.core import signing
from rest_framework import viewsets
from rest_framework import permissions

# Local Imports
from .serializers import ResponseSerializer
from .models import ResponseModel, ActiveSurveyStore
from .forms import ResponseForm
from .send_text import send_text

load_dotenv()


# Create your views here.
class ResponseFormView(View):
    template_name = 'response_form.html'
    form_class = ResponseForm

    def get(self, request, survey_id=None):
        form = self.form_class()

        if not survey_id:
            if 'id' in request.GET:
                survey_id = request.GET['id']
            else:
                # TODO: Return An error
                return  # an error

        survey_obj = ActiveSurveyStore.objects.get(active_survey_id=survey_id)
        if not survey_obj.expired_or_completed:
            request.session['survey_id'] = str(survey_id)
            user_first_name = survey_obj.user.first_name
            return render(request, self.template_name, context={'form': form,
                                                                'user_first_name': user_first_name,
                                                                'survey_id': survey_id})
        else:
            print("No longer valid")

    def post(self, request, survey_id=None):
        form = self.form_class(request.POST)

        if form.is_valid():
            if survey_id is None:
                survey_id = request.session['survey_id']

            signer = signing.Signer()
            if form.cleaned_data['text_response']:
                text_response = signer.sign_object({'text_response': str(form.cleaned_data['text_response'])})
            else:
                text_response = ''

            survey_obj = ActiveSurveyStore.objects.get(active_survey_id=survey_id)
            form_response = ResponseModel(id=survey_obj,
                                          response=form.cleaned_data['response'],
                                          text_response=text_response)
            form_response.save()

            survey_obj.completed = True
            survey_obj.save()

            if survey_obj.user.userphonenumber.next_survey_datetime:
                survey_obj.user.userphonenumber.next_survey_datetime = datetime.datetime.combine(
                    survey_obj.user.userphonenumber.next_survey_datetime.date() + datetime.timedelta(days=1),
                    survey_obj.user.userphonenumber.send_survey_time)
                survey_obj.user.userphonenumber.save()

            return HttpResponseRedirect(reverse('success'))
        else:
            # TODO: Return an error
            return


class ResponseFormSuccess(View):
    template_name = 'success.html'

    def get(self, request):
        dog_image = None
        rdi = requests.get("https://dog.ceo/api/breeds/image/random").json()
        if 'status' in rdi:
            if rdi['status'] == "success":
                dog_image = rdi['message']

        return render(request, self.template_name, context={'dog_image_url': dog_image})


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.AllowAny]

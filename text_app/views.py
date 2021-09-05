# Standard Imports
import datetime
import os

# 3rd Party Imports
from dotenv import load_dotenv
import requests
import logging

# Django Imports
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.views.generic import View
from django.core import signing
from django.utils import timezone as dtz
from rest_framework import viewsets
from rest_framework import permissions

# Local Imports
from .serializers import ResponseSerializer
from .models import ResponseModel, ActiveSurveyStore

from .forms import ResponseForm
from .models import ResponseModel

load_dotenv()


# Create your views here.
class ResponseFormView(View):
    template_name = 'response_form.html'
    form_class = ResponseForm

    def get(self, request, survey_id=None):
        if not survey_id:
            if 'id' in request.GET:
                logging.debug('Survey ID not found in URL. Getting survey ID from request')
                survey_id = request.GET['id']
            else:
                # TODO: Return An error
                logging.error('Survey ID not found in URL or in request')
                return HttpResponse("Survey ID not found in URL")

        try:
            logging.debug('Attempting to get survey response', extra={'survey_id': survey_id})
            submitted_form = ResponseModel.objects.get(id=survey_id)
            logging.debug('Survey found in batabase', extra={'survey_id': survey_id})

            populated_survey_form = {'mood_response': submitted_form.mood_response,
                                     'hours_slept': submitted_form.hours_slept,
                                     'daily_weight': submitted_form.daily_weight,
                                     'daily_symptoms': submitted_form.daily_symptoms.all()}

            if submitted_form.text_response:
                signer = signing.Signer()
                decrypted_text_response = signer.unsign_object(submitted_form.text_response)
                if decrypted_text_response:
                    decrypted_text_response.get('text_response')
                    populated_survey_form.update({'text_response': decrypted_text_response})

            form = self.form_class()
        except ResponseModel.DoesNotExist:
            logging.debug('Survey response not found, using empty form', survey_id={'survey_id': survey_id})
            form = self.form_class()

        survey_obj = ActiveSurveyStore.objects.get(active_survey_id=survey_id)
        request.session['survey_id'] = str(survey_id)
        user_first_name = survey_obj.user.first_name
        return render(request, self.template_name, context={'form': form,
                                                            'user_first_name': user_first_name,
                                                            'survey_id': survey_id})

    def post(self, request, survey_id=None):
        form = self.form_class(request.POST)

        if form.is_valid():
            if survey_id is None:
                survey_id = request.session['survey_id']

            signer = signing.Signer()
            if form.cleaned_data['text_response']:
                text_response = signer.sign_object(
                    {'text_response': str(form.cleaned_data['text_response'])})
            else:
                text_response = ''

            survey_obj = ActiveSurveyStore.objects.get(active_survey_id=survey_id)
            form_response, created = ResponseModel.objects.update_or_create(
                id=survey_obj,
                defaults={'mood_response': form.cleaned_data['mood_response'],
                          'hours_slept': form.cleaned_data['hours_slept'],
                          'daily_weight': form.cleaned_data['daily_weight'],
                          'text_response': text_response})
            for symptom in form.cleaned_data['daily_symptoms']:
                form_response.daily_symptoms.add(symptom)
            form_response.save()

            survey_obj.completed = True
            survey_obj.save()

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

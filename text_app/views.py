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
               return  # an error

        request.session['survey_id'] = str(survey_id)
        return render(request, self.template_name, context={'form': form,
                                                            'survey_id': survey_id})

    def post(self, request, survey_id=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            if survey_id is None:
                survey_id = request.session['survey_id']

            signer = signing.Signer()
            survey_obj = ActiveSurveyStore.objects.get(active_survey_id=survey_id)

            form_response = ResponseModel(id=survey_obj,
                                          response=form.cleaned_data['response'],
                                          text_response=signer.sign_object({'text_response': str(form.cleaned_data['text_response'])}))
            form_response.save()

            survey_obj.expired_or_completed = True
            survey_obj.save()

            return HttpResponseRedirect(reverse('success'))


class ResponseFormSuccess(View):
    template_name = 'success.html'

    def get(self, request):
        return render(request, self.template_name)


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.AllowAny]

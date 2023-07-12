import os
import logging
from functools import wraps

from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
from dotenv import load_dotenv

from text_app.models import UserPhoneNumber

load_dotenv()
logger = logging.getLogger(__name__)


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""

    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(os.environ.get('AUTH_TOKEN'))

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.build_absolute_uri(),
            request.POST,
            request.META.get('HTTP_X_TWILIO_SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if
        # it's not
        if request_valid or settings.DEBUG:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    return decorated_function


@require_POST
@csrf_exempt
@validate_twilio_request
def receive_message(request):
    # Parse fields from POST data
    request_from = str(request.POST.get('From'))
    request_body = str(request.POST.get('Body')).strip()

    # Begin building a response
    response = MessagingResponse()

    # Check if sender is a registered user
    if not UserPhoneNumber.objects.filter(phone_number=request_from).exists():
        response.message("Sorry, I couldn't find your account in our records")
    else:
        response.message(f"You said: \"{request_body}\"")

    return HttpResponse(content=response, content_type="application/xml")

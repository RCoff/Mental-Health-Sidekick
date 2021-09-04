import os
import datetime
from urllib.parse import urljoin

import pytz
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone as dtz
from dotenv import load_dotenv

from text_app import models, send_text

load_dotenv()


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        base_url = os.environ['WEBSITE_HOSTNAME']

        for user in models.UserPhoneNumber.objects.all().filter(active=True):
            active_surveys = user.user.activesurveystore_set.model.objects.filter(expired=False, user=user.user)
            survey_id = active_surveys[0].active_survey_id
            survey_url = f"{base_url}form/{survey_id}"

            body = f"Hi, {user.user.first_name}\n" \
                   f"I hope you're having a great day today\n\n" \
                   f"We've updated our site! Now you can find more questions to " \
                   f"help track how you're feeling every day.\n\n" \
                   f"You can also now edit what you've already submitted today.\n" \
                   f"Try it out! {survey_url}"

            response = send_text.send_text(body, user.phone_number)

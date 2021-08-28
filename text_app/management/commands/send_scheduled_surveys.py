import os
import datetime
import uuid

from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv

from text_app import models, send_text

load_dotenv()


# TODO: Use celery or APscheduler for scheduling?
class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        for user in models.UserPhoneNumber.objects.all().filter(active=True):
            new_survey = models.ActiveSurveyStore(
                user=user.user,
                survey_expire_datetime=(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=12))
            )
            new_survey.save()

            survey_id = new_survey.active_survey_id
            base_url = os.environ['WEBSITE_HOSTNAME']
            url = f"{base_url}form/{survey_id}"

            send_text.send_text(url, user.phone_number)
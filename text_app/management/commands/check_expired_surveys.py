from django.core.management.base import BaseCommand, CommandError
from text_app import models, send_text
import datetime
import uuid

from .send_scheduled_surveys import create_survey


class Command(BaseCommand):
    help = 'Check surveys and mark if expired'

    def handle(self, *args, **options):
        for survey in models.ActiveSurveyStore.objects.all().filter(expired_or_completed=False,
                                                                    survey_expire_datetime__lte=datetime.datetime.now(datetime.timezone.utc)):
            update_survey = survey(
                expired=True
            )
            update_survey.save()

            # url = create_survey(survey.user)
            #
            # send_text.send_text(url, survey.user.userphonenumber.phone_number)

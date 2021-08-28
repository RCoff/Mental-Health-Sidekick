from django.core.management.base import BaseCommand, CommandError
from text_app import models, send_text
import datetime
import uuid


class Command(BaseCommand):
    help = 'Check surveys and mark if expired'

    def handle(self, *args, **options):
        for survey in models.ActiveSurveyStore.objects.all().filter(expired_or_completed=False,
                                                                    survey_expire_datetime__lte=datetime.datetime.now(datetime.timezone.utc)):
            update_survey = survey(
                expired_or_completed=True
            )

            # TODO: Send user a new survey if not already sent

            update_survey.save()

from django.core.management.base import BaseCommand, CommandError
from text_app import models, send_text
import datetime
import uuid
import logging

from .send_scheduled_surveys import create_survey

logger = logging.getLogger('backend')


class Command(BaseCommand):
    help = 'Check surveys and mark if expired'

    def handle(self, *args, **options):
        start_time = datetime.datetime.now(datetime.timezone.utc)
        logger.debug("Checking expired surveys", extra={'start_time': start_time})

        for survey in models.ActiveSurveyStore.objects.all().filter(expired=False,
                                                                    survey_expire_datetime__lte=datetime.datetime.now(
                                                                        datetime.timezone.utc)):
            logger.debug(f"Marking '{survey.active_survey_id}' as expired",
                         extra={'survey_id': survey.active_survey_id,
                                'expired_datetime': datetime.datetime.now(datetime.timezone.utc)})

            survey.expired = True
            survey.save()

        end_time = datetime.datetime.now(datetime.timezone.utc)
        logger.debug("Finished marking surveys as expired", extra={'start_time': start_time,
                                                                   'end_time': end_time,
                                                                   'run_time': end_time-start_time})

        return

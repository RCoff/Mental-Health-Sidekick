import logging

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from text_app import models

logger = logging.getLogger('backend')


class Command(BaseCommand):
    help = 'Check surveys and mark if expired'

    def handle(self, *args, **options):
        start_time = timezone.now()
        logger.debug("Checking expired surveys", extra={'start_time': start_time})

        for survey in models.ActiveSurveyStore.objects.all().filter(expired=False,
                                                                    survey_expire_datetime__lte=timezone.now()):
            logger.debug(f"Marking '{survey.active_survey_id}' as expired",
                         extra={'survey_id': survey.active_survey_id,
                                'expired_datetime': timezone.now()})

            survey.expired = True
            survey.save()

        end_time = timezone.now()
        logger.debug("Finished marking surveys as expired", extra={'start_time': start_time,
                                                                   'end_time': end_time,
                                                                   'run_time': end_time-start_time})

        return

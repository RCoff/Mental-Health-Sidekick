import os
import datetime
import uuid
import logging

import pytz
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone as dtz
from dotenv import load_dotenv

from text_app import models, send_text

load_dotenv()
logger = logging.getLogger('backend')


# TODO: Use celery or APscheduler for scheduling?
class Command(BaseCommand):
    help = "Sends text messages at a user's scheduled time"

    def handle(self, *args, **options):
        base_url = os.environ['WEBSITE_HOSTNAME']
        start_time = datetime.datetime.now(datetime.timezone.utc)
        logger.debug("Sending surveys texts", extra={'start_time': start_time})

        for user in models.UserPhoneNumber.objects.all().filter(active=True):
            active_surveys = user.user.activesurveystore_set.model.objects.filter(sent=False, expired=False,
                                                                                  completed=False, user=user.user)
            logger.debug(f"Checking user '{user.user_id}'", extra={'user_id': user.user_id,
                                                                   'active_surveys': len(active_surveys)})
            print(user.user.first_name)
            print(len(active_surveys))
            print(f"Next Survey At: {user.next_survey_datetime}")
            print(f"Current time: {datetime.datetime.now(datetime.timezone.utc)}")

            if len(active_surveys) == 0:
                survey_obj = create_survey(user)
                logger.debug("No active surveys found. Creating survey", extra={'user_id': user.user_id,
                                                                                'survey_id': survey_obj.active_survey_id})

                if user.next_survey_datetime <= datetime.datetime.now(datetime.timezone.utc):
                    survey_id = survey_obj.active_survey_id
                else:
                    continue

            elif len(active_surveys) == 1:
                if active_surveys[0].sent is False:
                    if user.next_survey_datetime <= datetime.datetime.now(datetime.timezone.utc):
                        survey_obj = active_surveys[0]
                        survey_id = survey_obj.active_survey_id
                    else:
                        continue
                else:
                    continue
            else:
                logger.error("User has more than 1 active survey",
                             extra={'user_id': user.user_id,
                                    'active_surveys': len(active_surveys),
                                    'survey_ids': active_surveys.values_list('active_survey_id', flat=True)})
                # TODO: Raise an error
                continue

            body = f"Hi, {user.user.first_name}\n" \
                   f"I hope you're having a great day today\n" \
                   f"Please tell me how you're feeling:\n" \
                   f"{base_url}form/{survey_id}"

            logger.debug("Sending survey text", extra={'user_id': user.user_id,
                                                       'survey_id': survey_id})
            response = send_text.send_text(body, user.phone_number)
            if response.get('sent'):
                survey_obj.sent = True
                survey_obj.sent_datetime = datetime.datetime.now(datetime.timezone.utc)
                survey_obj.save()

                survey_obj.user.userphonenumber.last_survey_sent_datetime = datetime.datetime.now(datetime.timezone.utc)
                survey_obj.user.userphonenumber.next_survey_datetime = dtz.make_aware(datetime.datetime.combine(
                    datetime.datetime.now(datetime.timezone.utc).date() + datetime.timedelta(days=1),
                    survey_obj.user.userphonenumber.send_survey_time), timezone=pytz.timezone('UTC'))
                survey_obj.user.userphonenumber.save()
                logger.debug("Survey sent successfully", extra={'user_id': user.user_id,
                                                                'survey_id': survey_id,
                                                                'sent_datetime': str(survey_obj.sent_datetime)})
            else:
                logger.error("Failed to send survey text", extra={'user_id': user.user_id,
                                                                  'survey_id': survey_id})

        end_time = datetime.datetime.now(datetime.timezone.utc)
        logging.info("Finished sending survey texts", extra={'start_time': start_time,
                                                             'end_time': end_time,
                                                             'run_time': end_time-start_time})
        return


def create_survey(user):
    new_survey = models.ActiveSurveyStore(
        user=user.user,
        survey_expire_datetime=(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            hours=int(user.expire_after_hours)))
    )
    new_survey.save()

    return new_survey

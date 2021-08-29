import os
import datetime
import uuid

import pytz
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone as dtz
from dotenv import load_dotenv

from text_app import models, send_text

load_dotenv()


# TODO: Use celery or APscheduler for scheduling?
class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        base_url = os.environ['WEBSITE_HOSTNAME']

        for user in models.UserPhoneNumber.objects.all().filter(active=True):
            active_surveys = user.user.activesurveystore_set.model.objects.filter(expired_or_completed=False)
            print(user.next_survey_datetime)
            print(datetime.datetime.now(datetime.timezone.utc))

            if len(active_surveys) == 0:
                survey_obj = create_survey(user)

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
                # TODO: Raise an error
                continue

            body = f"Hi, {user.user.first_name}\n" \
                   f"I hope you're having a great day today\n" \
                   f"Please tell me how you're feeling:\n" \
                   f"{base_url}form/{survey_id}"

            response = send_text.send_text(body, user.phone_number)
            if response.get('sent'):
                survey_obj.sent = True
                survey_obj.save()

                survey_obj.user.userphonenumber.last_survey_sent_datetime = datetime.datetime.now(datetime.timezone.utc)
                survey_obj.user.userphonenumber.next_survey_datetime = dtz.make_aware(datetime.datetime.combine(
                    datetime.datetime.now(datetime.timezone.utc).date() + datetime.timedelta(days=1),
                    survey_obj.user.userphonenumber.send_survey_time), timezone=pytz.timezone('UTC'))
                survey_obj.user.userphonenumber.save()

        return


def create_survey(user):
    new_survey = models.ActiveSurveyStore(
        user=user.user,
        survey_expire_datetime=(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            hours=user.expire_after_hours))
    )
    new_survey.save()

    return new_survey

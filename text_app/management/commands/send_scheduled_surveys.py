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
        base_url = os.environ['WEBSITE_HOSTNAME']

        for user in models.UserPhoneNumber.objects.all().filter(active=True):
            active_surveys = user.user.activesurveystore_set.model.objects.filter(expired_or_completed=False)

            if len(active_surveys) == 0:
                survey_obj = create_survey(user)

                if user.next_survey_datetime <= datetime.datetime.now(datetime.timezone.utc):
                    survey_id = survey_obj.active_survey_id
                else:
                    continue

            elif len(active_surveys) == 1:
                if active_surveys[0].sent is False:
                    survey_obj = active_surveys[0]
                    survey_id = survey_obj.active_survey_id
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

import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

import uuid


# Create your models here.
class ActiveSurveyStore(models.Model):
    BOOLEAN_CHOICES = ((True, True), (False, False),)

    active_survey_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey_expire_datetime = models.DateTimeField(auto_now=False, blank=False, null=False)
    sent = models.BooleanField(default=False, choices=BOOLEAN_CHOICES)
    expired_or_completed = models.BooleanField(default=False, choices=BOOLEAN_CHOICES)
    expired = models.BooleanField(default=False, choices=BOOLEAN_CHOICES)
    completed = models.BooleanField(default=False, choices=BOOLEAN_CHOICES)

    def save(self, *args, **kwargs):
        if self.expired is True or self.completed is True:
            self.expired_or_completed = True
        super(ActiveSurveyStore, self).save(*args, **kwargs)


class Disorder(models.Model):
    disorder = models.CharField(max_length=100, primary_key=True)
    disorder_shortname = models.CharField(max_length=10, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.disorder_shortname


class DailySymptoms(models.Model):
    symptom = models.CharField(max_length=50, primary_key=True)
    disorder = models.ManyToManyField(Disorder)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symptom.title()


class ResponseModel(models.Model):
    RESPONSE_CHOICES = (
        (-4, -4),
        (-3, -3),
        (-2, -2),
        (-1, -1),
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4)
    )

    id = models.OneToOneField(ActiveSurveyStore, on_delete=models.CASCADE, primary_key=True)
    mood_response = models.SmallIntegerField(choices=RESPONSE_CHOICES)
    hours_slept = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(24)])
    daily_weight = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    daily_symptoms = models.ManyToManyField(DailySymptoms)
    text_response = models.TextField(null=True, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

# TODO: Why doesn't this work?
# def default_next_survey(send_survey_time):
#     next_survey_datetime = datetime.datetime.combine(
#         datetime.datetime.now(datetime.timezone.utc).date(),
#         send_survey_time)
#
#     if datetime.datetime.now(datetime.timezone.utc).time() > send_survey_time:
#         next_survey_datetime = (next_survey_datetime + datetime.timedelta(days=1))
#
#     return next_survey_datetime


class UserPhoneNumber(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    phone_number = models.PositiveBigIntegerField(blank=True, null=True)
    active = models.BooleanField(default=True, choices=((True, True), (False, False),))
    send_survey_time = models.TimeField()
    expire_after_hours = models.PositiveSmallIntegerField(default=12)
    survey_interval_hours = models.PositiveSmallIntegerField(default=24)
    last_survey_sent_datetime = models.DateTimeField(null=True, blank=True)
    next_survey_datetime = models.DateTimeField()

    # def save(self, *args, **kwargs):
    #     if self.last_survey_sent_datetime is not None:
    #         self.next_survey_datetime = self.last_survey_sent_datetime + datetime.timedelta(
    #             hours=self.survey_interval_hours)
    #     super(UserPhoneNumber, self).save(*args, **kwargs)


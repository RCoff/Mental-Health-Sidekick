from django.db import models
from django.contrib.auth.models import User

import uuid


# Create your models here.
class ResponseModel(models.Model):
    RESPONSE_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
    )

    # id = models.OneToOneField(ActiveSurveyStore, on_delete=models.CASCADE, primary_key=True)
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True)
    response = models.SmallIntegerField(choices=RESPONSE_CHOICES)
    text_response = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now=True)


class UserPhoneNumber(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    phone_number = models.PositiveBigIntegerField(blank=True, null=True)
    active = models.BooleanField(default=True, choices=((True, True), (False, False),))


class ActiveSurveyStore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active_survey_id = models.UUIDField(default=uuid.uuid4(), blank=False, null=False)
    survey_expire_datetime = models.DateTimeField(auto_now=False, blank=False, null=False)
    expired = models.BooleanField(default=False, choices=((True, True), (False, False),))

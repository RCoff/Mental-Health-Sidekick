from django.db import models
from django.contrib.auth.models import User

import uuid


# Create your models here.
class ActiveSurveyStore(models.Model):
    active_survey_id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey_expire_datetime = models.DateTimeField(auto_now=False, blank=False, null=False)
    expired_or_completed = models.BooleanField(default=False, choices=((True, True), (False, False),))
    expired = models.BooleanField(default=False, choices=((True, True), (False, False),))
    completed = models.BooleanField(default=False, choices=((True, True), (False, False),))

    def save(self, *args, **kwargs):
        if self.expired is True or self.completed is True:
            self.expired_or_completed = True
        super(ActiveSurveyStore, self).save(*args, **kwargs)


class ResponseModel(models.Model):
    RESPONSE_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
    )

    id = models.OneToOneField(ActiveSurveyStore, on_delete=models.CASCADE, primary_key=True)
    # id = models.UUIDField(default=uuid.uuid4(), primary_key=True)
    response = models.SmallIntegerField(choices=RESPONSE_CHOICES)
    text_response = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now=True, editable=False)


class UserPhoneNumber(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    phone_number = models.PositiveBigIntegerField(blank=True, null=True)
    active = models.BooleanField(default=True, choices=((True, True), (False, False),))
    send_survey_time = models.TimeField()
    expire_after_hours = models.PositiveSmallIntegerField(default=12)

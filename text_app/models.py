from django.db import models
import uuid


# Create your models here.
class ResponseModel(models.Model):
    RESPONSE_CHOICES = (
        (1, 1),
        (2, 2),
    )

    id = models.UUIDField(default=uuid.uuid4(), primary_key=True)
    response = models.CharField(max_length=1, choices=RESPONSE_CHOICES)
    datetime = models.DateTimeField(auto_now=True)


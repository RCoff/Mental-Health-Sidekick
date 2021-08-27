from django.db import models
import uuid


# Create your models here.
class ResponseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4())
    response = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now=True)

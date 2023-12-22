import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    created_datetime = models.DateTimeField(auto_now_add=True, editable=False)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, editable=True, null=False)

    class Meta:
        abstract = True


class BaseChecklistTemplate(BaseModel):
    name = models.CharField(max_length=128, blank=False, editable=True, null=False)
    description = models.CharField(max_length=2048, blank=True, editable=True, null=True)

    class Meta:
        abstract = True


class BaseChecklistItemTemplate(BaseModel):
    text = models.CharField(max_length=256, blank=True, editable=True, null=False)

    class Meta:
        abstract = True

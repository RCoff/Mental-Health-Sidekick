from django.db import models
from django.contrib.auth import get_user_model

from .base import (
    BaseChecklistTemplate,
    BaseChecklistItemTemplate
)


class UserChecklistTemplate(BaseChecklistTemplate):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             editable=False, null=False)
    copied_from = models.UUIDField(null=True)


class UserChecklistItemTemplate(BaseChecklistItemTemplate):
    user_checklist_template = models.ForeignKey(UserChecklistTemplate,
                                                on_delete=models.CASCADE,
                                                editable=False, null=False)


class UserChecklist(BaseChecklistTemplate):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             editable=False, null=False)
    created_from = models.UUIDField(null=True)


class UserChecklistItem(BaseChecklistItemTemplate):
    user_checklist = models.ForeignKey(UserChecklist,
                                       on_delete=models.CASCADE,
                                       editable=False, null=False)
    status = models.BooleanField(default=False, editable=True, null=False)

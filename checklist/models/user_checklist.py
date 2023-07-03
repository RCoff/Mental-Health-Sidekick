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

    def add_item(self, text: str):
        UserChecklistItemTemplate.objects.create(
            text=text,
            user_checklist_template=self
        )


class UserChecklistItemTemplate(BaseChecklistItemTemplate):
    user_checklist_template = models.ForeignKey(UserChecklistTemplate,
                                                on_delete=models.CASCADE,
                                                editable=False, null=False)


class UserChecklist(BaseChecklistTemplate):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             editable=False, null=False)
    created_from = models.UUIDField(null=True)

    def add_item(self, text: str):
        UserChecklistItem.objects.create(
            text=text,
            user_checklist=self
        )


class UserChecklistItem(BaseChecklistItemTemplate):
    user_checklist = models.ForeignKey(UserChecklist,
                                       on_delete=models.CASCADE,
                                       editable=False, null=False)
    status = models.BooleanField(default=False, editable=True, null=False)

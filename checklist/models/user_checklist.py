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
                             editable=True, null=False)
    created_from = models.UUIDField(blank=True, editable=False, null=True)

    def add_item(self, text: str):
        return UserChecklistItem.objects.create(
            text=text,
            user_checklist=self
        )

    @property
    def item_count(self):
        return self.userchecklistitem_set.filter(deleted=False).count()

    @property
    def checked_item_count(self):
        return self.userchecklistitem_set.filter(deleted=False, status=True).count()


class UserChecklistItem(BaseChecklistItemTemplate):
    user_checklist = models.ForeignKey(UserChecklist,
                                       on_delete=models.CASCADE,
                                       editable=True, null=False)
    status = models.BooleanField(default=False, editable=True, null=False)

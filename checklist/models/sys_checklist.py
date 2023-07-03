from typing import Optional

from django.db import models

from .base import (
    BaseChecklistTemplate,
    BaseChecklistItemTemplate
)


class ChecklistTemplate(BaseChecklistTemplate):
    """ """

    def add_item(self, text: str):
        ChecklistItemTemplate.objects.create(
            text=text,
            checklist_template=self
        )


class ChecklistItemTemplate(BaseChecklistItemTemplate):
    checklist_template = models.ForeignKey(ChecklistTemplate,
                                           on_delete=models.CASCADE,
                                           editable=False, null=False)

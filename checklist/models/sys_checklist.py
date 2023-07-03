from django.db import models

from .base import (
    BaseChecklistTemplate,
    BaseChecklistItemTemplate
)


class ChecklistTemplate(BaseChecklistTemplate):
    """ """


class ChecklistItemTemplate(BaseChecklistItemTemplate):
    checklist_template = models.ForeignKey(ChecklistTemplate,
                                           on_delete=models.CASCADE,
                                           editable=False, null=False)

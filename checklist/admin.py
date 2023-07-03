from django.contrib import admin

from .models import (
    ChecklistTemplate,
    ChecklistItemTemplate,
    UserChecklistTemplate,
    UserChecklistItemTemplate,
    UserChecklist,
    UserChecklistItem
)


@admin.register(ChecklistTemplate)
class SystemChecklistTemplateAdmin(admin.ModelAdmin):
    """ """


@admin.register(ChecklistItemTemplate)
class SystemChecklistItemTemplateAdmin(admin.ModelAdmin):
    """ """


@admin.register(UserChecklistTemplate)
class UserChecklistTemplateAdmin(admin.ModelAdmin):
    """ """


@admin.register(UserChecklistItemTemplate)
class UserChecklistItemTemplateAdmin(admin.ModelAdmin):
    """ """


@admin.register(UserChecklist)
class UserChecklistAdmin(admin.ModelAdmin):
    """ """


@admin.register(UserChecklistItem)
class UserChecklistItemAdmin(admin.ModelAdmin):
    """ """

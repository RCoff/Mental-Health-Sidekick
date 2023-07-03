from uuid import uuid4

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from django.shortcuts import render

from .models import (
    UserChecklist,
    UserChecklistItem,
    UserChecklistTemplate
)


@require_GET
def get_user_checklists(request):
    user_checklists = UserChecklist.objects.filter(user=request.user)

    return render(request, template_name='all_checklists.html', context={'checklists': user_checklists})


@require_GET
def get_user_checklist_templates(request):
    pass


@require_GET
def get_user_checklist(request, checklist_id: uuid4):
    checklist_items = UserChecklistItem.objects.filter(deleted=False,
                                                       user_checklist__user=request.user,
                                                       user_checklist=checklist_id,
                                                       user_checklist__deleted=False)

    return render(request, template_name='checklist.html', context={'checklist_items': checklist_items})


@require_GET
def get_user_checklist_template(request, checklist_id: uuid4):
    pass

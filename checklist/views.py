from uuid import uuid4
import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_http_methods
from django.shortcuts import render
from django.views import View

from .models import (
    UserChecklist,
    UserChecklistItem,
    UserChecklistTemplate
)


@require_GET
def get_user_checklists(request):
    user_checklists = UserChecklist.objects.filter(user=request.user,
                                                   deleted=False) \
        .order_by('-modified_datetime')

    return render(request, template_name='all_checklists.html', context={'checklists': user_checklists})


@require_GET
def get_user_checklist_templates(request):
    pass


class UserChecklistView(View):
    def get(self, request, checklist_id: uuid4):
        checklist_name = UserChecklist.objects.values('name').get(deleted=False,
                                                                  user=request.user,
                                                                  id=checklist_id)['name']
        checklist_items = UserChecklistItem.objects.filter(deleted=False,
                                                           user_checklist__user=request.user,
                                                           user_checklist=checklist_id,
                                                           user_checklist__deleted=False)

        return render(request, template_name='user_checklist.html', context={'checklist_items': checklist_items,
                                                                             'checklist_name': checklist_name})


class UserChecklistItemView(View):
    def put(self, request, checklist_item_id: uuid4):
        status = json.loads(request.body).get('status')
        item = self._get_item(user=request.user, checklist_item_id=checklist_item_id)
        item.status = status
        item.save()

        return HttpResponse(status=201)

    def delete(self, request, checklist_item_id: uuid4):
        item = self._get_item(user=request.user, checklist_item_id=checklist_item_id)
        item.deleted = True
        item.save()

        return HttpResponse(status=202)

    @staticmethod
    def _get_item(user, checklist_item_id: uuid4):
        return UserChecklistItem.objects.get(user_checklist__user=user,
                                             id=checklist_item_id)


@require_GET
def get_user_checklist_template(request, checklist_id: uuid4):
    pass

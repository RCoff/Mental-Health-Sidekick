from typing import Optional
from uuid import uuid4
import json

from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views import View

from .utils import oai
from .models import (
    UserChecklist,
    UserChecklistItem,
    UserChecklistTemplate
)


@require_POST
def create_checklist(request):
    request_json = json.loads(request.body)
    prompt = request_json.get('prompt')

    if prompt is None:
        return JsonResponse({"message": "Request must include the 'prompt' parameter"}, status=400)

    checklist_list = oai.create_checklist(prompt)
    checklist_name = oai.create_checklist_name(prompt)

    new_checklist = UserChecklist.objects.create(user=request.user,
                                                 name=checklist_name)
    for item in checklist_list:
        new_checklist.add_item(text=item)
    new_checklist.save()

    return JsonResponse({"id": new_checklist.id}, status=201)


class Checklist(View):
    model = UserChecklist

    def get(self, request, checklist_id: Optional[uuid4] = None):
        user_checklists = self.model.objects.filter(user=request.user,
                                                    deleted=False) \
            .order_by('-modified_datetime')

        if not checklist_id:
            user_checklists = user_checklists \
                .annotate(item_count=Count('userchecklistitem')) \
                .annotate(checked_item_count=Count('userchecklistitem', filter=Q(userchecklistitem__status=True)))
            return JsonResponse({"checklists": list(user_checklists.values())}, status=200)
        else:
            checklist_name = user_checklists.values("name").get(id=checklist_id)["name"]
            checklist_items = UserChecklistItem.objects.filter(deleted=False,
                                                               user_checklist__user=request.user,
                                                               user_checklist=checklist_id,
                                                               user_checklist__deleted=False)
            return JsonResponse({"checklist_items": list(checklist_items.values()),
                                 "checklist_name": checklist_name}, status=200)

    def post(self, request):
        request_json = json.loads(request.body)
        name = request_json.get("name")

        if not name:
            return JsonResponse({"message": "Request must include a 'name' parameter that includes the checklist name"},
                                status=400)

        new_checklist = self.model.objects.create(user=request.user,
                                                  name=name)
        new_checklist.save()

        return JsonResponse({"id": new_checklist.id,
                             "name": new_checklist.name}, status=201)

    def delete(self, request, checklist_id: uuid4):
        update_model = self.model.objects.get(id=checklist_id)
        update_model.deleted = True
        update_model.save()

        return JsonResponse({"message": "SUCCESS"}, status=202)

    def put(self, request, checklist_id: uuid4):
        request_json = json.loads(request.body)
        name = request_json.get("name")

        update_model = self.model.objects.get(id=checklist_id,
                                              user=request.user)
        update_model.name = name
        update_model.save()

        return JsonResponse({"message": "SUCCESS"}, status=202)


class ChecklistItem(View):
    parent_model = UserChecklist
    model = UserChecklistItem

    def post(self, request, checklist_id: uuid4):
        request_json = json.loads(request.body)
        text = request_json.get('text')

        if not text:
            return JsonResponse({"message": "Request must include a 'text' parameter that includes the task name"},
                                status=400)

        self.parent_model.objects.get(id=checklist_id,
                                      user=request.user).add_item(text=text)

        return JsonResponse({"message": "SUCCESS"}, status=202)

    def put(self, request, item_id: uuid4):
        request_json = json.loads(request.body)
        text = request_json.get('text')

        if not text:
            return JsonResponse({"message": "Request must include a 'text' parameter that includes the task name"},
                                status=400)

        update_item = self.model.objects.get(id=item_id,
                                             user_checklist__user=request.user)
        update_item.text = text
        update_item.save()

        return JsonResponse({"message": "SUCCESS"}, status=202)

    def delete(self, request, item_id: uuid4):
        update_item = self.model.objects.get(id=item_id,
                                             user_checklist__user=request.user)
        update_item.deleted = True
        update_item.save()

        return JsonResponse({"message": "SUCCESS"}, status=202)

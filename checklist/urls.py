from django.urls import path

from . import views

urlpatterns = [
    path('', views.Checklist.as_view(), name='user-checklists'),
    path('<uuid:checklist_id>', views.Checklist.as_view(), name='user-checklist'),
    path('item/<uuid:checklist_item_id>', views.ChecklistItem.as_view(), name='user-checklist-item'),
    # path('template/', views.get_user_checklist_templates, name='user-checklist-templates'),
    # path('template/<uuid:checklist_id>', views.get_user_checklist_template, name='user-checklist-template'),
]

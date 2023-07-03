from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_user_checklists, name='user-checklists'),
    path('<uuid:checklist_id>', views.UserChecklistView.as_view(), name='user-checklist'),
    path('item/<uuid:checklist_item_id>', views.UserChecklistItemView.as_view(), name='user-checklist-item'),
    path('template/', views.get_user_checklist_templates, name='user-checklist-templates'),
    path('template/<uuid:checklist_id>', views.get_user_checklist_template, name='user-checklist-template'),
]

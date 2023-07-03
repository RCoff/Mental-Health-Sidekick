from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_user_checklists, name='user-checklists'),
    path('<uuid:checklist_id>', views.get_user_checklist, name='user-checklist'),
    path('template/', views.get_user_checklist_templates, name='user-checklist-templates'),
    path('template/<uuid:checklist_id>', views.get_user_checklist_template, name='user-checklist-template'),
]

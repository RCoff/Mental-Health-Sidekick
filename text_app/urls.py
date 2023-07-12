from django.urls import path, include
from rest_framework import routers

from . import views
from . import web_hooks

router = routers.DefaultRouter()
router.register(r'responses', views.ResponseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('message/', web_hooks.receive_message)
]

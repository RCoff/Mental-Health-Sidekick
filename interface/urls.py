from django.contrib import admin
from django.urls import path, include
from interface import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
]

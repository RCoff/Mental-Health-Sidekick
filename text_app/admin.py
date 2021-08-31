from django.contrib import admin
from . import models

# Register your models here
admin.site.register(models.ResponseModel)
admin.site.register(models.ActiveSurveyStore)
admin.site.register(models.UserPhoneNumber)
admin.site.register(models.Disorder)
admin.site.register(models.DailySymptoms)

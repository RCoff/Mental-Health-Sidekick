from rest_framework import serializers
from .models import ResponseModel


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseModel
        fields = ['id', 'response']

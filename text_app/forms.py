from django import forms
from . import models


class ResponseForm(forms.ModelForm):
    class Meta:
        model = models.ResponseModel
        fields = ['response', 'text_response']
        widgets = {
            'response': forms.Select(attrs={'class': 'form-control'}),
            'text_response': forms.Textarea(attrs={'class': 'form-control'})
        }

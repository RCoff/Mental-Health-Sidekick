from django import forms
from . import models


class ResponseForm(forms.ModelForm):
    class Meta:
        model = models.ResponseModel
        fields = ['mood_response', 'hours_slept', 'daily_weight', 'daily_symptoms', 'text_response']
        widgets = {
            'mood_response': forms.NumberInput(attrs={'type': 'range',
                                                      'class': 'form-range',
                                                      'min': -4,
                                                      'max': 4,
                                                      'step': 1,
                                                      'id': 'mood-range',
                                                      'list': 'mood-steps'}),
            'hours_slept': forms.NumberInput(attrs={'class': 'form-control'}),
            'daily_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'daily_symptoms': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'text_response': forms.Textarea(attrs={'class': 'form-control'})
        }

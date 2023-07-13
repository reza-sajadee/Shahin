from django import forms
from django.db import models
from .models import Dashboard



class CreateFormDashboard(forms.ModelForm):

    

    class Meta:
        model = Dashboard
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        
        
        self.fields['name'].label             ='نام را وارد کنید'

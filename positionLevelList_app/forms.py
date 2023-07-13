from django import forms
from django.db import models
from .models import PositionLevelList



class CreateFormPositionLevelList(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = PositionLevelList
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['positionLevelCode'].widget.attrs.update({'class': 'form-control'})
  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        self.fields['positionLevelCode'].label                   =' کد سطح سازمانی فرآیندی را وارد کنید'

        
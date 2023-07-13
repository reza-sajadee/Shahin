from django import forms
from django.db import models
from .models import PositionNameList



class CreateFormPositionNameList(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = PositionNameList
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['positionNameCode'].widget.attrs.update({'class': 'form-control'})
  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        self.fields['positionNameCode'].label       =' کد نام پست سازمانی را وارد کنید'

        
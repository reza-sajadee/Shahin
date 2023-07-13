
from django import forms
from django.db import models
from .models import Notifications 



class CreateFormNotifications(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = Notifications
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['personalStatus'].widget.attrs.update({'class': 'form-control'})
        self.fields['icon'].widget.attrs.update({'class': 'form-control'})
        self.fields['recivers'].widget.attrs.update({'class': 'form-control'})
       
        

        

        

        #لیبل توضیح 
        self.fields['title'].label    ='عنوان  را وارد کنید'
        self.fields['description'].label             ='توضیحات را انتخاب کنید'
        self.fields['status'].label      ='نوع اطلاعیه را انتخاب کنید'
        self.fields['personalStatus'].label      ='وضعیت اطلاعیه را انتخاب کنید'
        self.fields['icon'].label      =' آیکون را انتخاب کنید'
        self.fields['recivers'].label      ='گیرندگان را انتخاب کنید'
      
   
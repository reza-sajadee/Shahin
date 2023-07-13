from django import forms
from django.db import models
from .models import Event

from process_app.models import Group


class CreateFormEvent(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = Event
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
     
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        
        self.fields['is_active'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_deleted'].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['start'].widget.attrs.update({'class': 'form-control'})
        self.fields['end'].widget.attrs.update({'class': 'form-control'})
        
        

        #لیبل توضیح 
        
        self.fields['is_active'].label         =' آیا رویداد فعال است ؟'
        self.fields['is_deleted'].label         =' آیا رویداد پاک شده است ؟'
        self.fields['user'].label         ='کاربر را انتخاب کنید'
        self.fields['title'].label         ='عنوان را وارد کنید'
        self.fields['description'].label         ='توضیحات را وارد کنید'
        self.fields['start'].label         ='زمان شروع رویداد را وارد کنید'
        self.fields['end'].label         ='زمان پایان رویداد را وارد کنید'
        

  






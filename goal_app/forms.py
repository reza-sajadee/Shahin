from django import forms
from django.db import models
from .models import  Objective

from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
        

      
     
class CreateFormObjective(forms.ModelForm):

    class Meta:
        #نام مدل
        model = Objective
       
        #فیلد های نمایش داده شده در فرم
        
        fields  = '__all__'
   

     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['principle'].widget.attrs.update({'class': 'form-control'})
        self.fields['presppective'].widget.attrs.update({'class': 'form-control'})
        self.fields['goal'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['index'].widget.attrs.update({'class': 'form-control'})
        self.fields['trendIndex'].widget.attrs.update({'class': 'form-control'})
        self.fields['target'].widget.attrs.update({'class': 'form-control'})
        self.fields['currentSituation'].widget.attrs.update({'class': 'form-control'})
        self.fields['startLine'].widget.attrs.update({'class': 'form-control'})
        self.fields['deadLine'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': '3'})
        # self.fields['text'].widget.attrs.update({'class': 'form-control'})
        
        
     





 
        
        self.fields['principle'].label            =' نوع جلسه را انتخاب کنید'
        self.fields['presppective'].label            =' نوع جلسه را انتخاب کنید'
        self.fields['goal'].label            =' نوع جلسه را انتخاب کنید'
        self.fields['title'].label            =' نوع جلسه را انتخاب کنید'
        self.fields['index'].label            =' نوع جلسه را انتخاب کنید'
        self.fields['trendIndex'].label            =' نوع جلسه را انتخاب کنید'
        self.fields['target'].label            =' نوع جلسه را انتخاب کنید'
        self.fields['currentSituation'].label            =' نوع جلسه را انتخاب کنید'
        self.fields['startLine'].label            =' نوع جلسه را انتخاب کنید'
        self.fields['deadLine'].label            =' نوع جلسه را انتخاب کنید'
        self.fields['description'].label            =' نوع جلسه را انتخاب کنید'
       
        
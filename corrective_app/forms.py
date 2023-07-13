from django import forms
from django.db import models
from .models import CorrectiveAction

from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
        




class CreateFormCorrectiveAction(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = CorrectiveAction
        #فیلد های نمایش داده شده در فرم
        
        exclude  = ('demandantId' , 'vahed' , 'owner','deadLine' , 'effective')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['problem'].widget.attrs.update({'class': 'form-control '})
        self.fields['demandantVahed'].widget.attrs.update({'class': 'form-control '})
        #self.fields['demandantId'].widget.attrs.update({'class': 'form-control'})
        self.fields['standardRelated'].widget.attrs.update({'class': 'form-control '})
        self.fields['source'].widget.attrs.update({'class': 'form-control '})
  
        

        #لیبل توضیح 
        self.fields['problem'].label              ='نوع مسئله را انتخاب کنید'
        self.fields['demandantVahed'].label       ='   واحد درخواست کننده را را انتخاب کنید'
        #self.fields['demandantId'].label          ='  شماره درخواست را وارد کنید'
        self.fields['standardRelated'].label      ='  سیستم مربوطه را انتخاب کنید'
        self.fields['source'].label               ='  منشا بروز را  را انتخاب کنید'

        
   
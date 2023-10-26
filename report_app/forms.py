from django import forms
from django.db import models

from .models import Report , ReportActivityManager
from autocomplete import HTMXAutoComplete, widgets 
from organization_app.models import JobBank

from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
        


   
class CreateFormReportActivityManager(forms.ModelForm):

    class Meta:
        #نام مدل
        model = ReportActivityManager
       
        #فیلد های نمایش داده شده در فرم
        
        
        exclude = ('ReportRelated' , 'previousActivity' , 'nextActivity' ,'sender' ,'reciver' ,'status')
        
        



     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['deadLine'] = JalaliDateField(label=('deadLine'), # date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget # optional, to use default datepicker
        )

      

        
     

        
       



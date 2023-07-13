from django import forms
from django.db import models
from .models import EmployeeList



class CreateFormEmployeeList(forms.ModelForm):

    

    class Meta:
        model = EmployeeList
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs.update({'class': 'form-control'})
        self.fields['lastName'].widget.attrs.update({'class': 'form-control'})
        self.fields['idNumber'].widget.attrs.update({'class': 'form-control'})
        self.fields['employeeNumber'].widget.attrs.update({'class': 'form-control'})
        

        
        self.fields['firstName'].label                  ='نام را وارد کنید'
        self.fields['lastName'].label                   ='نام خانوادگی را وارد کنید'
        self.fields['idNumber'].label                   ='کد ملی را وارد کنید'
        self.fields['employeeNumber'].label             ='کد پرسنلی را وارد کنید'
        
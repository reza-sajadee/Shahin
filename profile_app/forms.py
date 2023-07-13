from django import forms
from django.db import models

from .models import Nahiye , Hoze , Group  ,Process



class CreateFormNahiye(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = Nahiye
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['nahiyeCode'].widget.attrs.update({'class': 'form-control'})
  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        self.fields['nahiyeCode'].label                   =' کد ناحیه فرآیندی را وارد کنید'

        
        


class CreateFormGroup(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = Group
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['groupCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['hozeCode'].widget.attrs.update({'class': 'form-control'})

  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        self.fields['groupCode'].label       =' کد  فرآیند را وارد کنید'
        self.fields['hozeCode'].label        ='  گروه فرآیندی را انتخاب کنید'
        

        
        

class CreateFormProcess(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = Process
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['processCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['groupCode'].widget.attrs.update({'class': 'form-control'})

  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        self.fields['processCode'].label       =' کد گروه فرآیندی را وارد کنید'
        self.fields['groupCode'].label        ='  حوزه فرآیندی را انتخاب کنید'
        

        
        


class CreateFormHoze(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = Hoze
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['hozeCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['nahiyeCode'].widget.attrs.update({'class': 'form-control'})

  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        self.fields['hozeCode'].label       =' کد حوزه فرآیندی را وارد کنید'
        self.fields['nahiyeCode'].label        ='  حوزه فرآیندی را انتخاب کنید'
        

        




from django import forms
from django.db import models
from .models import Committee 




class CreateFormCommittee(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = Committee
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
        exclude = ('members', )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['topic'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['mostanadGhanoni'].widget.attrs.update({'class': 'form-control'})
        self.fields['hoze'].widget.attrs.update({'class': 'form-control'})
        self.fields['typeComittee'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['head'].widget.attrs.update({'class': 'form-control'})
        self.fields['janeshinAval'].widget.attrs.update({'class': 'form-control'})
        self.fields['janeshinDovom'].widget.attrs.update({'class': 'form-control'})
        self.fields['dabir'].widget.attrs.update({'class': 'form-control'})
  
        

        #لیبل توضیح 
        self.fields['topic'].label                  ='سرفصل را انتخاب کنید'
        self.fields['title'].label         =' عنوان را وارد کنید'
        self.fields['mostanadGhanoni'].label                  ='مستند قانونی تشکیل جلسه را وارد کنید'
        self.fields['hoze'].label         =' حوزه مرتبط را انتخاب کنید را وارد کنید'
        self.fields['typeComittee'].label                  ='نوع کمیته را انتخاب کنید'
        
        self.fields['head'].label                  ='رئیس را وارد کنید'
        self.fields['janeshinAval'].label         ='   جانشین اول را انتخاب کنید'
        self.fields['janeshinDovom'].label                  ='جانشین دوم را انتخاب کنید'
        self.fields['dabir'].label         =' دبیر   را انتخاب کنید'

        
        

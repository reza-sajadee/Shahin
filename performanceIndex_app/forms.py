from django import forms
from django.db import models
from .models import  TextDataBase,BoolDataBase ,ConfirmationDataBase , SubjectPerformanceIndex,TopicPerformanceIndex,PerformanceIndex ,VariableDataBase ,PerformanceFormula ,PerformanceIndexActivityManager

from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
        




         
     
class CreateFormPerformanceIndex(forms.ModelForm):

    class Meta:
        #نام مدل
        model = PerformanceIndex
       
        #فیلد های نمایش داده شده در فرم
        
        exclude = ('document' , )
   






     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['codePerformanceIndex'].widget.attrs.update({'class': 'form-control'})
        self.fields['processRelated'].widget.attrs.update({'class': 'form-control'})
        self.fields['indexType'].widget.attrs.update({'class': 'form-control'})
        self.fields['reference'].widget.attrs.update({'class': 'form-control'})
        self.fields['standardRelated'].widget.attrs.update({'class': 'form-control'})
        self.fields['stackHolder'].widget.attrs.update({'class': 'form-control'})
     


 
        
        self.fields['title'].label                  =' عنوان را وارد کنید'
        self.fields['codePerformanceIndex'].label   =' کد را وارد کنید'
        self.fields['processRelated'].label         =' فرآیند مرتبط را انتخاب کنید'
        self.fields['indexType'].label              =' نوع معیار را انتخاب کنید'
        self.fields['reference'].label              =' مرجع را وارد کنید'
        self.fields['standardRelated'].label        =' استاندارد مرتبط را انتخاب کنید'
        self.fields['stackHolder'].label            =' ذینفعان را وارد کنید'
       
        
     
class CreateFormPerformanceFormula(forms.ModelForm):

    class Meta:
        #نام مدل
        model = PerformanceFormula
       
        #فیلد های نمایش داده شده در فرم
        
        exclude  = ('PerformanceFormula', 'variablesRelated')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        


        self.fields['performanceIndexRelated'].widget.attrs.update({'class': 'form-control' , 'disabled':''})
        self.fields['acceptableCriteria'].widget.attrs.update({'class': 'form-control'})
        self.fields['acceptableCondition'].widget.attrs.update({'class': 'form-control'})
        self.fields['cycle'].widget.attrs.update({'class': 'form-control'})
        self.fields['responsible'].widget.attrs.update({'class': 'form-control'})
        self.fields['metric'].widget.attrs.update({'class': 'form-control'})
        #self.fields['PerformanceFormula'].widget.attrs.update({'class': 'form-control'})
        
        


 
        
        self.fields['performanceIndexRelated'].label   =' معیار عملکردی مرتبط را انتخاب کنید'
        self.fields['acceptableCriteria'].label        =' مقدار معیار پذیرش را وارد کنید'
        self.fields['acceptableCondition'].label        =' شرط معیار پذیرش را وارد کنید'
        self.fields['cycle'].label                     =' دوره را انتخاب کنید'
        self.fields['responsible'].label               =' مسئول وارد کردن را انتخاب کنید'
        self.fields['metric'].label                    =' واحد را وارد کنید'
       # self.fields['PerformanceFormula'].label        =' فرمول شاخص را وارد کنید'
        
        
  
class CreateFormVariableDataBase(forms.ModelForm):

    class Meta:
        #نام مدل
        model = VariableDataBase
       
        #فیلد های نمایش داده شده در فرم
        
        fields  = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        






        self.fields['title'].widget.attrs.update({'class': 'form-control' , })
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': '3'})
        self.fields['code'].widget.attrs.update({'class': 'form-control'})
        self.fields['code'].widget.attrs.update({'disabled': ''})
        self.fields['responsible'].widget.attrs.update({'class': 'form-control'})
        
  
        #self.fields['PerformanceFormula'].widget.attrs.update({'class': 'form-control'})
        
        


 
        
        self.fields['title'].label   ='عنوان متغییر را وارد کنید'
        self.fields['description'].label        ='در صورت وجود توضیحات را وارد کنید'
        self.fields['code'].label        ='کد متغییر'
        self.fields['responsible'].label                     =' مسئول وارد کردن را انتخاب کنید'
        
        
       # self.fields['PerformanceFormula'].label        =' فرمول شاخص را وارد کنید'
        
        
  
from django import forms
from django.db import models

from .models import Nahiye , Hoze , Group  ,Process ,ProcessDocument ,ProcessDescription



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
        self.fields['ownerVahed'].widget.attrs.update({'class': 'form-control'})

  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        self.fields['processCode'].label       =' کد گروه فرآیندی را وارد کنید'
        self.fields['groupCode'].label        ='  حوزه فرآیندی را انتخاب کنید'
        self.fields['ownerVahed'].label        ='  مالک فرآیند را انتخاب کنید'

        
        


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
        

        



class CreateFormProcessDocument(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = ProcessDocument
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['process'].widget.attrs.update({'class': 'form-control'})
        self.fields['goalProcess'].widget.attrs.update({'class': 'form-control'})
        self.fields['driverProcess'].widget.attrs.update({'class': 'form-control'})
        self.fields['inputProcess'].widget.attrs.update({'class': 'form-control'})
        self.fields['fromProcess'].widget.attrs.update({'class': 'form-control'})
        self.fields['outputProcess'].widget.attrs.update({'class': 'form-control'})
        self.fields['toProcess'].widget.attrs.update({'class': 'form-control'})

  
        

        #لیبل توضیح 
        self.fields['process'].label                  ='فرآیند را انتخاب کنید'
        self.fields['goalProcess'].label       ='   هدف فرآیند را وارد کنید'
        self.fields['driverProcess'].label        ='   محرک فرآیند را وارد کنید'
        self.fields['inputProcess'].label                  ='عنوان را وارد کنید'
        self.fields['fromProcess'].label       ='    از فرآیند را وارد کنید'
        self.fields['outputProcess'].label        ='  خروجی فرآیندی را وارد کنید'
        self.fields['toProcess'].label        ='   به فرآیند را وارد کنید'
        


class CreateFormProcessDescription(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = ProcessDescription
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css

        self.fields['ProcessDocumentRelated'].widget.attrs.update({'class': 'form-control'})
        self.fields['activityDescription'].widget.attrs.update({'class': 'form-control'})
        self.fields['ownerActivity'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

  
        

        #لیبل توضیح 
        self.fields['ProcessDocumentRelated'].label                  ='سند فرآیند مرتبط را وارد کنید'
        self.fields['activityDescription'].label       ='  شرح فعالیت را وارد کنید'
        self.fields['ownerActivity'].label        ='   مسئول / مسئولان را وارد کنید'
        self.fields['description'].label        ='  توضیحات  را وارد کنید'
        

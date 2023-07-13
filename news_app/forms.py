from django import forms
from django.db import models
from .models import Categoriy ,News


class CreateFormNews(forms.ModelForm):



    class Meta:
        #نام مدل
        model = News
        #فیلد های نمایش داده شده در فرم
        fields = ['title','image','description','NewsCategoriy']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        



        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['NewsCategoriy'].widget.attrs.update({'class': 'form-control'})
        

        #لیبل توضیح 
        
        self.fields['title'].label         =' عنوان دسته بندی خبر را وارد کنید'
        self.fields['image'].label         =' عنوان دسته بندی خبر را وارد کنید'
        self.fields['description'].label         =' عنوان دسته بندی خبر را وارد کنید'
        self.fields['NewsCategoriy'].label         =' عنوان دسته بندی خبر را وارد کنید'
    

    

class CreateFormCategoriy(forms.ModelForm):



    class Meta:
        #نام مدل
        model = Categoriy
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        
        

        #لیبل توضیح 
        
        self.fields['title'].label         =' عنوان دسته بندی خبر را وارد کنید'
        
        
        
from django import forms
from django.db import models

from .models import Rade,Hoze,Bakhsh,Daste,SatheVahed,TypePostSazmani,Vahed,SathPost ,IndexMahaleKhedmat , JobBank , Post





class CreateFormRade(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = Rade
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['radeCode'].widget.attrs.update({'class': 'form-control'})
  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        self.fields['radeCode'].label       =' کد نام پست سازمانی را وارد کنید'

        




class CreateFormDaste(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = Daste
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['dasteCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['bakhsh'].widget.attrs.update({'class': 'form-control'})

  
        

        #لیبل توضیح 
        self.fields['title'].label             ='عنوان را وارد کنید'
        self.fields['dasteCode'].label    =' کد  دسته سازمانی را وارد کنید'
        self.fields['bakhsh'].label      ='  بخش سازمانی را انتخاب کنید'
        
        
        


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
  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        self.fields['hozeCode'].label       =' کد حوزه سازمانی را وارد کنید'




class CreateFormSatheVahed(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = SatheVahed
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['satheVahedCode'].widget.attrs.update({'class': 'form-control'})
  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        self.fields['satheVahedCode'].label       =' کد سطح سازمانی را وارد کنید'




class CreateFormTypePostSazmani(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = TypePostSazmani
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['typePostSazmaniCode'].widget.attrs.update({'class': 'form-control'})
  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        self.fields['typePostSazmaniCode'].label       =' کد  پست سازمانی را وارد کنید'




class CreateFormBakhsh(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = Bakhsh
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['bakhshCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['hoze'].widget.attrs.update({'class': 'form-control'})

  
        

        #لیبل توضیح 
        self.fields['title'].label             ='عنوان را وارد کنید'
        self.fields['bakhshCode'].label    =' کد  بخش سازمانی را وارد کنید'
        self.fields['hoze'].label      ='  حوزه سازمانی را انتخاب کنید'
        

        
        

class CreateFormVahed(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = Vahed
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
      
        self.fields['vahedMafogh'].widget.attrs.update({'class': 'form-control'})
        self.fields['satheVahed'].widget.attrs.update({'class': 'form-control'})
        self.fields['typePostSazmani'].widget.attrs.update({'class': 'form-control'})
        self.fields['daste'].widget.attrs.update({'class': 'form-control'})
        self.fields['bakhsh'].widget.attrs.update({'class': 'form-control'})
        self.fields['hoze'].widget.attrs.update({'class': 'form-control'})
        
  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
       
        self.fields['vahedMafogh'].label       =' کد  پست سازمانی مافوق را وارد کنید'
        self.fields['satheVahed'].label                  ='عنوان را وارد کنید'
        self.fields['typePostSazmani'].label       =' کد نام پست سازمانی را وارد کنید'
        self.fields['daste'].label                  ='عنوان را وارد کنید'
        self.fields['bakhsh'].label       =' کد نام پست سازمانی را وارد کنید'
        self.fields['hoze'].label       =' کد نام پست سازمانی را وارد کنید'
        



class CreateFormSathPost(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = SathPost
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['sathPostCode'].widget.attrs.update({'class': 'form-control'})
        

        #لیبل توضیح 
        self.fields['title'].label             ='عنوان را وارد کنید'
        self.fields['sathPostCode'].label    =' کد سطح پست سازمانی را وارد کنید'
        
        

class CreateFormIndexMahaleKhedmat(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = IndexMahaleKhedmat
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['indexCode'].widget.attrs.update({'class': 'form-control'})
  
        

        #لیبل توضیح 
        self.fields['title'].label                   ='عنوان را وارد کنید'
        self.fields['indexCode'].label               =' ایندکس محل خدمت را وارد کنید'



class CreateFormJobBank(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = JobBank
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['jobTitle'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahed'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahedMafogh'].widget.attrs.update({'class': 'form-control'})
        self.fields['typePostSazmani'].widget.attrs.update({'class': 'form-control'})
        self.fields['typePostSazmaniMafogh'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile'].widget.attrs.update({'class': 'form-control'})
        self.fields['counter'].widget.attrs.update({'class': 'form-control'})
        
        
        
        
      





        #لیبل توضیح 
        self.fields['jobTitle'].label               =' شمارنده را وارد کنید'
        self.fields['vahed'].label                   ='واحد را انتخاب کنید'
        self.fields['vahedMafogh'].label               =' واحد سازمانی مافوق را وارد کنید'
        self.fields['typePostSazmani'].label               =' نوع پست سازمانی را وارد کنید'
        self.fields['typePostSazmaniMafogh'].label               =' نوع پست سازمانی مافوق را وارد کنید'
        self.fields['profile'].label               =' کارمند را انتخاب کنید'
        self.fields['counter'].label               =' شمارنده را وارد کنید'
        
        
        


    

class CreateFormPost(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = Post
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahed'].widget.attrs.update({'class': 'form-control'})
        self.fields['SathPost'].widget.attrs.update({'class': 'form-control'})
        self.fields['zarfiyateMojaz'].widget.attrs.update({'class': 'form-control'})
        self.fields['janamayiFeli'].widget.attrs.update({'class': 'form-control'})
        self.fields['indexMahaleKhedmat'].widget.attrs.update({'class': 'form-control'})
        self.fields['RadePostSazmani'].widget.attrs.update({'class': 'form-control'})
        self.fields['postMafogh'].widget.attrs.update({'class': 'form-control'})
        
  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        self.fields['vahed'].label       =' کد  واحد سازمانی را وارد کنید'
        self.fields['SathPost'].label       =' سطح  پست سازمانی  را وارد کنید'
        self.fields['zarfiyateMojaz'].label                  ='ظرفیت مجاز را وارد کنید'
        self.fields['janamayiFeli'].label       ='    جانمایی فعلی را وارد کنید'
        self.fields['indexMahaleKhedmat'].label                  ='ایندکس محل خدمت را وارد کنید'
        self.fields['RadePostSazmani'].label       =' رده  پست سازمانی را وارد کنید'
        self.fields['postMafogh'].label       =' کد  پست مافوق را وارد کنید'
        


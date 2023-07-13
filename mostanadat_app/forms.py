from django import forms
from django.db import models
from .models import MostanadatDakheli ,TypeMadrak , MostanadatKhareji ,MostanadatDakheliChange ,RecordDataBase
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime


class CreateFormMostanadatDakheliChange(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = MostanadatDakheliChange
        #فیلد های نمایش داده شده در فرم
        
        exclude  = ('demandantProfile' , 'vahedRelated' , 'deadLine' , 'description')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['problem'].widget.attrs.update({'class': 'form-control'})
        
        
        self.fields['documentRelated'].widget.attrs.update({'class': 'form-control'})
        
        
        
  
        

        #لیبل توضیح 
        self.fields['problem'].label              ='نوع مسئله را انتخاب کنید'
        
        self.fields['documentRelated'].label      ='  سند مربوطه را انتخاب کنید'
        
        
        

        


class CreateFormMostanadatDakheli(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = MostanadatDakheli
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
        exclude = ('outdated',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['dakheliSanadCode'].widget.attrs.update({'class': 'form-control'})
       
        self.fields['versionNumber'].widget.attrs.update({'class': 'form-control'})
        self.fields['tabaghbandi'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahedMotevaliCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahedTaeidCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahedTasvibCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['typeMadrakCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['systemMortabetCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahedMortabetCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['molahezat'].widget.attrs.update({'class': 'form-control'})



        

        #لیبل توضیح 
        self.fields['title'].label      ='عنوان  را وارد کنید'
        self.fields['dakheliSanadCode'].label      =' کد سند داخلی را وارد کنید'
    
        self.fields['tabaghbandi'].label      ='طبقه بندی  را انتخاب کنید'
        self.fields['versionNumber'].label      ='شماره ورژن   را انتخاب کنید'
        self.fields['vahedMotevaliCode'].label      ='واحد متولی  را انتخاب کنید'
        self.fields['vahedTaeidCode'].label      ='واحد تایید کننده  را انتخاب کنید'
        self.fields['vahedTasvibCode'].label      ='واحد تصویب کننده  را انتخاب کنید'
        self.fields['typeMadrakCode'].label      ='نوع مدرک  را انتخاب کنید'
        self.fields['systemMortabetCode'].label      ='سیستم مرتبط را انتخاب کنید'
        self.fields['vahedMortabetCode'].label      ='واحد مرتبط را  انتخاب کنید'
        self.fields['molahezat'].label      ='ملاحظات را وارد نمایید'
        

class CreateFormRecordDataBase(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = RecordDataBase
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
        exclude = ('outdated',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['recordCode'].widget.attrs.update({'class': 'form-control'})
       
        self.fields['postKeeper'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahedKeeper'].widget.attrs.update({'class': 'form-control'})
        self.fields['privacy'].widget.attrs.update({'class': 'form-control'})
        self.fields['typeKeeping'].widget.attrs.update({'class': 'form-control'})
        self.fields['determine'].widget.attrs.update({'class': 'form-control'})
        self.fields['jariY'].widget.attrs.update({'class': 'form-control'})
        self.fields['jariM'].widget.attrs.update({'class': 'form-control'})
        self.fields['rakedY'].widget.attrs.update({'class': 'form-control'})
        self.fields['rakedM'].widget.attrs.update({'class': 'form-control'})




        

        #لیبل توضیح 
        self.fields['title'].label      ='عنوان  را وارد کنید'
        self.fields['recordCode'].label      =' کد سابقه  را وارد کنید'
    
        self.fields['postKeeper'].label      ='طبقه بندی  را انتخاب کنید'
        self.fields['vahedKeeper'].label      ='شماره ورژن   را انتخاب کنید'
        self.fields['privacy'].label      ='واحد متولی  را انتخاب کنید'
        self.fields['typeKeeping'].label      ='واحد تایید کننده  را انتخاب کنید'
        self.fields['determine'].label      ='واحد تصویب کننده  را انتخاب کنید'
        self.fields['jariY'].label      ='نوع مدرک  را انتخاب کنید'
        self.fields['jariM'].label      ='سیستم مرتبط را انتخاب کنید'
        self.fields['rakedY'].label      ='نوع مدرک  را انتخاب کنید'
        self.fields['rakedM'].label      ='سیستم مرتبط را انتخاب کنید'

        


class ViewFormMostanadatDakheli(forms.ModelForm):



    class Meta:
        #نام مدل
        model = MostanadatDakheli
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['updated_at'] = JalaliDateField(label=('updated_at'), widget=AdminJalaliDateWidget )
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['dakheliSanadCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['versionNumber'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['tabaghbandi'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahedMotevaliCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahedTaeidCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahedTasvibCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['typeMadrakCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['systemMortabetCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahedMortabetCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['molahezat'].widget.attrs.update({'class': 'form-control'})
        

        

        

        #لیبل توضیح 
        self.fields['title'].label      ='عنوان  را وارد کنید'
        self.fields['dakheliSanadCode'].label      =' کد سند داخلی را وارد کنید'
        self.fields['versionNumber'].label      ='شماره نسخه  را وارد کنید'
        self.fields['tabaghbandi'].label      ='طبقه بندی  را انتخاب کنید'
        self.fields['vahedMotevaliCode'].label      ='واحد متولی  را انتخاب کنید'
        self.fields['vahedTaeidCode'].label      ='واحد تاوید کننده  را انتخاب کنید'
        self.fields['vahedTasvibCode'].label      ='واحد تصویب کننده  را انتخاب کنید'
        self.fields['typeMadrakCode'].label      ='نوع مدرک  را انتخاب کنید'
        self.fields['systemMortabetCode'].label      ='سیستم مرتبط را انتخاب کنید'
        self.fields['vahedMortabetCode'].label      ='واحد مرتبط را  انتخاب کنید'
        self.fields['molahezat'].label      ='ملاحظات را وارد نمایید'
            


class ViewFormMostanadatKhareji(forms.ModelForm):



    class Meta:
        #نام مدل
        model = MostanadatKhareji
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['updated_at'] = JalaliDateField(label=('updated_at'), widget=AdminJalaliDateWidget )
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['kharejiSanadCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['processCode'].widget.attrs.update({'class': 'form-control'})
        
        
        self.fields['versionNumber'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['refrenceName'].widget.attrs.update({'class': 'form-control'})
        self.fields['expiredDate'].widget.attrs.update({'class': 'form-control'})
        self.fields['postmasolUpdate'].widget.attrs.update({'class': 'form-control'})
        self.fields['updatePeriod'].widget.attrs.update({'class': 'form-control'})
        self.fields['tozihat'].widget.attrs.update({'class': 'form-control'})
        

        

        

        #لیبل توضیح 
        self.fields['title'].label      ='عنوان  را وارد کنید'
        self.fields['kharejiSanadCode'].label      =' کد سند داخلی را وارد کنید'
        self.fields['processCode'].label      ='شماره نسخه  را وارد کنید'
        
        self.fields['versionNumber'].label      ='واحد متولی  را انتخاب کنید'
        
        self.fields['refrenceName'].label      ='واحد تصویب کننده  را انتخاب کنید'
        self.fields['expiredDate'].label      ='نوع مدرک  را انتخاب کنید'
        self.fields['postmasolUpdate'].label      ='سیستم مرتبط را انتخاب کنید'
        self.fields['updatePeriod'].label      ='واحد مرتبط را  انتخاب کنید'
        self.fields['tozihat'].label      ='ملاحظات را وارد نمایید'
            

        


class CreateFormTypeMadrak(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = TypeMadrak
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['typeMadrakCode'].widget.attrs.update({'class': 'form-control'})
  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        self.fields['typeMadrakCode'].label         =' کد نوع مدرک را وارد کنید'

        
        


class CreateFormMostanadatKhareji(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = MostanadatKhareji
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['kharejiSanadCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['processCode'].widget.attrs.update({'class': 'form-control'})
        
        
        self.fields['versionNumber'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['refrenceName'].widget.attrs.update({'class': 'form-control'})
        self.fields['expiredDate'].widget.attrs.update({'class': 'form-control'})
        self.fields['postmasolUpdate'].widget.attrs.update({'class': 'form-control'})
        self.fields['updatePeriod'].widget.attrs.update({'class': 'form-control'})
        self.fields['tozihat'].widget.attrs.update({'class': 'form-control'})


        

        

        #لیبل توضیح 
        self.fields['title'].label      ='عنوان  را وارد کنید'
        self.fields['kharejiSanadCode'].label      =' کد سند خارجی را وارد کنید'
        self.fields['processCode'].label      ='کد فرآیند را انتخاب کنید'
        
        self.fields['versionNumber'].label      ='شماره نسخه را وارد کنید'
        
        self.fields['refrenceName'].label      ='نام مرجع را وارد نمایید'
        self.fields['expiredDate'].label      ='تاریخ منسوخ شدن را انتخاب نمایید'
        self.fields['postmasolUpdate'].label      ='پست مسئول به روزرسانی را انتخاب نمایید'
        self.fields['updatePeriod'].label      ='دوره به روز رسانی را وارد نمایید'
        self.fields['tozihat'].label      ='ملاحظات را وارد نمایید'
        

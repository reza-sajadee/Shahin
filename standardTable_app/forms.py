from django import forms
from django.db import models
from .models import Standard ,StandardReferenceRelease



class CreateFormStandard(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = Standard
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['standardNumber'].widget.attrs.update({'class': 'form-control'})
        self.fields['standardTitlePersian'].widget.attrs.update({'class': 'form-control'})
        self.fields['standardTitleEnglish'].widget.attrs.update({'class': 'form-control'})
        self.fields['namad'].widget.attrs.update({'class': 'form-control'})
        self.fields['vaziyatEjra'].widget.attrs.update({'class': 'form-control'})
        self.fields['shamsiReleaseDate'].widget.attrs.update({'class': 'form-control'})
        self.fields['miladiReleaseDate'].widget.attrs.update({'class': 'form-control'})
        self.fields['tajdidNazarNumber'].widget.attrs.update({'class': 'form-control'})
        self.fields['refrerence'].widget.attrs.update({'class': 'form-control'})
        self.fields['language'].widget.attrs.update({'class': 'form-control'})
        self.fields['typeStandard'].widget.attrs.update({'class': 'form-control'})
        self.fields['geoDomainStandard'].widget.attrs.update({'class': 'form-control'})
        self.fields['internationalStandardReference'].widget.attrs.update({'class': 'form-control'})
        self.fields['internationalStandardReferenceNumber'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahedMotevaliCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahedMortabetCode'].widget.attrs.update({'class': 'form-control'})

        

        

        #لیبل توضیح 
        self.fields['standardNumber'].label      ='شماره استاندارد را وارد کنید'
        self.fields['standardTitlePersian'].label      ='عنوان فارسی را وارد کنید'
        self.fields['standardTitleEnglish'].label      ='عنوان انگلیسی را وارد کنید'
        self.fields['namad'].label      ='نماد را وارد کنید'
        self.fields['vaziyatEjra'].label      ='وضعیت اجرا را انتخاب کنید'
        self.fields['shamsiReleaseDate'].label      ='تاریخ انتشار (شمسی) را وارد کنید'
        self.fields['miladiReleaseDate'].label      ='تاریخ انتشار(میلادی) را وارد کنید'
        self.fields['tajdidNazarNumber'].label      ='شماره تجدید نظر را وارد کنید'
        self.fields['refrerence'].label      ='مرجع را انتخاب کنید'
        self.fields['language'].label      ='زبان را انتخاب کنید'
        self.fields['typeStandard'].label      ='نوع استاندارد را وارد کنید'
        self.fields['geoDomainStandard'].label      ='محدوده جقرافیایی را انتخاب کنید'
        self.fields['internationalStandardReference'].label      ='مرجع استاندارد بین المللی را وارد کنید'
        self.fields['internationalStandardReferenceNumber'].label      ='شماره مرجع مرجع را وارد کنید'
        self.fields['vahedMotevaliCode'].label      ='واحد های متولی را انتخاب کنید'
        self.fields['vahedMortabetCode'].label      ='.احد های مرتبط را انتخاب کنید'

        

        


class CreateFormStandardReferenceRelease(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = StandardReferenceRelease
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['persianReferenceName'].widget.attrs.update({'class': 'form-control'})
        self.fields['englishReferenceName'].widget.attrs.update({'class': 'form-control'})
        self.fields['namad'].widget.attrs.update({'class': 'form-control'})
        self.fields['website'].widget.attrs.update({'class': 'form-control'})
        self.fields['phoneNumber'].widget.attrs.update({'class': 'form-control'})



        #لیبل توضیح 
        self.fields['persianReferenceName'].label      ='نام فارسی استاندارد مرجع را وارد کنید'
        self.fields['englishReferenceName'].label      ='نام انگلیسی استاندارد مرجع را وارد کنید'
        self.fields['namad'].label                     ='نماد استاندارد  مرجع را وارد کنید'
        self.fields['website'].label                   ='وب سایت استاندارد مرجع را وارد کنید'
        self.fields['phoneNumber'].label               ='شماره تماس استاندارد مرجع را وارد کنید'
        
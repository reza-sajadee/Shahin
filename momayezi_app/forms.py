from django import forms
from django.db import models
from .models import TypeMomayezi ,ReportMomayezi , ForsatBehbod ,NoghatGhovat ,AdamEntebagh ,CalenderMomayezi ,RoleMomayezi  , MomayeziTeam ,MomayeziActivityManager  , CheckListMomayezi , MomayeziTeamRequest ,QuestionMomayeziList

from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

class CreateFormReportMomayezi(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = ReportMomayezi
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['reportMomayeziCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahedCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['typeMomayeziCode'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['standardCode'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['teamMomayezi'].widget.attrs.update({'class': 'form-control'})
        

        

        

        #لیبل توضیح 
        self.fields['reportMomayeziCode'].label    ='کد گزارش ممیزی  را وارد کنید'
        self.fields['vahedCode'].label             ='واحد ممیزی را انتخاب کنید'
        self.fields['typeMomayeziCode'].label      ='نوع ممیزی را انتخاب کنید'
        self.fields['standardCode'].label          ='کد استاندارد را وارد کنید'
        
        self.fields['teamMomayezi'].label          ="تیم ممیزی را وارد نمایید"
        

        

        


class CreateFormTypeMomayezi(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = TypeMomayezi
        #فیلد های نمایش داده شده در فرم
      
        exclude = ('step',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['modir'].widget.attrs.update({'class': 'form-control'})
  
        

        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        
        self.fields['modir'].label         ='  مدیر بهبود را انتخاب کنید'

        
        


class CreateFormForsatBehbod(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = ForsatBehbod
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['reportMomayeziCode'].widget.attrs.update({'class': 'form-control'})
  
        

        #لیبل توضیح 
        self.fields['title'].label                      ='عنوان را وارد کنید'
        self.fields['reportMomayeziCode'].label         ='گزارش ممیزی را انتخاب نمایید'

        
        
class CreateFormNoghatGhovat(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = ForsatBehbod
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['reportMomayeziCode'].widget.attrs.update({'class': 'form-control'})
  
        

        #لیبل توضیح 
        self.fields['title'].label                      ='عنوان را وارد کنید'
        self.fields['reportMomayeziCode'].label               ='گزارش ممیزی را انتخاب نمایید'

        
        

class CreateFormAdamEntebagh(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = AdamEntebagh
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['reportMomayeziCode'].widget.attrs.update({'class': 'form-control'})
        self.fields['bandStandard'].widget.attrs.update({'class': 'form-control'})
  
        

        #لیبل توضیح 
        self.fields['title'].label                      ='عنوان را وارد کنید'
        self.fields['reportMomayeziCode'].label         ='گزارش ممیزی را انتخاب نمایید'
        self.fields['bandStandard'].label               ='بند استاندارد را وارد نمایید'

        
        
class CreateFormCalenderMomayezi(forms.ModelForm):

    class Meta:
        #نام مدل
        model = CalenderMomayezi
       
        #فیلد های نمایش داده شده در فرم
        
        #fields = '__all__'
        exclude = ('activity','typeMomayezi')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dateMomayezi'] = JalaliDateField(label=('dateMomayezi'), widget=AdminJalaliDateWidget )
        #کلاس های css
      
        #self.fields['dateMomayezi'].widget.attrs.update({'class': 'form-control jalali_date-date hasDatepicker'})
        self.fields['dateMomayezi'].widget.attrs.update({'class': 'jalali_date-date'})
        self.fields['vahedMomayezi'].widget.attrs.update({'class': 'form-control'})
        self.fields['timeDuration'].widget.attrs.update({'class': 'form-control js-time-picker'})
        self.fields['timeStart'].widget.attrs.update({'class': 'form-control js-time-picker-start'})
        self.fields['teamMomayezi'].widget.attrs.update({'class': 'form-control'})
        self.fields['systemMomayezi'].widget.attrs.update({'class': 'form-control'})
        self.fields['bandMomayezi'].widget.attrs.update({'class': 'form-control'})
        #self.fields['typeMomayezi'].widget.attrs.update({'class': 'form-control'})

        

    
        #self.fields['playerCode'].queryset = models.playerCode.objects.filter(playerCode__icontains="1")
  
        

        #لیبل توضیح 
        
        self.fields['dateMomayezi'].label                  ='تاریخ ممیزی  را انتخاب کنید'
        self.fields['vahedMomayezi'].label                  ='واحد ممیزی  را انتخاب کنید'
        self.fields['timeStart'].label                  ='زمان شروع ممیزی  را انتخاب کنید'
        self.fields['timeDuration'].label                  ='مدت زمان  را انتخاب کنید'
        self.fields['teamMomayezi'].label                  ='تیم ممیزی  را وارد کنید'
        self.fields['systemMomayezi'].label                  ='سیستم ممیزی را وارد کنید'
        self.fields['bandMomayezi'].label                  ='بند های را وارد کنید'
        #self.fields['typeMomayezi'].label                  =' نوع ممیزی را انتخاب کنید'
        
        
       
        
class CreateFormRoleMomayezi(forms.ModelForm):

    class Meta:
        #نام مدل
        model = RoleMomayezi
       
        #فیلد های نمایش داده شده در فرم
        
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #کلاس های css
      
       
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        


    
        #self.fields['playerCode'].queryset = models.playerCode.objects.filter(playerCode__icontains="1")
  
        

        #لیبل توضیح 
        
        self.fields['title'].label                  =' عنوان نقش ممیزی  را وارد کنید'
        
        
        
class CreateFormMomayeziTeam(forms.ModelForm):

    class Meta:
        #نام مدل
        model = MomayeziTeam
       
        #فیلد های نمایش داده شده در فرم
        
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #کلاس های css
      
       
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['typeMomayeziRelated'].widget.attrs.update({'class': 'form-control'})
        self.fields['memberMomayezi'].widget.attrs.update({'class': 'form-control'})
        self.fields['standardRelated'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahedMomayezi'].widget.attrs.update({'class': 'form-control'})
        self.fields['sarMomayez'].widget.attrs.update({'class': 'form-control'})


    
        #self.fields['playerCode'].queryset = models.playerCode.objects.filter(playerCode__icontains="1")
  
        

        #لیبل توضیح 
        
        self.fields['title'].label                  =' عنوان تیم   را وارد کنید'
        self.fields['typeMomayeziRelated'].label                  =' نوبت ممیزی را انتخاب کنید'
        self.fields['memberMomayezi'].label                  =' عضو ممیز   را انتخاب کنید'
        self.fields['standardRelated'].label                  =' استاندارد   را انتخاب کنید'
        self.fields['vahedMomayezi'].label                  =' واحد   را انتخاب کنید'
        self.fields['sarMomayez'].label                  =' سرممیز   را انتخاب کنید'
        
    
     
        
class CreateMomayeziTeamRequest(forms.ModelForm):

    class Meta:
        #نام مدل
        model = MomayeziTeamRequest
       
        #فیلد های نمایش داده شده در فرم
        
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #کلاس های css
      

        self.fields['memberMomayezi'].widget.attrs.update({'class': 'form-control'})
        self.fields['sabegheYear'].widget.attrs.update({'class': 'form-control'})
        self.fields['document'].widget.attrs.update({'class': 'form-control'})

        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        


    
        #self.fields['playerCode'].queryset = models.playerCode.objects.filter(playerCode__icontains="1")
  
        

        #لیبل توضیح 
        
        
   
        self.fields['memberMomayezi'].label                  =' عضو ممیز   را وارد کنید'

        self.fields['sabegheYear'].label                  =' سابقه   را وارد کنید'
        
        


class CreateFormMomayeziActivityManager(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = MomayeziActivityManager
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['sender'].widget.attrs.update({'class': 'form-control'})
        self.fields['reciver'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['activity'].widget.attrs.update({'class': 'form-control'})
        self.fields['team'].widget.attrs.update({'class': 'form-control'})
        self.fields['previousActivity'].widget.attrs.update({'class': 'form-control'})
        self.fields['nextActivity'].widget.attrs.update({'class': 'form-control'})
        
  
        






        #لیبل توضیح 
        self.fields['sender'].label              =' فرستنده  ممیزی را انتخاب کنید'
        self.fields['reciver'].label             =' گیرنده فعالیت ممیزی را انتخاب کنید'
        self.fields['status'].label              =' وضعیت فعالیت ممیزی را انتخاب کنید'
        self.fields['activity'].label            =' نوع فعالیت ممیزی را انتخاب کنید'
        self.fields['team'].label                =' تیم فعالیت ممیزی را انتخاب کنید'
        self.fields['previousActivity'].label    =' فعالیت ممیزی قبلی را انتخاب کنید'
        self.fields['nextActivity'].label        =' فعالیت ممیزی بعدی را انتخاب کنید'
        


class CreateFormCheckListMomayezi(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = CheckListMomayezi
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'rows': '5'})
        self.fields['activity'].widget.attrs.update({'class': 'form-control'})
        self.fields['observed'].widget.attrs.update({'class': 'form-control'})
        self.fields['observed'].widget.attrs.update({'rows': '5'})
        self.fields['result'].widget.attrs.update({'class': 'form-control'})
        self.fields['question'].widget.attrs.update({'class': 'form-control'})
        

        #لیبل توضیح 
        self.fields['title'].label             =' فرستنده  ممیزی را انتخاب کنید'
        self.fields['activity'].label          =' گیرنده فعالیت ممیزی را انتخاب کنید'
        self.fields['observed'].label          =' وضعیت فعالیت ممیزی را انتخاب کنید'
        self.fields['result'].label            =' نوع فعالیت ممیزی را انتخاب کنید'
        self.fields['question'].label            ='  سوال ممیزی را انتخاب کنید'
        

class CreateFormQuestionMomayeziList(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = QuestionMomayeziList
        #فیلد های نمایش داده شده در فرم
        exclude = ['standardQuestion' ,'requirementStandardQuestion' ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['vahedQuestion'].widget.attrs.update({'class': 'form-control'})
        self.fields['question'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': '5'})
        
        

        







        #لیبل توضیح 
        self.fields['vahedQuestion'].label             =' واحد  ممیزی را انتخاب کنید'
        self.fields['question'].label          =' سوال  ممیزی را وارد کنید'
        self.fields['description'].label          ='   توضیحات سوال را وارد کنید'
        


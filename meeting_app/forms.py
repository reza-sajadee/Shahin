from django import forms
from django.db import models
from .models import  TextDataBase,BoolDataBase ,ConfirmationDataBase ,MeetingProfile  , MeetingDate , Meeting , MeetingInvitation , MeetingAgenda , MeetingEnactment

from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
        




         
     
class CreateFormMeetingProfile(forms.ModelForm):

    class Meta:
        #نام مدل
        model = MeetingProfile
       
        #فیلد های نمایش داده شده در فرم
        
        fields  = '__all__'
   

     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        self.fields['meetingType'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['responsible'].widget.attrs.update({'class': 'form-control'})
        self.fields['manager'].widget.attrs.update({'class': 'form-control'})
        self.fields['firstSuccessor'].widget.attrs.update({'class': 'form-control'})
        self.fields['secondSuccessor'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].widget.attrs.update({'rows': '3'})
        
     





 
        
        self.fields['meetingType'].label            =' نوع جلسه را انتخاب کنید'
        self.fields['title'].label                  =' عنوان جلسه را وارد کنید'
        self.fields['responsible'].label            =' دبیر جلسه را انتخاب کنید'
        self.fields['manager'].label            =' مدیر جلسه را انتخاب کنید'
        self.fields['firstSuccessor'].label            =' جانشین اول جلسه را انتخاب کنید'
        self.fields['secondSuccessor'].label            =' جانشین دوم جلسه را انتخاب کنید'
    
        self.fields['text'].label                   ='توضیحات  را وارد کنید'
        
        
     
class CreateFormMeeting(forms.ModelForm):

    class Meta:
        #نام مدل
        model = Meeting
       
        #فیلد های نمایش داده شده در فرم
        
     
        fields = '__all__'

     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        self.fields['meetingProfileRelated'].widget =  forms.HiddenInput()
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': '3'})
        
     





 
        
        
        self.fields['title'].label                  =' عنوان جلسه را وارد کنید'
        
    
        self.fields['description'].label                   ='توضیحات  را وارد کنید'
        
        
     
class CreateFormMeetingDate(forms.ModelForm):

    class Meta:
        #نام مدل
        model = MeetingDate
       
        #فیلد های نمایش داده شده در فرم
        
        fields  = '__all__'
        

     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meetingDate'] = JalaliDateField(label=('meetingDate'), widget=AdminJalaliDateWidget )

        self.fields['meetingDate'].widget.attrs.update({'class': 'form-control'})
        self.fields['meetingTime'].widget.attrs.update({'class': 'form-control'})
        self.fields['meetingTimeDuration'].widget.attrs.update({'class': 'form-control'})
        self.fields['meetingPlace'].widget.attrs.update({'class': 'form-control'})

        
     

        
        self.fields['meetingDate'].label            =' نوع جلسه را انتخاب کنید'
        self.fields['meetingTime'].label                  =' عنوان جلسه را وارد کنید'
        self.fields['meetingTimeDuration'].label            =' دبیر جلسه را انتخاب کنید'
        self.fields['meetingPlace'].label                =' اعضا  را انتخاب کنید'
 
 
class CreateFormMeetingEnactment(forms.ModelForm):

    class Meta:
        #نام مدل
        model = MeetingEnactment
       
        #فیلد های نمایش داده شده در فرم
        
        
        fields  = ('deadLine',)
        
        



     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        

        
        
        self.fields['deadLine'] = JalaliDateField(label=('deadLine'), widget=AdminJalaliDateWidget )
        


        
     
class CreateFormMeetingMember(forms.ModelForm):

    class Meta:
        #نام مدل
        model = MeetingDate
       
        #فیلد های نمایش داده شده در فرم
        
        fields  = '__all__'
        

     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meetingDate'] = JalaliDateField(label=('meetingDate'), widget=AdminJalaliDateWidget )

        self.fields['meetingDate'].widget.attrs.update({'class': 'form-control'})
        self.fields['meetingTime'].widget.attrs.update({'class': 'form-control'})
        self.fields['meetingTimeDuration'].widget.attrs.update({'class': 'form-control'})
        self.fields['meetingPlace'].widget.attrs.update({'class': 'form-control'})

        
     

        
        self.fields['meetingDate'].label            =' نوع جلسه را انتخاب کنید'
        self.fields['meetingTime'].label                  =' عنوان جلسه را وارد کنید'
        self.fields['meetingTimeDuration'].label            =' دبیر جلسه را انتخاب کنید'
        self.fields['meetingPlace'].label                =' اعضا  را انتخاب کنید'
 
        
   
     
class CreateFormMeetingInvitation(forms.ModelForm):

    class Meta:
        #نام مدل
        model = MeetingInvitation
       
        #فیلد های نمایش داده شده در فرم
        
        fields  = '__all__'
        

     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['meetingRelated'].widget =  forms.HiddenInput()
        
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
    
      
        self.fields['title'].label                  =' عنوان دعوتنامه را وارد کنید'
        self.fields['text'].label            =' متن دعوتنامه  را وارد کنید'
 
 
            
  
class CreateFormMeetingAgenda(forms.ModelForm):

    class Meta:
        #نام مدل
        model = MeetingAgenda
       
        #فیلد های نمایش داده شده در فرم
        
        fields  = '__all__'
        

     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['meetingRelated'].widget =  forms.HiddenInput()
        
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].widget.attrs.update({'rows': '3'})
        self.fields['responsible'].widget.attrs.update({'class': 'form-control'})
        self.fields['timeDuration'].widget.attrs.update({'class': 'form-control'})
      
        self.fields['title'].label                  =' عنوان دستور را وارد کنید'
        self.fields['text'].label            =' توضیحات دستور  را وارد کنید'
        self.fields['responsible'].label            =' مسئول دستور جلسه  را انتخاب کنید'
        self.fields['timeDuration'].label            =' مدت زمان برای این دستور   را انتخاب کنید'
 
 
            
  
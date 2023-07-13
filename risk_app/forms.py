from django import forms
from django.db import models
from .models import QuestionDaste ,RiskProfile ,RiskTeam , RiskIdentification , RiskActivityManager , RiskIdentificationSelecting,RiskMeasurement , RiskProcessRelated

from process_app.models import Group


class CreateFormQuestionDaste(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = QuestionDaste
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        
        

        #لیبل توضیح 
        
        self.fields['title'].label         =' عنوان دسته بندی سوال را وارد کنید'
        

        

class CreateFormRiskProfile(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = RiskProfile
        #فیلد های نمایش داده شده در فرم
        exclude = ('step',)
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['committeeRisk'].widget.attrs.update({'class': 'form-control'})
        
        

        #لیبل توضیح 
        
        self.fields['title'].label         =' عنوان پروفایل ریسک  را وارد کنید'
        self.fields['committeeRisk'].label ='   کمیته ریسک  را انتخاب کنید'
        

        
        


class CreateFormRiskTeam(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = RiskTeam
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['riskProfile'].widget.attrs.update({'class': 'form-control'})
        self.fields['memberProfile'].widget.attrs.update({'class': 'form-control'})
        self.fields['riskTopic'].widget.attrs.update({'class': 'form-control'})
        self.fields['hoze'].widget.attrs.update({'class': 'form-control'})
  
        


        #لیبل توضیح 
        self.fields['title'].label                  ='عنوان را وارد کنید'
        self.fields['riskProfile'].label            ='  پروفایل ریسک را انتخاب کنید'
        self.fields['memberProfile'].label          =' اعضا را انتخاب کنید'
        self.fields['riskTopic'].label            ='  سر فصل ریسک را انتخاب کنید'
        self.fields['hoze'].label          =' حوزه ریسک را انتخاب کنید'

        def clean_title(self,*args,**kwargs):
            title = self.cleaned_data.get("title")
            if (title == ''):
                raise forms.ValidationError('وارد کردن یک عنوان برای تیم اجباری است')

class CreateFormRiskIdentification(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = RiskIdentification
        
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['process'].widget.attrs.update({'class': 'form-control'})
        self.fields['group'].widget.attrs.update({'class': 'form-control'})
        self.fields['riskFailureModes'].widget.attrs.update({'class': 'form-control'})
        self.fields['riskCauses'].widget.attrs.update({'class': 'form-control'})
        self.fields['riskEffects'].widget.attrs.update({'class': 'form-control'})
        self.fields['currentAction'].widget.attrs.update({'class': 'form-control'})
        self.fields['team'].widget.attrs.update({'class': 'form-control'})
        self.fields['recommender'].widget.attrs.update({'class': 'form-control'})
        self.fields['activity'].widget.attrs.update({'class': 'form-control'})


        





        #لیبل توضیح 
        
        self.fields['riskFailureModes'].widget.attrs['placeholder']=' عنوان ریسک را وارد کنید'
        self.fields['riskCauses'].widget.attrs['placeholder']          =' علل بروز خطا را وارد کنید'
        self.fields['riskEffects'].widget.attrs['placeholder']         =' اثرات بروز خطا  را وارد کنید'
        self.fields['currentAction'].widget.attrs['placeholder']       =' کنترل های فعلی را وارد کنید'
        self.fields['team'].label                     =' تیم را وارد کنید'
        self.fields['recommender'].label              =' پیشنهاد دهنده را وارد کنید'
        self.fields['activity'].label                 =' فعالیت را وارد کنید'
        self.fields['process'].label                  =' فرآیند ریسک را انتخاب کنید'
        self.fields['group'].label                    =' گروه ریسک را انتخاب کنید'
        self.fields['riskFailureModes'].label         =''      
        self.fields['riskCauses'].label               =''  
        self.fields['riskEffects'].label              =''    
        self.fields['currentAction'].label            =''       


        def clean(self,*args,**kwargs):
            group = self.cleaned_data.get("group")
            if (group == ''):
                raise forms.ValidationError('وارد کردن یک عنوان برای تیم اجباری است')
class CreateFormRiskActivityManager(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = RiskActivityManager
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
        self.fields['riskTopic'].widget.attrs.update({'class': 'form-control'})
        self.fields['hoze'].widget.attrs.update({'class': 'form-control'})
  
        






        #لیبل توضیح 
        self.fields['sender'].label              =' فرستنده فعالیت را انتخاب کنید'
        self.fields['reciver'].label             =' گیرنده فعالیت را انتخاب کنید'
        self.fields['status'].label              =' وضعیت فعالیت را انتخاب کنید'
        self.fields['activity'].label            =' نوع فعالیت را انتخاب کنید'
        self.fields['team'].label                =' تیم فعالیت را انتخاب کنید'
        self.fields['previousActivity'].label    =' فعالیت قبلی را انتخاب کنید'
        self.fields['nextActivity'].label        =' فعالیت بعدی را انتخاب کنید'
        self.fields['riskTopic'].label           =' سرفصل ریسک را انتخاب کنید'
        self.fields['hoze'].label                =' حوزه ریسک را انتخاب کنید'




class CreateFormRiskIdentificationSelecting(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = RiskIdentificationSelecting
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['process'].widget.attrs.update({'class': 'form-control'})
        self.fields['group'].widget.attrs.update({'class': 'form-control'})
        self.fields['riskFailureModes'].widget.attrs.update({'class': 'form-control'})
        self.fields['riskCauses'].widget.attrs.update({'class': 'form-control'})
        self.fields['riskEffects'].widget.attrs.update({'class': 'form-control'})
        self.fields['currentAction'].widget.attrs.update({'class': 'form-control'})
        self.fields['team'].widget.attrs.update({'class': 'form-control'})
        self.fields['recommender'].widget.attrs.update({'class': 'form-control'})
        self.fields['activity'].widget.attrs.update({'class': 'form-control'})
        self.fields['riskIdentifications'].widget.attrs.update({'class': 'form-control'})
        





        #لیبل توضیح 
        self.fields['process'].label                  =' فرآیند ریسک را انتخاب کنید'
        self.fields['group'].label                  =' گروه ریسک را انتخاب کنید'
        self.fields['riskFailureModes'].label                  =' عنوان ریسک را وارد کنید'
        self.fields['riskCauses'].label            =' علل بروز خطا را وارد کنید'
        self.fields['riskEffects'].label          =' اثرات بروز خطا  را وارد کنید'
        self.fields['currentAction'].label             =' کنترل های فعلی را وارد کنید'
        self.fields['team'].label            =' تیم را وارد کنید'
        self.fields['recommender'].label            =' پیشنهاد دهنده را وارد کنید'
        self.fields['activity'].label            =' فعالیت را وارد کنید'
        self.fields['riskIdentifications'].label            =' ریسک های شناسایی شده مرتبط را انتخاب کنید'




class CreateFormRiskMeasurement(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = RiskMeasurement
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        self.fields['riskSeverity'].widget.attrs.update({'class': 'form-control' ,})
        self.fields['riskSeverity'].widget.attrs['min'] = 1
        self.fields['riskOccurrence'].widget.attrs.update({'class': 'form-control' ,})
        self.fields['riskDetection'].widget.attrs.update({'class': 'form-control' ,})
        self.fields['riskIdentificated'].widget.attrs.update({'class': 'form-control'})
        self.fields['activity'].widget.attrs.update({'class': 'form-control'})
        
  
        





        #لیبل توضیح 
        self.fields['riskSeverity'].label                  ='شدت ریسک را وارد کنید'
        self.fields['riskOccurrence'].label       =' احتمال وقوع ریسک را وارد کنید'
        self.fields['riskDetection'].label                  ='قابلیت کشف ریسک را وارد کنید'
        self.fields['riskIdentificated'].label       =' ریسک مرتبط  را وارد کنید'
        self.fields['activity'].label                  ='فعالیت مرتبط را وارد کنید'
        

      
      
      
class CreateFormRiskProcessRelated(forms.ModelForm):

    

    class Meta:
        #نام مدل
        model = RiskProcessRelated
        #فیلد های نمایش داده شده در فرم
        fields = '__all__'
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #کلاس های css
        
        self.fields['riskProfile'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        
        

        #لیبل توضیح 
        
        self.fields['riskProfile'].label         ='  پروفایل ریسک  را انتخاب کنید'
        self.fields['title'].label               ='   عنوان ارزیابی ریسک  را انتخاب کنید'
        
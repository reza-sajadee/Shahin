from django import forms
from django.db import models
from .models import  ProjectProfile , Project , PlanProfile , Action

from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
        

      
     
class CreateFormProjectProfile(forms.ModelForm):

    class Meta:
        #نام مدل
        model = ProjectProfile
       
        #فیلد های نمایش داده شده در فرم
        
        fields  = '__all__'
   

     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['accountable'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': '3'})
        self.fields['targetRequired'].widget.attrs.update({'class': 'form-control'})
        self.fields['targetRequired'].widget.attrs.update({'rows': '3'})
        self.fields['capitalEstimate'].widget.attrs.update({'class': 'form-control'})
        self.fields['capitalEstimate'].widget.attrs.update({'rows': '3'})
        self.fields['diurationEsimate'].widget.attrs.update({'class': 'form-control'})
        self.fields['diurationEsimate'].widget.attrs.update({'rows': '3'})
        self.fields['sourceProject'].widget.attrs.update({'class': 'form-control'})
        self.fields['sourceId'].widget.attrs.update({'class': 'form-control'})
        
        
        
        
        
  
class CreateFormProject(forms.ModelForm):

    class Meta:
        #نام مدل
        model = Project
       
        #فیلد های نمایش داده شده در فرم
        
        fields  = '__all__'
   

     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['code'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['responsible'].widget.attrs.update({'class': 'form-control'})
        self.fields['startTime'].widget.attrs.update({'class': 'form-control'})
        self.fields['startTime'].widget.attrs.update({'class': 'form-control'})
        self.fields['deadLine'].widget.attrs.update({'class': 'form-control'})
        self.fields['index'].widget.attrs.update({'class': 'form-control'})
        self.fields['currentSituation'].widget.attrs.update({'class': 'form-control'})
        self.fields['target'].widget.attrs.update({'class': 'form-control'})
       
        self.fields['resourceProject'].widget.attrs.update({'class': 'form-control'})
        self.fields['resourceId'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['controller'].widget.attrs.update({'class': 'form-control'})
        self.fields['accountable'].widget.attrs.update({'class': 'form-control'})
        self.fields['taskDependencies'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': '3'})
        
        
        
        

    
class CreateFormPlanProfile(forms.ModelForm):

    class Meta:
        #نام مدل
        model = PlanProfile
       
        #فیلد های نمایش داده شده در فرم
        
        fields  = '__all__'
        

     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['startTiem'] = JalaliDateField(label=('startTiem'), widget=AdminJalaliDateWidget )
        self.fields['deadLine'] = JalaliDateField(label=('deadLine'), widget=AdminJalaliDateWidget )

        self.fields['accountable'].widget.attrs.update({'class': 'form-control'})
        self.fields['responsible'].widget.attrs.update({'class': 'form-control'})
        self.fields['sourcePlan'].widget.attrs.update({'class': 'form-control'})
       


   
class CreateFormAction(forms.ModelForm):

    class Meta:
        #نام مدل
        model = Action
       
        #فیلد های نمایش داده شده در فرم
        
        #fields  = '__all__'
        
        fields  = ['planProfileRelated','responsible','title','description','startTiem','deadLine',]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['startTiem'] = JalaliDateField(label=('startTiem'), widget=AdminJalaliDateWidget )
        self.fields['deadLine'] = JalaliDateField(label=('deadLine'), widget=AdminJalaliDateWidget )
      

      


 
        
       
       
        
from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse
from organization_app.models import Vahed
from standardTable_app.models import RequirementStandards
from standardTable_app.models import Standard
from .forms import CreateFormPerformanceIndex , CreateFormPerformanceFormula , CreateFormVariableDataBase
from .models import TextDataBase  ,BoolDataBase ,ConfirmationDataBase ,SubjectPerformanceIndex ,TopicPerformanceIndex,PerformanceIndex ,VariableDataBase ,PerformanceFormula ,PerformanceIndexActivityManager
from organization_app.models import JobBank
from profile_app.models import Profile
#from .utils import get_next_month
from django.views.generic import ListView
import json
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from jalali_date import datetime2jalali, date2jalali

from datetime import timedelta

from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from formtools.wizard.views import SessionWizardView

#تایپ



class CreateViewPerformanceIndex( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createPerformanceIndex.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewPerformanceIndex'
    menu_link = 'ViewPerformanceIndex'
    def get(self, request, *args, **kwargs):
        form = CreateFormPerformanceIndex()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک شناسنامه عملکردی   جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex = {'extend':self.extend ,'menuBack':self.menuBack ,'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormPerformanceIndex(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            obj = form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='شناسنامه عملکردی   جدید با موفقیت ساخته شد !!!')
            return redirect('CreateViewPerformanceFormula' ,obj.pk )
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title =' شناسنامه عملکردی  مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'form': form }
        return redirect('CreateViewPerformanceFormula' ,form.id )



class CreateViewPerformanceFormula( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createFormula.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewPerformanceIndex'
    menu_link = 'ViewPerformanceIndex'
    def get(self, request , performanceIndexId, *args, **kwargs):
        performanceSelected = PerformanceIndex.objects.all().filter(id =performanceIndexId )[0]
        form = CreateFormPerformanceFormula(initial={'performanceIndexRelated':performanceSelected})
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "تعریف فرمول شناسنامه عملکردی   "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        
        #دیکشنری داده ها
        contex = {'extend':self.extend ,'menuBack':self.menuBack , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'form' :form , 'performanceSelected' : performanceSelected , }
        return render(request,self.template_name,contex)


    def post(self, request,performanceIndexId, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormPerformanceFormula(request.POST,request.FILES)
        performanceSelected = PerformanceIndex.objects.all().filter(id =performanceIndexId )[0]
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            obj = form.save(commit=False)
            obj.performanceIndexRelated = performanceSelected
            obj.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='شناسنامه عملکردی   جدید با موفقیت ساخته شد !!!')
            return redirect('CreateViewPerformanceVariables' ,obj.pk )
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title =' شناسنامه عملکردی  مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'form': form }
        return render(request,self.template_name,context)


class CreateViewPerformanceVariables( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createVariables.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewPerformanceIndex'
    menu_link = 'ViewPerformanceIndex'
    def get(self, request , performanceFormulaId, *args, **kwargs):
        formulaSelected = PerformanceFormula.objects.all().filter(id =performanceFormulaId )[0]
        performanceVariable = formulaSelected
        variables = VariableDataBase.objects.all()
        form = CreateFormVariableDataBase(initial = {'code' : 'x' + str(len(variables) +1)})
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "تعریف متغییر ها و فرمول شاخص  عملکردی   "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        allJob = JobBank.objects.all()
        headersList = ['نماد'  , 'عنوان' , 'مسئول']
     
        queryset = VariableDataBase.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.code)
            data.append(query.title)
            data.append(query.responsible)
   
            
 

         
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend ,'menuBack':self.menuBack , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color ,'form':form , 'formulaSelected' : formulaSelected , 'FormulaId' :formulaSelected.id  , 'performanceFormulaId':performanceFormulaId , 'allJob':allJob , 'variables':variables , 'len':len(variables) +1 , 'list_data':list_data  , 'headersList' : headersList , 'performanceVariable':performanceVariable}
        return render(request,self.template_name,contex)


    def post(self, request,performanceFormulaId , *args, **kwargs):
        #فرم دریافت شده
        try:
            PerformanceFormulaSelected = PerformanceFormula.objects.all().filter(id =performanceFormulaId )[0]
            PerformanceFormulaSelected.PerformanceFormula = request.POST.get('formula')
            PerformanceFormulaSelected.save()
            sweetify.toast(self.request,timer=30000 , icon="success",title ='شناسنامه عملکردی   جدید با موفقیت ساخته شد !!!')
            return redirect('ViewPerformanceIndex' , )
        except:
            sweetify.toast(self.request,timer=30000 , icon="error",title =' شناسنامه عملکردی  مورد نظر ساخته نشد !')
            context = {'extend':self.extend, }
            return render(request,self.template_name,context)
        #بررسی صحت اطلاعات ورودی
       
            #تابع نمایش پیغام
            
 

def add_variable(request , performanceFormulaId ):
    if request.method =="POST":
        title = request.POST.get('title')
        jobId = request.POST.get('responsible')
        jobSelected = JobBank.objects.all().filter(id = jobId)[0]
        responsible = jobSelected.profile
        description = request.POST.get('description')
        code = request.POST.get('code')
      

        
        PerformanceFormulaRelatedSelected = PerformanceFormula.objects.all().filter(id =performanceFormulaId )[0]

        if(VariableDataBase.objects.all().filter(title =title ).exists()):
            instance = VariableDataBase.objects.all().filter(title =title )[0]
        else:
            instance = VariableDataBase.objects.create(title = title ,description = description ,code = code ,responsible = jobSelected , )
        
        allVariables = VariableDataBase.objects.all()
        if(instance in PerformanceFormulaRelatedSelected.variablesRelated.all() ):
            pass
        else:
            PerformanceFormulaRelatedSelected.variablesRelated.add(instance)
        
        performanceVariable = PerformanceFormulaRelatedSelected
        
        return render(request , 'partials/variable-list.html' ,{'allVariables' : allVariables , 'performanceVariable' : performanceVariable} )
    else:
        pass


def add_variable_toFormula(request , performanceFormulaId , variableId ):
    if request.method =="POST":
        
        
        
       
       
        PerformanceFormulaRelatedSelected = PerformanceFormula.objects.all().filter(id =performanceFormulaId )[0]
        
        variableSelected = VariableDataBase.objects.all().filter(id = variableId)[0]
        print('***********len' ,variableSelected) 
        allVariables = VariableDataBase.objects.all()
        if(variableSelected in PerformanceFormulaRelatedSelected.variablesRelated.all() ):
            pass
        else:
            PerformanceFormulaRelatedSelected.variablesRelated.add(variableSelected)
        
        performanceVariable = PerformanceFormulaRelatedSelected
        
        return render(request , 'partials/variable-list.html' ,{'allVariables' : allVariables , 'performanceVariable' : performanceVariable} )
    else:
        pass
  
def delete_variable(request , performanceFormulaId, variableId):

    variableSelected = VariableDataBase.objects.all().filter(id = variableId)[0]
    performanceFormulaSelected = PerformanceFormula.objects.all().filter(id =performanceFormulaId )[0]
    performanceFormulaSelected.variablesRelated.remove(variableSelected)

    performanceFormulaSelectedNew = PerformanceFormula.objects.all().filter(id =performanceFormulaId )[0]
    allVariables = VariableDataBase.objects.all()
    
    performanceVariable = performanceFormulaSelectedNew
   
    return render(request , 'partials/variable-list.html' ,{'allVariables' : allVariables , 'performanceVariable' : performanceVariable , 'FormulaId' : performanceFormulaSelectedNew.id} )



class ListViewPerformanceFormula(ListView):
  
    extend = 'baseEmployee.html'
    menuBack = 'ViewPerformanceIndex'
    
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست ارزیابی ریسک سوال  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام ارزیابی ریسک سوال  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان شاخص عملکردی' , 'دوره' , 'مسئول']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = PerformanceFormula.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
         
            data.append(query.performanceIndexRelated.title)
            data.append(query.get_cycle_display)
            data.append(query.responsible)
           
   
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend,'menuBack':self.menuBack, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = PerformanceFormula
    ordering = '-created_at' 
    template_name ='list.html'


class ViewPerformanceFormula( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "viewPerformanceFormula.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewPerformanceIndex'
    def get_obj(self):

        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(PerformanceFormula,id = id)
        return obj

   

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            
            #print(default_storage.exists('caspian'))

            
            obj = get_object_or_404(PerformanceFormula,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش مستند داخلی  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت
            icon_name     = "person_add"
            #تعداد ستون ها
            color         = "info"


            

            #رنگ
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'menuBack':self.menuBack,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name, 'obj':obj,
            'color':color , 'columns':columns ,}


        return render(request,self.template_name,context)
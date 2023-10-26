from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse
from organization_app.models import Vahed
from standardTable_app.models import RequirementStandards
from standardTable_app.models import Standard
from .forms import CreateFormPerformanceIndex , CreateFormPerformanceFormula , CreateFormVariableDataBase
from .models import TextDataBase  ,BoolDataBase ,ConfirmationDataBase ,SubjectPerformanceIndex ,TopicPerformanceIndex,PerformanceIndex ,VariableDataBase ,PerformanceFormula ,PerformanceIndexActivityManager , VariableDataBase , PerformanceSettings
from organization_app.models import JobBank
from profile_app.models import Profile
from .utils import create_activity  , get_activity_done , gregorian_to_jalali , jalali_to_gregorian
from django.views.generic import ListView
import json
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from jalali_date import datetime2jalali, date2jalali
from event_app.models import Event
from datetime import timedelta
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from formtools.wizard.views import SessionWizardView
from django.db.models import Q
from .utils import   colorPrimary, colorSuccess, colorDanger, generate_color_palette
import pandas as pd
def activityCreator(profile , cycle ):
   pass
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
        
            PerformanceFormulaSelected = PerformanceFormula.objects.all().filter(id =performanceFormulaId )[0]
            PerformanceFormulaSelected.PerformanceFormula = request.POST.get('formula')
            PerformanceFormulaSelected.save()
            create_activity(PerformanceFormulaSelected , PerformanceIndexActivityManager , PerformanceSettings.objects.all()[0] , Event)
            sweetify.toast(self.request,timer=30000 , icon="success",title ='شناسنامه عملکردی   جدید با موفقیت ساخته شد !!!')
            
            return redirect('ViewPerformanceIndexDashboard' , )
        
        #بررسی صحت اطلاعات ورودی
       
            #تابع نمایش پیغام
            
 

def add_variable(request , performanceFormulaId ):
    if request.method =="POST":
        title = request.POST.get('title')
        jobId = request.POST.get('responsible')
        jobSelected = JobBank.objects.all().filter(id = jobId)[0]
        responsible = jobSelected.profile
        description = request.POST.get('description')
        
        
        
        PerformanceFormulaRelatedSelected = PerformanceFormula.objects.all().filter(id =performanceFormulaId )[0]
        code = 'x' + str(PerformanceFormulaRelatedSelected.variablesRelated.all().count()+1) 
        if(VariableDataBase.objects.all().filter(title =title ).exists()):
            instance = VariableDataBase.objects.all().filter(title =title )[0]
        else:
            code = 'x' + str(VariableDataBase.objects.all().count()+1) 
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


def add_variable_value(request , activityId ):
    if request.method =="POST":
        activitySelected = PerformanceIndexActivityManager.objects.get(id = activityId)
        variableValue = request.POST.get('variable')
        activitySelected.texts = variableValue
        activitySelected.status = 'done'
        activitySelected.save()
        userProfile = Profile.objects.get(user=request.user)
        if(userProfile.user.is_superuser):
            allActivity = PerformanceIndexActivityManager.objects.all()
        else:
            allActivity = PerformanceIndexActivityManager.objects.all().filter(reciver = userProfile)
        if(request.user.is_superuser):
            activityNotDone = allActivity.filter(status='doing' )
        else:
            activityNotDone = allActivity.filter(Q(reciver = userProfile) & Q(status='doing') )
        
     
        return render(request , 'partials/variable-enter-list.html' ,{'activityNotDone' : activityNotDone , } )
    else:
        pass


def add_variable_toFormula(request , performanceFormulaId , variableId ):
    if request.method =="POST":
        
        
        
       
       
        PerformanceFormulaRelatedSelected = PerformanceFormula.objects.all().filter(id =performanceFormulaId )[0]
        
        variableSelected = VariableDataBase.objects.all().filter(id = variableId)[0]
        
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
        header_title  = "لیست فرمول شاخص ها    "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام ارزیابی ریسک سوال  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
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
    


class ListViewPerformanceَActivity(ListView):
  
    extend = 'baseEmployee.html'
    menuBack = 'ViewPerformanceIndex'
    
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        userProfile = Profile.objects.get(user = self.request.user)
        header_title  = "لیست فرمول شاخص ها    "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام ارزیابی ریسک سوال  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = [ 'مسئول' , 'متغییر' , 'عنوان متغییر' , 'زمان شروع' , 'زمان پایان']
        #اسم داده های جدول

        #دریافت تمام داده ها
        if(userProfile.user.is_superuser):
            queryset = PerformanceIndexActivityManager.objects.all()
        else:
            queryset = PerformanceIndexActivityManager.objects.all(reciver = userProfile)
      
        list_data_now = []
        list_data_complate = []
        list_data_notComplate = []
        list_data_other = []
        #ایجاد لیست داده ها
        for data in queryset:
            if(data.getResidual() > PerformanceSettings.objects.all().first().startPeriod and data.getResidual() < PerformanceSettings.objects.all().first().endPeriod):
                list_data_now.append(data)
            elif(data.getResidual() < 0):
                if(data.status == 'done'):
                    list_data_complate.append(data)
                else:
                    list_data_notComplate.append(data)
            else:
                list_data_other.append(data)


       
        #دیکشنری داده ها
        context= {'extend':self.extend,'menuBack':self.menuBack, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,'queryset': queryset, 
        'columns':columns , 'color':color , 'header_table': header_table  , 'today' : datetime.today().date 
          ,  'list_data_now':list_data_now,  'list_data_complate':list_data_complate,  'list_data_notComplate':list_data_notComplate , 'list_data_other':list_data_other}
        return context

    model = PerformanceFormula
    ordering = '-created_at' 
    template_name ='listvr.html'



 
class ViewPerformanceIndexDashboard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "clearDashboard.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
 
    def get(self, request ,*args, **kwargs):
        monthName = {1 : 'فروردین', 2 :'اردیبهشت' ,3 :'خرداد' , 4 :'تیر' ,5 :'مرداد' , 6 :'شهریور' ,7 :'مهر' , 8 :'آبان' ,9 :'آذر' , 10 : 'دی',11 :'بهمن' , 12 :'اسفند' ,}
        userProfile = Profile.objects.get(user=self.request.user)
        
        header_title  = "داشبورد شاخص عملکردی"
        #توضحات نمایش داده شده در زیر عنوان
        
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"

        responsibleCount = 0
        memberCount = 0
        createNewProfile = 'CreateViewPerformanceIndex'
        allProfile=[]
        allPerformanceIndex = PerformanceIndex.objects.all()
        if(userProfile.user.is_superuser):
            allActivity = PerformanceIndexActivityManager.objects.all()
        else:
            allActivity = PerformanceIndexActivityManager.objects.all().filter(reciver = userProfile)
        for performanceIndex in allPerformanceIndex:
            allProfile.append(performanceIndex)
        if(request.user.is_superuser):
            activityNotDone = allActivity
        else:
            activityNotDone = allActivity.filter(Q(reciver = userProfile) )
       
        allLenghtDoing = len(allActivity.filter(status='doing') )
        partials = 'partials/performanceDashboard.html'
        allFormula = PerformanceFormula.objects.all()
        
        if(request.GET.get('profileId',None)):
            try:
                profilePerformanceIndexSelected = PerformanceIndex.objects.get(id = request.GET['profileId'])
            except:
                return render(request,self.template_name,context={'partials':partials ,'header_title':header_title ,'icon_name':icon_name ,'color':color ,'responsibleCount':responsibleCount ,'memberCount':memberCount ,'createNewProfile':createNewProfile ,'allProfile':allProfile ,'activityNotDone':activityNotDone })

        else:
            profilePerformanceIndexSelected = PerformanceIndex.objects.all().last()
        
        
       
        responsible_link = None
        member_link =  'ListViewPerformanceَActivity'
        if(len(activityNotDone) >0):
            memberCount = len(activityNotDone)
            member_link = 'ListViewCorrectiveActionDoing'    
        # if(jobBankSelected in profileRiskSelected.committeeRisk.members.all()):
        #     member_link = 'ViewRiskDashboardMember'
        
        member_link = None
       
        dataList = {}
        #dataList2 = {'خرداد' :5 , 'تیر' : 3,'مرداد' :7 ,'شهریور' : 2,'مهر' :9 ,}
        try:
            performanceFormulaSelected = PerformanceFormula.objects.get(performanceIndexRelated__id = profilePerformanceIndexSelected.id)
        except:
            context = {'extend':self.extend , 'menuBack':self.menuBack, 'header_title':header_title,'profileSelected':profilePerformanceIndexSelected,'createNewProfile':createNewProfile,
        'icon_name':icon_name,'header_title':header_title,'responsible_link':responsible_link,'member_link':member_link,'activityNotDone':activityNotDone,
        'color':color ,'partials':partials, 'allProfile':allProfile ,  'responsibleCount':responsibleCount,'memberCount':memberCount , 'dataList':dataList  , 
        }

            return render(request,self.template_name,context)
        allVariables = performanceFormulaSelected.variablesRelated.all()
        tdJalali = gregorian_to_jalali(datetime.today().year , datetime.today().month , datetime.today().day)
        listDataVariableSelected = {}
        
        
        
            
        for i in range(1,13):
            for variable in allVariables:
               
                groDate = gregorian_to_jalali(datetime.today().year , i , 1)
                
                if(i > tdJalali[1]):
                    
                    break
                else:
                    
                    if(performanceFormulaSelected.cycle == 'seasonal'):
                        if i%3 != 0:
                            continue
                    if(performanceFormulaSelected.cycle == 'semiAnnualy'):
                        if i%6 != 0:
                            continue
                    if(performanceFormulaSelected.cycle == 'annualy'):
                        if i%12 != 0:
                            continue
                    
                    #listDataVariableSelected({monthName[i] : {variable.code : 1 } })
                    tempDict = {}
                    
                    
                    if PerformanceIndexActivityManager.objects.all().filter(variableRelated = variable).filter(startTime__month = i).exists():
                        try:
                            tempDict[variable.code] = float(PerformanceIndexActivityManager.objects.all().filter(variableRelated = variable).filter(startTime__month = i).first().texts)
                        except:
                            tempDict[variable.code] = None
                    else:
                        tempDict[variable.code] = None
                    
                    if(monthName[i] in listDataVariableSelected ):
                        
                        if PerformanceIndexActivityManager.objects.all().filter(variableRelated = variable).filter(startTime__month = i).exists():
                            try:
                                listDataVariableSelected[monthName[i]][variable.code] = float(PerformanceIndexActivityManager.objects.all().filter(variableRelated = variable).filter(startTime__month = i).first().texts)
                            except:
                                listDataVariableSelected[monthName[i]][variable.code] = None

                        else:
                            listDataVariableSelected[monthName[i]][variable.code] = None
                    else:
                        listDataVariableSelected[monthName[i]] = tempDict
        
        for month in listDataVariableSelected:
            monthVariables = dict(listDataVariableSelected[month])
            
            variableValue = 0
            
            for variable in monthVariables:
                if not monthVariables[variable]:
                    break
                else:
      
                    variableValue = (eval(performanceFormulaSelected.PerformanceFormula,{"__builtins__":None},monthVariables))
                    
                    
                    break
            if(variableValue != 0):
                dataList[month]    = variableValue
                print('variableValue' , month , ' : ' , variableValue)
            
                
        
       
        #عنوان نمایش داده شده در بالای صفحه
        firstBound = []
        secondBound = []
        zeroBound = []
        dataList
        allLabeles = list(dataList.keys())
        allValue = list(dataList.values())
        condition = performanceFormulaSelected.acceptableCondition
        for x in allLabeles :
            firstBound.append(performanceFormulaSelected.acceptableCriteria)
            secondBound.append(performanceFormulaSelected.acceptableCriteriaSecond)
            zeroBound.append(0)

        #رنگ             
        columns       = 1
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack, 'header_title':header_title,'profileSelected':profilePerformanceIndexSelected,'createNewProfile':createNewProfile,'today':datetime.today().date,
        'icon_name':icon_name,'header_title':header_title,'responsible_link':responsible_link,'member_link':member_link,'activityNotDone':activityNotDone,'condition':condition ,'firstBound':firstBound ,'secondBound':secondBound ,'allValue':allValue,'zeroBound':zeroBound,
        'columns':columns , 'color':color ,'partials':partials, 'allProfile':allProfile ,  'responsibleCount':responsibleCount,'memberCount':memberCount , 'dataList':dataList  , 'allLabeles':allLabeles
        }

        return render(request,self.template_name,context)
    
def loadChart(request ):
     dataSets = []
    
     
     df = pd.read_csv('data.csv' ,dtype={1:'int64',2:'int64'})
     df = df.set_index('Date')
     labels = df.keys()
     for label in labels:
         temp = {
                "label": label,
                "backgroundColor": [colorSuccess, colorDanger],
                "borderColor": [colorSuccess, colorDanger],
                "data": list(df[label]),
            }
         dataSets.append(temp)
     return JsonResponse({
        "title": f"1",

        "data": {
            "labels": list(df.index),
            "datasets": dataSets,
        },
    })
 
class ViewChart( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "chart.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
 
    def get(self, request ,*args, **kwargs):
        monthName = {1 : 'فروردین', 2 :'اردیبهشت' ,3 :'خرداد' , 4 :'تیر' ,5 :'مرداد' , 6 :'شهریور' ,7 :'مهر' , 8 :'آبان' ,9 :'آذر' , 10 : 'دی',11 :'بهمن' , 12 :'اسفند' ,}
        userProfile = Profile.objects.get(user=self.request.user)
        
       
        #توضحات نمایش داده شده در زیر عنوان
        
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"

        

        
       
        #رنگ             
        columns       = 1
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack, 'icon_name':icon_name, 'columns':columns , 'color':color   , 
         }

        return render(request,self.template_name,context)
    

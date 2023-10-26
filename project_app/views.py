from django.shortcuts import render
from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CreateFormProjectProfile , CreateFormProject , CreateFormPlanProfile , CreateFormAction
from .models import Task , ProjectProfile , Project , PlanProfile , Action
from django.urls import reverse
from django.views.generic import ListView
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from profile_app.models import Profile
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Model
from profile_app.decorators import  staff_only
from organization_app.models import JobBank
from django.db.models import Q
from collections import defaultdict
from datetime import datetime
# Create your views here.

class CreateViewProjectProfile( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createProjectProfileView.html"
    extend='baseEmployee.html'
    menuBack = 'ViewProject'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormProjectProfile()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "تعریف یک پروژه جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک پروژه جدید جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        #دیکشنری داده ها
        contex = {'extend':self.extend, 'menuBack':self.menuBack ,'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormProjectProfile(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='پروژه جدید جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewProjectProfile')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='پروژه جدید مورد نظر ساخته نشد !')
        context = {'extend':self.extend, 'menuBack':self.menuBack ,'riskDabir':'','form': form}
        return render(request,self.template_name,context)


class ListViewProjectProfile(ListView):
  


    extend='baseEmployee.html'
    menuBack = 'ViewProject'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست   پروفایل پروژه ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوع پست سازمانی ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
        link_list =[]
        admin_link_list = []
        profileSelected =  Profile.objects.get(user = self.request.user)
        if(ProjectProfile.objects.all().filter(accountable__profile =profileSelected ).exists()):
            link_dict = {'title' : ' تعریف جلسه جدید' , 'icon' : 'edit' , 'link' : 'CreateViewProject' , 'type':'key' }
            link_list.append(link_dict)



        header_table   = ['عنوان' ]
        #اسم داده های جدول
        object_name    = ['title','accountable' , 'meetingType']
        #دریافت تمام داده ها
        queryset = ProjectProfile.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
    
           
            
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend, 'menuBack':self.menuBack , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data , 'link_list' :link_list}
        return context

    model = ProjectProfile
  
    template_name ='listProjectProfileView.html'

class ListViewProject(ListView):
  


    extend='baseEmployee.html'
    menuBack = 'ViewProject'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست    پروژه ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوع پست سازمانی ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
        link_list =[]
        admin_link_list = []
        profileSelected =  Profile.objects.get(user = self.request.user)
        jobSelected = JobBank.objects.get(profile =profileSelected )
   



        header_table   = ['عنوان' ]
        #اسم داده های جدول
        object_name    = ['title','accountable' , 'meetingType']
        #دریافت تمام داده ها
        if(self.request.user.is_superuser):
            queryset = Project.objects.all()
        else:
            queryset = Project.objects.all().filter(accountable = jobSelected )
        
        
        list_data = []
        #ایجاد لیست داده ها
       
        #دیکشنری داده ها
        context = {'extend':self.extend, 'menuBack':self.menuBack , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'queryset' : queryset , 'link_list' :link_list}
        return context

    model = ProjectProfile
  
    template_name ='listProjectView.html'


class CreateViewProject( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createProjectView.html"
    extend='baseEmployee.html'
    menuBack = 'ViewProject'
    
    def get(self , request, profileId=None, *args, **kwargs):
        form = CreateFormProject()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "تعریف یک پروژه جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک پروژه جدید جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        profileSelected = ProjectProfile.objects.get(id = profileId)
        source_link = '#'
        list_data = []
        allProjects = Project.objects.all().filter(profileProjectRelated = profileSelected)
        #دیکشنری داده ها
        
        contex = {'extend':self.extend, 'menuBack':self.menuBack ,'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'profileSelected':profileSelected , 'source_link' : source_link , 'allProjects' : allProjects}
        return render(request,self.template_name,contex)


    def post(self, request , profileId=None, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormProject(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            instance = form.save(commit=False)
            if(instance.previousProject !=None):
                pP = instance.previousProject
                instance.save()
                pP.nextProject.add(instance)
                pP.save()

            else:
                instance.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='پروژه جدید جدید با موفقیت ساخته شد !!!')
            return redirect('CreateViewProject', profileId=profileId)
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='پروژه جدید مورد نظر ساخته نشد !')
        context = {'extend':self.extend, 'menuBack':self.menuBack ,'riskDabir':'','form': form}
        return render(request,self.template_name,context)


class DeleteViewProject( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend = 'baseEmployee.html'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Project,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک   پروژه"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که   پروژه   " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend':self.extend, 'menuBack':self.menuBack ,'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    def post(self, request,profileId=None,id=None ,*args, **kwargs):
        context = {'extend':self.extend, 'menuBack':self.menuBack ,}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            profileId = obj.profileProjectRelated.id
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='پروژه  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('CreateViewProject', profileId=profileId)
        return render(request,self.template_name,context)
    


class ViewProject( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detail.html"
    extend = 'baseEmployee.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Project,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = Project.objects.all().filter(id=id)[0]
           
            obj = get_object_or_404(Project,id = id)
            
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "اطلاعات پروژه   "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "چزییات ارزیابی ریسک سوال را در این صفحه می توانید مشاهده کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها

            #جدول لیست پرداختی ها
        
    
            #ایجاد لیست داده ها
            header_table   = ['عنوان' ]
            
            list_data = { 'پروفایل':obj.profileProjectRelated,'کد':obj.code ,'عنوان':obj.title , 'مسئول':obj.responsible,'زمان شروع':obj.startTime ,'تاریخ پایان':obj.deadLine ,'سنجه':obj.index ,'وضیعیت علی':obj.currentSituation ,'وضعیت مطلوب':obj.target ,'منشا':obj.resourceProject ,'توضیحات':obj.description ,'کنترلر':obj.controller ,'مدیر پروژه':obj.accountable ,'وابستگی وظیفه':obj.taskDependencies,'وضعیت':obj.status ,  }
            #ایجاد لیست داده ها
           
            #جدول لیست کلاس ها
            # عنوان های جدول
            
                
            context =  {'extend':self.extend , 'object':obj , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,
                'color':color , 'columns':columns,'list_data':list_data,
                'header_table':header_table , 'form':form , }


        return render(request,self.template_name,context)
 

 
class ViewPlanDashboard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "clearDashboard.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    selectProfile = 'فعالیت'
 
    def get(self, request ,*args, **kwargs):
        
        dataBars = defaultdict(list)
        
        selectedType =  request.GET.get('type') 
        createNewProfile = None
        allPlan = PlanProfile.objects.all()
        allProfile = None
        responsible_link = None
        
        allPlanCount  = allPlan.count()
        allPlanDoneCount  = allPlan.filter(status = 'complate').count()

        myPlanCount = allPlan.filter(responsible__profile__user = request.user).count()
        myPlanDoneCount = allPlan.filter(responsible__profile__user = request.user , status='complate').count()
        for plan in allPlan:
            dataBars['label'].append(plan.title)
            dataBars['doing'].append(len(Action.objects.filter(planProfileRelated = plan).filter(status = 'doing')))
            dataBars['done'].append(len(Action.objects.filter(planProfileRelated = plan).filter(status = 'done')))
            #dataBars['done'].append(len(plan.filter(status = 'done')))
        
        member_link =  None
     
        partials = 'partials/planDashboard.html'
        header_title = "داشبورد برنامه های اجرایی"
       
        #دریافت تمام داده ها
        member = Profile.objects.get(user = request.user)
        jobBankSelected = JobBank.objects.get(profile = member)
        if(request.user.is_superuser):
            responsible_link = None
            member_link = None
            createNewProfile = None
     
        if(request.GET.get('profileId',None)):
            profileSelected = PlanProfile.objects.get(id = request.GET['profileId'])
        else:
            profileSelected = PlanProfile.objects.all().first()
        
        
        allPlan = PlanProfile.objects.all().filter(responsible = jobBankSelected)
        if(profileSelected):
            allAction = Action.objects.all().filter(planProfileRelated = profileSelected.id)
        else:
            allAction = None
        
        
       
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
     
     
        
        context = {'extend':self.extend , 'menuBack':self.menuBack, 'header_title':header_title,'member_link':member_link,'dataBars':dataBars,
        'discribtion':discribtion,'icon_name':icon_name,'header_title':header_title,'responsible_link':responsible_link ,'profileSelected':profileSelected,
        'color':color  ,'partials':partials,'createNewProfile':createNewProfile,'allProfile':allProfile , 'allAction':allAction , 'selectProfile' :self.selectProfile,
        'allPlanCount' :allPlanCount , 'allPlanDoneCount' :allPlanDoneCount , 'myPlanCount' :myPlanCount , 'myPlanDoneCount' :myPlanDoneCount 
        }

        return render(request,self.template_name,context)
    
    def post(self, request , actionId = None  , *args, **kwargs):
        x = request.POST.get('actionId')
        actionSelected = Action.objects.get(id = request.POST.get('actionId'))
        if(actionSelected.status == 'pending'):
            actionSelected.status = 'done'
            sweetify.toast(self.request,timer=30000 , icon="success",title ='فعالیت مورد نظر به اتمام رسید!!!')
        else:
            actionSelected.status = 'pending'
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='فعالیت مورد نظر در حال انتظار است  !!!')
        actionSelected.save()
        
        
        return redirect('ViewPlanDashboard' )

def change_status(request):
    actionId = request.POST.get('actionId')
    actionSelected = Action.objects.get(id = request.POST.get('actionId'))
    if(actionSelected.status == 'pending'):
        actionSelected.status = 'done'
        sweetify.toast(request,timer=30000 , icon="success",title ='فعالیت مورد نظر به اتمام رسید!!!')
    else:
        actionSelected.status = 'pending'
        sweetify.toast(request,timer=30000 , icon="warning",title ='فعالیت مورد نظر در حال انتظار است  !!!')
    actionSelected.save()
    planeSelected = actionSelected.planProfileRelated
    allAction = PlanProfile.objects.filter(planProfileRelated = planeSelected.id)
    return render(request , 'partials/time-line.html' ,{ 'allAction' : allAction} )


class CreateViewPlanProfile( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createPlanProfile.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewPlanDashboard'
   
  

    def get(self, request  ,  *args, **kwargs):
        
      
     
        
        form = CreateFormPlanProfile()
        
        
            
       
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "تعریف برنامه اجرایی جدید  "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        jobBankUser = JobBank.objects.get(profile__user = request.user)
        
       
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'form':form ,'jobBankUser' : jobBankUser}
        return render(request,self.template_name,contex)


    def post(self, request  , *args, **kwargs):
        
        form = CreateFormPlanProfile( request.POST )
        print(form)
        
        #فرم دریافت شده
        if form.is_valid():
            userProfileSelected = Profile.objects.get(user = self.request.user)
            jobBankSelected = JobBank.objects.get(profile = userProfileSelected)
            
            instance = form.save(commit=False)
            instance.accountable = jobBankSelected
            instance.responsible = jobBankSelected
            instance.save()
            sweetify.toast(self.request,timer=30000 , icon="success",title =' برنامه اجرایی جدید ساخته شد!!!')
            return redirect('ViewPlanDashboard')
        else:
            messages.error(request, "Error")
            sweetify.toast(self.request,timer=30000 , icon="error",title =' برنامه اجرایی جدید ساخته نشد !!!')
            return redirect('ViewPlanDashboard')


class UpdateViewPlanProfile( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(PlanProfile,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormPlanProfile(instance=obj)
            
            obj = get_object_or_404(PlanProfile,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش نوبت ممیزی  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این نوبت ممیزی  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns ,'extend':self.extend , 'menuBack':self.menuBack ,}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormTypeMomayezi(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='نوبت ممیزی  جدید با موفقیت ساخته شد !!!')
                return redirect('MomayeziListViewTypeMomayezi')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='نوبت ممیزی  مورد نظر ساخته نشد !')           
            context = {'form': form,'object':obj ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return render(request,self.template_name,context)


class DeleteViewAction( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Action,id = id)
        return obj
   
    def get(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='نوبت ممیزی  با موفقیت پاک شد !!!')
            context ={'extend':self.extend , 'menuBack':self.menuBack }
            return redirect('ViewPlanProfile' ,obj.planProfileRelated.id )
        return render(request,self.template_name,context)
 

class ListViewPlanProfile(ListView):
  


    extend='baseEmployee.html'
    menuBack = 'ViewPlanDashboard'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست     برنامه های اجرایی"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوع پست سازمانی ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
        link_list =[]
        admin_link_list = []
        userProfileSelected =  Profile.objects.get(user = self.request.user)
        jobSelected = JobBank.objects.get(profile =userProfileSelected )
   



        header_table   = ['عنوان' ]
        #اسم داده های جدول
       
        #دریافت تمام داده ها
        if (self.request.user.is_superuser  ):
            queryset = PlanProfile.objects.all()
        else:
            queryset = PlanProfile.objects.all().filter(responsible = jobSelected )
        
        list_data = []
        #ایجاد لیست داده ها
       
        #دیکشنری داده ها
        context = {'extend':self.extend, 'menuBack':self.menuBack , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
        'queryset' : queryset , 'link_list' :link_list}
        return context

    model = ProjectProfile
  
    template_name ='listPlanView.html'



class ViewPlanProfile( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detailPlanProfile.html"
    extend = 'baseEmployee.html'
    menuBack = 'ListViewPlanProfile'
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

      
        form = CreateFormPlanProfile()
        planProfileSelected = PlanProfile.objects.get(id = id)
        
        allAction = Action.objects.all().filter(planProfileRelated = planProfileSelected)
        
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "اطلاعات پروژه   "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "چزییات ارزیابی ریسک سوال را در این صفحه می توانید مشاهده کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        #رنگ             
        columns       = 1
        #دیکشنری داده ها

        #جدول لیست پرداختی ها
    

        #ایجاد لیست داده ها
       
        
        
        #ایجاد لیست داده ها
        
        #جدول لیست کلاس ها
        # عنوان های جدول
        ss = "--accent-color:#41516C"
        allJobBank  =     JobBank.objects.all()
        context =  {'extend':self.extend,'menuBack' : self.menuBack , 'form':form , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,'allAction':allAction,'allJobBank':allJobBank,
            'color':color , 'columns':columns, 'planProfileSelected' : planProfileSelected,'ss':ss
             }
        return render(request,self.template_name,context)
 
    def post(self, request , id = None  , *args, **kwargs):
        planProfileSelected = PlanProfile.objects.get(id = id)
        form = CreateFormAction( request.POST )
        #فرم دریافت شده
        
        
        if form.is_valid():
            
            
            instance = form.save()
            instance.color = instance.id%5
            
            # if(len(Action.objects.all().filter(planProfileRelated = planProfileSelected)) == 1):
            #     instance.status = 'doing'
                
            instance.save()
            sweetify.toast(self.request,timer=30000 , icon="success",title =' برنامه اجرایی جدید ساخته شد!!!')
            return redirect('ViewPlanProfile' ,  id=id)
        else:
            print (form.errors)
            sweetify.toast(self.request,timer=30000 , icon="error",title =' برنامه اجرایی جدید ساخته نشد !!!')
            return redirect('ViewPlanProfile' ,  id=id)
 

class ViewPlanProfile2( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detailPlanProfile2.html"
    extend = 'baseEmployee.html'
    menuBack = 'ListViewPlanProfile'
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

      
        form = CreateFormPlanProfile()
        planProfileSelected = PlanProfile.objects.get(id = id)
        
        allAction = Action.objects.all().filter(planProfileRelated = planProfileSelected)
        progressDone = 0
        for action in allAction:
            progressDone = progressDone + (action.progress * (action.weight/100))
        
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "اطلاعات پروژه   "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "چزییات ارزیابی ریسک سوال را در این صفحه می توانید مشاهده کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        #رنگ             
        columns       = 1
        projectRemainsDayes = (planProfileSelected.deadLine.date() - datetime.now().date()).days
        
        if (projectRemainsDayes < 0 ):
            projectRemainsDayes = 0
        projectPassedDayes = (datetime.now().date() - planProfileSelected.startTiem.date()).days
        
        if (projectPassedDayes < 0 ):
            projectPassedDayes = 0
        projectDays = (planProfileSelected.deadLine.date() - planProfileSelected.startTiem.date()).days
        projectBarColor = 'success'
        if((projectPassedDayes / projectDays) > 0.5):
            if((projectPassedDayes / projectDays) > 0.75):
                projectBarColor = 'danger'
            else:
                projectBarColor = 'warning'
       
        
        
        try:
            
            max_weight = allAction[0].max_weight()
        except:
            max_weight = 100
        
        ss = "--accent-color:#41516C"
        allJobBank  =     JobBank.objects.all()
        context =  {'extend':self.extend,'menuBack' : self.menuBack , 'form':form , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,'allAction':allAction,'allJobBank':allJobBank,'max_weight':max_weight,
            'color':color , 'columns':columns, 'planProfileSelected' : planProfileSelected,'ss':ss , 'progressDone':progressDone , 'projectRemainsDayes' :projectRemainsDayes , 'projectPassedDayes' :projectPassedDayes ,'projectDays' :projectDays ,'projectBarColor':projectBarColor,
             }
        return render(request,self.template_name,context)
 
    def post(self, request , id = None  , *args, **kwargs):
        planProfileSelected = PlanProfile.objects.get(id = id)
        form = CreateFormAction( request.POST )
        #فرم دریافت شده
        
        print(form.is_valid())
        if form.is_valid():
            
            
            instance = form.save()
            instance.color = instance.id%5
            print(request.POST.get('weight'))
            instance.weight = int(request.POST.get('weight'))
            # if(len(Action.objects.all().filter(planProfileRelated = planProfileSelected)) == 1):
            #     instance.status = 'doing'
                
            instance.save()
            sweetify.toast(self.request,timer=30000 , icon="success",title =' برنامه اجرایی جدید ساخته شد!!!')
            return redirect('ViewPlanProfile2' ,  id=id)
        else:
            print (form.errors)
            sweetify.toast(self.request,timer=30000 , icon="error",title =' برنامه اجرایی جدید ساخته نشد !!!')
            return redirect('ViewPlanProfile2' ,  id=id)
 
    def put(self, request , id = None  , *args, **kwargs):
        
        obj = get_object_or_404(Action,id = id)
        form = CreateFormAction(request.POST or request.FILES,instance=obj)
        if form.is_valid():
            form.save()
            sweetify.toast(self.request,timer=30000 , icon="success",title =' برنامه اجرایی جدید ساخته شد!!!')
            return redirect('ViewPlanProfile' ,  id=id)
        else:
            sweetify.toast(self.request,timer=30000 , icon="error",title =' برنامه اجرایی جدید ساخته نشد !!!')
            return redirect('ViewPlanProfile' ,  id=id)
 
# class CreateViewAction( LoginRequiredMixin,View): 
#     redirect_field_name = '/profile/login'
#     #قالب کلی ایجاد 
#     template_name = "createPlanProfile.html"
#     extend = 'baseEmployee.html'
#     menu_link = 'ViewPlanDashboard'


#     def post(self, request , planProfileId = None  , *args, **kwargs):
#         planProfileSelected = PlanProfile.objects.get(id = planProfileId)
#         form = CreateFormAction( request.POST )
#         #فرم دریافت شده
#         if form.is_valid():
            
            
#             instance = form.save()
#             instance.color = instance.id%5
          
#             instance.save()
#             sweetify.toast(self.request,timer=30000 , icon="success",title =' برنامه اجرایی جدید ساخته شد!!!')
#             return redirect('ViewPlanDashboard' ,  id=id)
#         else:
#             sweetify.toast(self.request,timer=30000 , icon="error",title =' برنامه اجرایی جدید ساخته نشد !!!')
#             return redirect('ViewPlanDashboard' ,  id=id)
class ChangeActionStatus( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detailPlanProfile.html"
    extend = 'baseEmployee.html'

    
    @staff_only 
   
    def post(self, request , actionId = None  , *args, **kwargs):
        actionSelected = Action.objects.get(id = actionId)
        if(actionSelected.status == 'pending'):
            actionSelected.status = 'done'
            sweetify.toast(self.request,timer=30000 , icon="success",title ='فعالیت مورد نظر به اتمام رسید!!!')
        else:
            actionSelected.status = 'pending'
            sweetify.toast(self.request,timer=30000 , icon="success",title ='فعالیت مورد نظر در حال انتظار است  !!!')
        actionSelected.save()
        
        
        return redirect('ViewPlanProfile' ,  id=id)
        
class UpdateViewAction( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(PlanProfile,id = id)
        return obj

    
    def post(self, request , id = None  , *args, **kwargs):
        
        obj = get_object_or_404(Action,id = request.POST.get('id'))
        progress_value = request.POST.get('progress')
        if progress_value == '100':
            obj.progress = 100
            
            obj.status = 'done'
            obj.save()
        else:
            obj.progress = progress_value
            obj.status = 'doing'
            obj.save()


        
        sweetify.toast(self.request,timer=30000 , icon="success",title =' برنامه اجرایی جدید ساخته شد!!!')
        return redirect('ViewPlanProfile2' ,  id=obj.planProfileRelated.id)
        

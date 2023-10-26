from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse
from .forms import CreateFormReportActivityManager
from organization_app.models import    JobBank  ,GetItemsMultiAutoComplete
from django.db.models import Q

from notifications_app.models import Notifications
from event_app.models import Event
from .models import Report ,ReportActivityManager
from profile_app.decorators import  staff_only
from profile_app.models import Profile

from django.views.generic import ListView
import json
from jalali_date.fields import JalaliDateField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from jalali_date import datetime2jalali, date2jalali
from datetime import timedelta
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


class CreateViewReport( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "reportCreate.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormReportActivityManager()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ایجاد درخواست گزارش"
        allJob = JobBank.objects.all()
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک اقدام اصلاحی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #دیکشنری داده ها
        formActivity =  CreateFormReportActivityManager()
        contex = {'extend':self.extend , 'menu_link':self.menu_link, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'form':form , 'allJob':allJob , 'formActivity':formActivity}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        
        jobReciverId = request.POST.get('responsible')
        jobReciverSelected = JobBank.objects.get(id = jobReciverId)
        profileSender  = Profile.objects.filter(user=self.request.user)[0]
        profileReciver  = Profile.objects.filter(user=jobReciverSelected.profile.user)[0]
        titleSelected = request.POST.get('title')
        descriptionSelected = request.POST.get('text')
        referablSelected = request.POST.get('referabl') 
        forwardSelected = request.POST.get('forward') 
        arcaneSelected  = request.POST.get('arcane') 
        
        
        formActivity =  CreateFormReportActivityManager(request.POST,request.FILES)
       
      
        
        #بررسی صحت اطلاعات ورودی
        if formActivity.is_valid():
            f = formActivity.save(commit=False)
            f.sender = profileSender
            f.reciver = profileReciver
            
            instance = Report.objects.create(title=titleSelected,description=descriptionSelected,document = f.document  ,referabl = referablSelected ,forward = forwardSelected ,arcane = arcaneSelected)
            f.document = None
            f.text = None
            f.ReportRelated = instance

            f.save()
            


            Event.objects.create( user =profileReciver , title =titleSelected ,end = f.deadLine , start =f.startTime   )
            
            Notifications.objects.create( title = ' یک درخواست گزارش توسط '  + profileSender.firstName + ' ' + profileSender.lastName + 'برای شما ثبت شده است.' , recivers = profileReciver )
            
            sweetify.toast(self.request,timer=30000 , icon="success",title ='   درخواست گزارش ثبت شد     !!!')
            return redirect('ViewReportDashboard')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='درخواست گزارش ثبت شد  !!!')
        context = {'extend':self.extend,  }
        return render(request,self.template_name,context)


class ListViewReportRequest(ListView):
  


    extend='baseEmployee.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست   گزارشات درخواست شده     "
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
       
       
      
        
        header_table   = ['عنوان' , 'بارگزاری'  , 'ارجاع' , 'ارسال ']
        #اسم داده های جدول
        object_name    = ['title','responsible' , 'meetingType']
        #دریافت تمام داده ها
        profileSelected = Profile.objects.filter(user=self.request.user)[0]
        if(profileSelected.user.is_superuser):
            queryset = ReportActivityManager.objects.all().filter(status='doing')
        else:
            queryset = ReportActivityManager.objects.filter( Q(reciver=profileSelected) & Q(status='doing') )
    
        doing_string =  '<a class="nav-link text-black-80" href="{0}" ><span class=" fw-bold text-dark">انجام دادن</span></a>'
        done_string =  '<a class="nav-link text-black-80" href="{0}" ><span class=" fw-bold text-success">ویرایش کردن </span></a>'
        not_responsible =  '<a class="nav-link text-black-80" href="#" ><span class=" fw-bold text-danger">دسترسی ندارید</span></a>'
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            # if(len(ReportDate.objects.filter(meetingProfileRelated = query)) != 0):
            #     continue
            data = []
            dict_temp = {}
            data.append(query.ReportRelated.title)
            data.append(doing_string.format(reverse('CreateViewReportUpload'  , kwargs={'reportId':query.id})) )
            data.append(not_responsible.format(reverse('CreateViewReport' )) )
            data.append(not_responsible )

            dict_temp = {query.ReportRelated.id : data}
            list_data.append(dict_temp)   
        #دیکشنری داده ها
        context = {'extend':self.extend, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data ,'link_list' : link_list , 'admin_link_list' : admin_link_list   }
        return context

    model = Report
    ordering = '-created_at' 
    template_name ='reportList.html'


class CreateViewReportUpload( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "reportUpload.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    
    def get(self, request , reportId, *args, **kwargs):
        form = CreateFormReportActivityManager()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "  بارگزاری گزارش"
        
        #توضحات نمایش داده شده در زیر عنوان
       
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #دیکشنری داده ها
        activitySelected = ReportActivityManager.objects.get(id = reportId)
        reportSelected = activitySelected.ReportRelated
        contex = {'extend':self.extend , 'menu_link':self.menu_link, 'header_title':header_title,
       'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'form':form , 'reportSelected':reportSelected}
        return render(request,self.template_name,contex)


    def post(self, request ,reportId, *args, **kwargs):
        #فرم دریافت شده
        
     
        request.FILES.get('')
      
        descriptionSelected = request.POST.get('text')
        reportSelected = Report.objects.get(id = reportId)
        reportActivitySelected = ReportActivityManager.objects.get(ReportRelated = reportSelected)  
        x =request.FILES.get('document')
        reportActivitySelected.document = x
        reportActivitySelected.status = 'done'
        reportActivitySelected.save()
        
            
        Notifications.objects.create( title = ' گزارش درخواست شده از '  + reportActivitySelected.reciver.firstName + ' ' + reportActivitySelected.reciver.lastName + 'انجام شده است .'  , recivers =reportActivitySelected.sender )
        sweetify.toast(self.request,timer=30000 , icon="success",title ='   درخواست گزارش ثبت شد     !!!')
        return redirect('ListViewReportDone')
        




class ListViewReportDone(ListView):

  
    extend = 'baseEmployee.html'
    menu_link = 'ViewMomayezi'
    
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "سوابق گزارشات "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام سوال ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = [ 'ردیف' , 'عنوان' , 'تاریخ' ,   ]
        #اسم داده های جدول





        profileSelected = Profile.objects.filter(user=self.request.user)[0]
        
        #دریافت تمام داده ها
        if(profileSelected.user.is_superuser):
            allActivity = ReportActivityManager.objects.all()
        else:
            allActivity = ReportActivityManager.objects.get(Q(reciver =profileSelected ) |Q(sender =profileSelected ) )
        
            
            
      
        queryset = allActivity.filter(status = 'done')
        list_data = []
        counter = 0
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            counter += 1
            data.append(counter)
            data.append(query.ReportRelated.title)
            data.append(datetime2jalali(query.updated_at).strftime('14%y/%m/%d'))
           
  
           
   
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = ReportActivityManager
    ordering = '-created_at' 
    template_name ='listReportReview.html'


class ViewReportReview( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "viewReportReview.html"
    extend = 'baseEmployee.html'
    

    def get(self, request,reportId=None ,*args, **kwargs):

          
       
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ویرایش گزارش ممیزی  "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این گزارش ممیزی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        #رنگ             
        columns       = 1
        #دیکشنری داده ها
        
        ReportActivitySelected = ReportActivityManager.objects.all().filter(id =reportId )[0]
        ProfileReportReviewSelected = ReportActivitySelected.ReportRelated
        
        context =  {'header_title':header_title,'discribtion':discribtion,'icon_name':icon_name,
        'color':color , 'columns':columns ,'extend':self.extend ,'ReportActivitySelected':ReportActivitySelected , 'ProfileReportReviewSelected':ProfileReportReviewSelected,}


        return render(request,self.template_name,context)
    
    

class ViewReportDashboard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "clearDashboard.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
    @staff_only 
    def get(self, request ,*args, **kwargs):
        userProfile = Profile.objects.get(user=self.request.user)
        
        partials = 'partials/reportDashboard.html'
        
        
        
        profileSelected = None
        
        createNewProfile = None
        
        
       
        responsible_link = None
        member_link =  None
        
        # if(jobBankSelected in profileRiskSelected.committeeRisk.members.all()):
        #     member_link = 'ViewRiskDashboardMember'
       
        
        
            
        
        
        
        
        
        
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "داشبورد گزارشات"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        
        
        if(userProfile.user.is_superuser):
            allActivity = ReportActivityManager.objects.all()
        else:
            allActivity = ReportActivityManager.objects.get(Q(reciver =userProfile ) |Q(sender =userProfile ) )
        
            
            
        doingAct =     allActivity.filter(status='doing')
        doneAct = allActivity.filter(status='done')
        lenDoingAct = len(doingAct)
        lenDoneAct = len(doneAct)
        #رنگ             
        columns       = 1
        
        
        
        #رنگ             
        columns       = 1
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack, 'header_title':header_title,'profileSelected':profileSelected,'createNewProfile':createNewProfile,
        'discribtion':discribtion,'icon_name':icon_name,'header_title':header_title,'responsible_link':responsible_link,'member_link':member_link,
        'columns':columns , 'color':color ,'partials':partials, 'doingAct' :doingAct , 'doneAct' : doneAct, 'lenDoingAct' :lenDoingAct , 'lenDoneAct' :lenDoneAct}

        return render(request,self.template_name,context)
    

from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse

from organization_app.models import TypePostSazmani , Vahed , JobBank , Post , Hoze





from profile_app.decorators import  staff_only
from profile_app.models import Profile
from .models import ProfileManagementChange
from django.views.generic import ListView
import json
from django.db.models import Q
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




#تایپ


    

class CreateViewManagementChange( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "managementChangeCreate.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
   
    def get(self, request, *args, **kwargs):
      
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ثبت اطلاعات پایه اقدام اصلاحی"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک اقدام اصلاحی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        allVahed = Vahed.objects.all()
        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menu_link':self.menu_link, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'allVahed':allVahed}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        
        
        
       
        sweetify.toast(self.request,timer=30000 , icon="success",title =' درخواست تغییر  جدید با موفقیت ساخته شد !!!')
        return redirect('ListViewManagementChange')
    
       

class ViewManagementChangeDashboard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "clearDashboard.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
    
    def get(self, request ,*args, **kwargs):
        userProfile = Profile.objects.get(user=self.request.user)
        
        partials = 'partials/managementChangeDashboard.html'
        
        
        
        profileSelected = None
        
        createNewProfile = None
        
        
       
        responsible_link = None
        member_link =  None
        
        # if(jobBankSelected in profileRiskSelected.committeeRisk.members.all()):
        #     member_link = 'ViewRiskDashboardMember'
       
        
        
            
        
        
        
        
        
        
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "داشبورد مدیریت تغییر"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        
        
        if(userProfile.user.is_superuser):
            #allActivity = ReportActivityManager.objects.all()
            pass
        else:
           # allActivity = ReportActivityManager.objects.get(Q(reciver =userProfile ) |Q(sender =userProfile ) )
           pass
        
            
            
    
        #رنگ             
        columns       = 1
        
        
        
        #رنگ             
        columns       = 1
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack, 'header_title':header_title,'profileSelected':profileSelected,'createNewProfile':createNewProfile,
        'discribtion':discribtion,'icon_name':icon_name,'header_title':header_title,'responsible_link':responsible_link,'member_link':member_link,
        'columns':columns , 'color':color ,'partials':partials, }

        return render(request,self.template_name,context)
    





class ListViewManagementChange(ListView):

  
    extend = 'baseEmployee.html'
    menu_link = 'ViewMomayezi'
    
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "سوابق  تغییرات "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام سوال ممیزی  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = [ 'کد' , 'واحد' , 'نوع تغییر' ,  'موضوع تغییر' ]
        #اسم داده های جدول






        #دریافت تمام داده ها
        queryset = ProfileManagementChange.objects.all()
        list_data = []
        counter = 0
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
           
            data.append( 'CH-00' +str(query.id))
            data.append(query.VahedChange.title)
            data.append(query.typeChange)
            data.append(query.subjectChange)




           
  
           
   
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = ProfileManagementChange
    ordering = '-created_at' 
    template_name ='listManagementChange.html'




class ViewMangementChange( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "managementChange.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    
    def get(self, request, id,*args, **kwargs):
    
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "شناسنامه تغییر "
        #توضحات نمایش داده شده در زیر عنوان
        
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
     
        changeData = ProfileManagementChange.objects.all().filter(id = id)[0]

    



        

        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menu_link':self.menu_link, 'header_title':header_title,
        'changeData':changeData,'icon_name':icon_name ,
        'columns' : columns , 'color' : color ,} 
        return render(request,self.template_name,contex)


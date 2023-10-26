from django.shortcuts import render
from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse


from .models import fileProfile



from django.views.generic import ListView


from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from jalali_date import datetime2jalali, date2jalali




from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse


# Create your views here.
# Create your views here.

class CreateViewfileProfile( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createfileProfile.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewPerformanceIndex'
    def get(self, request ,  *args, **kwargs):
        
      
        form = CreateFormfileProfile()
       
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "آپلود فایل"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        allJob = JobBank.objects.all()
        profileList = Profile.objects.all()
           
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color ,  'allJob':allJob , 'form' :form  }
        return render(request,self.template_name,contex)


    def post(self, request , *args, **kwargs):
        #فرم دریافت شده
        jobId = request.POST.getlist('jobSelected')
        jobSelected = JobBank.objects.all().filter(id__in = jobId)
       
        meetingType = request.POST.get('meetingType')
        title = request.POST.get('title')
        responsibleId = request.POST.get('responsible')
        managerId = request.POST.get('manager' or None)
        firstSuccessorId = request.POST.get('firstSuccessor' or None)
        secondSuccessorId = request.POST.get('secondSuccessor' or None)
        responsible = JobBank.get_Job(self , id = responsibleId)
        managerSelected = JobBank.get_Job(self , id = managerId)
        firstSuccessorSelected = JobBank.get_Job(self , id = firstSuccessorId)
        secondSuccessorSelected = JobBank.get_Job(self , id = secondSuccessorId)
        text = request.POST.get('text')
        instanceProfile = fileProfile.objects.create(meetingType = meetingType ,title = title ,responsible = responsible  ,text = text  ,manager=managerSelected ,firstSuccessor=firstSuccessorSelected ,secondSuccessor=secondSuccessorSelected )
        
        instanceProfile.membersPrimary.set(jobSelected)
      
        sweetify.toast(self.request,timer=30000 , icon="success",title ='پروفایل جلسه با موفقیت ساخته شد!!!')
        return redirect('ViewProfileMeeting')
        
        
        #بررسی صحت  ورودی
       
            #تابع نمایش پیغام


class ListViewfileProfile(ListView):
  


    extend='baseEmployee.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "   کتابخانه "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوع پست سازمانی ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
        
        admin_link_list = []
        



        
        #اسم داده های جدول
        
        #دریافت تمام داده ها
        queryset = fileProfile.objects.all()
        
           
        #دیکشنری داده ها
        context = {'extend':self.extend, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 
          'queryset':queryset}
        return context

    model = fileProfile
    ordering = '-created_at' 
    template_name ='listLibrary.html'


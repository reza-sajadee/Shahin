from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse
from organization_app.models import Vahed
from standardTable_app.models import RequirementStandards
from standardTable_app.models import Standard
from .forms import CreateFormMeetingProfile , CreateFormMeetingDate , CreateFormMeeting , CreateFormMeetingDate ,CreateFormMeetingInvitation , CreateFormMeetingAgenda ,CreateFormMeetingEnactment
from .models import TextDataBase  ,BoolDataBase ,ConfirmationDataBase  ,MeetingProfile , MeetingDate , MeetingMember , Meeting  , MeetingInvitation , MeetingAgenda  , MeetingEnactment , Member , MeetingDocument ,MeetingPlan
from organization_app.models import JobBank
from profile_app.models import Profile
from event_app.models import Event
from django.views.generic import ListView
import json
from django.db.models import Q
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from jalali_date import datetime2jalali, date2jalali
from notifications_app.models import Notifications
from messages_app.models import Messages
from datetime import timedelta

from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from formtools.wizard.views import SessionWizardView
from .serializers import MeetingProfileSerializer
# Create your views here.
def load_events(request):
    qs_val = list(MeetingProfile.objects.all())
    
    serializer = MeetingProfileSerializer(qs_val , many=True)
    return JsonResponse( serializer.data,safe=False)

class CreateViewMeetingProfile( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingProfile.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewPerformanceIndex'
    def get(self, request ,  *args, **kwargs):
        
      
        form = CreateFormMeetingProfile()
       
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "انتخاب اعضا اعضاء ثابت  "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        allJob = JobBank.objects.all().filter(~Q(profile = None) )
        profileList = Profile.objects.all()
           
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color ,  'allJob':allJob , 'form' :form  }
        return render(request,self.template_name,contex)


    def post(self, request , *args, **kwargs):
        #فرم دریافت شده
        jobId = request.POST.getlist('jobSelected')
        jobSelected = JobBank.objects.all().filter(~Q(profile = None) ).filter(id__in = jobId)
       
        meetingType = request.POST.get('meetingType')
        title = request.POST.get('title')
        responsibleId = request.POST.get('responsible')
        managerId = request.POST.get('manager' or None)
        firstSuccessorId = request.POST.get('firstSuccessor' or None)
        secondSuccessorId = request.POST.get('secondSuccessor' or None)
        if(responsibleId == ''):
            pass
        else:
            responsible = JobBank.get_Job(self , id = responsibleId)
        
        if(managerId == ''):
            pass
        else:
            managerSelected = JobBank.get_Job(self , id = managerId)
        
        if(firstSuccessorId == ''):
            pass
        else:
            firstSuccessorSelected = JobBank.get_Job(self , id = firstSuccessorId)
        
        if(secondSuccessorId == ''):
            pass
        else:
            secondSuccessorSelected = JobBank.get_Job(self , id = secondSuccessorId)
        
        text = request.POST.get('text')
        instanceProfile = MeetingProfile.objects.create(meetingType = meetingType ,title = title ,responsible = responsible  ,text = text  ,manager=managerSelected ,firstSuccessor=firstSuccessorSelected ,secondSuccessor=secondSuccessorSelected )
        
        instanceProfile.membersPrimary.set(jobSelected)
      
        sweetify.toast(self.request,timer=30000 , icon="success",title ='پروفایل جلسه با موفقیت ساخته شد!!!')
        return redirect('ViewProfileMeeting')
        
        
        #بررسی صحت  ورودی
       
            #تابع نمایش پیغام


class ListViewMeetingProfile(ListView):
  


    extend='baseEmployee.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست   پروفایل جلسات"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوع پست سازمانی ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
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
        if(MeetingProfile.objects.all().filter(responsible__profile =profileSelected ).exists()):
            link_dict = {'title' : ' تعریف جلسه جدید' , 'icon' : 'edit' , 'link' : 'CreateViewMeeting' , 'type':'key' }
            link_list.append(link_dict)



        header_table   = ['عنوان','دبیر' , 'نوع جلسه']
        #اسم داده های جدول
        object_name    = ['title','responsible' , 'meetingType']
        #دریافت تمام داده ها
        queryset = MeetingProfile.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.responsible)
            data.append(query.get_meetingType_display)
            
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data , 'link_list' :link_list}
        return context

    model = MeetingProfile
    ordering = '-created_at' 
    template_name ='listNew.html'


class CreateViewMeeting( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewPerformanceIndex'
    def get(self, request , id ,  *args, **kwargs):
        
        
        form = CreateFormMeeting( initial={ 'meetingProfileRelated' : id})
       
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ایجاد یک جلسه جدید"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
       
      
           
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color  , 'form' :form  }
        return render(request,self.template_name,contex)


    def post(self, request,id , *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormMeeting(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            f = form.save()
            #تابع نمایش پیغام
            meetingProfileSlected = MeetingProfile.objects.get(id = id)
            for member in meetingProfileSlected.membersPrimary.all():
                instanceMember = Member.objects.create( JobBankRelated =member ,meetingRelated =f  )  
            sweetify.toast(self.request,timer=30000 , icon="success",title ='جلسه جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewMeeting')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='جلسه مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'form': form}
        return render(request,self.template_name,context)
        
      
       
        
        #بررسی صحت اطلاعات ورودی
       
            #تابع نمایش پیغام


class DeleteViewMeetingProfile( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend = 'base.html'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MeetingProfile,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک   پروفایل جلسه"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که   پروفایل جلسه  " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend':self.extend,'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend,}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='نوع پست سازمانی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ViewProfileMeeting')
        return render(request,self.template_name,context)
    


class ListViewMeeting(ListView):
  


    extend='baseEmployee.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست   جلسات     "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوع پست سازمانی ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
      
        profileSelected =  Profile.objects.get(user = self.request.user)
        jobSelected = JobBank.objects.get(profile = profileSelected)
        link_list =[]
        admin_link_list = []
       
        if(self.request.user.is_superuser):
            # admin_link_dict = {'title' : 'ویرایش' , 'icon' : "edit" , 'link' : '#' , 'type': 'key' }
            # admin_link_list.append(admin_link_dict)
            pass
        if(Meeting.objects.all().filter(meetingProfileRelated__responsible =jobSelected ).exists()):
            link_dict = {'title' : 'تاریخ و زمان' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingDate' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : 'افزودن اعضا' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingMembers' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : 'دعوت نامه' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingInvitation' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : ' دستور جلسه' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingDate' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : 'درخواست گزارش' , 'icon' : 'edit' , 'link' : 'CreateViewReport' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : 'طرح جلسه' , 'icon' : 'edit' , 'link' : 'CreateViewReport' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : 'صورت جلسه' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingDate' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : ' حاضرین در جلسه' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingDate' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : '  مستندات جلسه' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingDate' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : '   بایگانی' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingDate' , 'type':'key' }
            link_list.append(link_dict)

        
        header_table   = ['عنوان' , 'نوع جلسه']
        #اسم داده های جدول
        object_name    = ['title','responsible' , 'meetingType']
        #دریافت تمام داده ها
        queryset = Meeting.objects.all().filter(meetingProfileRelated__responsible = jobSelected).filter(complate = False)
        doing_string =  '<a class="nav-link text-black-80" href="{0}" ><span class=" fw-bold text-dark">انجام دادن</span></a>'
        done_string =  '<a class="nav-link text-black-80" href="{0}" ><span class=" fw-bold text-success">ویرایش کردن </span></a>'
        not_responsible =  '<a class="nav-link text-black-80" href="#" ><span class=" fw-bold text-danger">دسترسی ندارید</span></a>'
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            # if(len(MeetingDate.objects.filter(meetingProfileRelated = query)) != 0):
            #     continue
            data = []
            dict_temp = {}
            data.append(query.title)
           
            data.append(query.meetingProfileRelated.get_meetingType_display)
            #تاریخ و زمان
            if(MeetingDate.objects.all().filter(meetingRelated = query ).exists()):
                data.append(done_string.format(reverse('CreateViewMeetingDate' , kwargs={'meetingId':query.id})) )
            else:
                data.append(doing_string.format(reverse('CreateViewMeetingDate' , kwargs={'meetingId':query.id})) )
            #افزودن اعضا
            if(MeetingMember.objects.all().filter(meetingRelated = query ).exists()):
                data.append(done_string.format(reverse('CreateViewMeetingMembers' , kwargs={'meetingId':query.id})) )
            else:
                data.append(doing_string.format(reverse('CreateViewMeetingMembers' , kwargs={'meetingId':query.id})) )
            #دعوت نامه
            if(MeetingInvitation.objects.all().filter(meetingRelated = query ).exists()):
                data.append(done_string.format(reverse('CreateViewMeetingInvitation' , kwargs={'meetingId':query.id})) )
            else:
                data.append(doing_string.format(reverse('CreateViewMeetingInvitation' , kwargs={'meetingId':query.id})) )
            #دستور جلسه
            if(MeetingAgenda.objects.all().filter(meetingRelated = query ).exists()):
                data.append(done_string.format(reverse('CreateViewMeetingAgenda' , kwargs={'meetingId':query.id})) )
            else:
                data.append(doing_string.format(reverse('CreateViewMeetingAgenda' , kwargs={'meetingId':query.id})) )
            #درخواست گزارش
            data.append(doing_string.format(reverse('CreateViewReport') ))
            #طرح جلسه
            if(MeetingPlan.objects.all().filter(meetingRelated = query ).exists()):
                data.append(done_string.format(reverse('CreateViewMeetingPlan' , kwargs={'meetingId':query.id})) )
            else:
                data.append(doing_string.format(reverse('CreateViewMeetingPlan' , kwargs={'meetingId':query.id})) )
            #صورت جلسه
            if(MeetingEnactment.objects.all().filter(meetingRelated = query ).exists()):
                data.append(done_string.format(reverse('CreateViewMeetingEnactment' , kwargs={'meetingId':query.id})) )
            else:
                data.append(doing_string.format(reverse('CreateViewMeetingEnactment' , kwargs={'meetingId':query.id})) )
            #حاضرین در جلسه                
            if(MeetingMember.objects.all().filter(meetingRelated = query ).exists()):
        
                if(MeetingMember.objects.all().filter(meetingRelated = query )[0].compated):
                    data.append(done_string.format(reverse('CreateViewMeetingMinute' , kwargs={'meetingId':query.id})) )
                else:
                    data.append(doing_string.format(reverse('CreateViewMeetingMinute' , kwargs={'meetingId':query.id})) )                
            else:
                data.append(doing_string.format(reverse('CreateViewMeetingMinute' , kwargs={'meetingId':query.id})) )                
            #مستندات
            if(MeetingDocument.objects.all().filter(meetingRelated = query ).exists()):
                data.append(done_string.format(reverse('CreateViewMeetingDocument' , kwargs={'meetingId':query.id})) )
            else:
                data.append(doing_string.format(reverse('CreateViewMeetingDocument' , kwargs={'meetingId':query.id})) )                
            
            data.append(doing_string.format(reverse('CreateViewMeetingComplate' , kwargs={'meetingId':query.id})) )
            
            
           
            
            
            

            dict_temp = {query.id : data}
            list_data.append(dict_temp)   
        #دیکشنری داده ها
        context = {'extend':self.extend, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data ,'link_list' : link_list , 'admin_link_list' : admin_link_list   }
        return context

    model = MeetingProfile
    ordering = '-created_at' 
    template_name ='meetingList.html'



class CreateViewMeetingDate( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingDate.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewPerformanceIndex'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MeetingDate,id = id)
        return obj

    def get(self, request , meetingId ,  *args, **kwargs):
        
      
        if(len(MeetingDate.objects.all().filter(meetingRelated__id = meetingId)) >0):
            obj = MeetingDate.objects.all().filter(meetingRelated__id = meetingId)[0]
            form = CreateFormMeetingDate(instance=obj)
        else:
            form = CreateFormMeetingDate()
        
        
            
       
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "تنظیم تاریخ جلسه"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
     
        try:
            meetingSelectedDate = MeetingDate.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedDate = None
        try:
            meetingSelectedMembers = MeetingMember.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedMembers = None
        try:
            meetingSelectedAgendas = MeetingAgenda.objects.all().filter(meetingRelated = meetingSelected)
        except:
            meetingSelectedAgendas = None
        try:
            allEnactment = MeetingEnactment.objects.all().filter(meetingRelated = meetingSelected)
        except:
            allEnactment = None
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'meetingSelected':meetingSelected  , 'form':form , 'meetingSelectedDate':meetingSelectedDate , 'meetingSelectedDate' :meetingSelectedDate ,'meetingSelectedMembers' :meetingSelectedMembers , 'meetingSelectedAgendas' :meetingSelectedAgendas  , 'allEnactment':allEnactment}
        return render(request,self.template_name,contex)


    def post(self, request , meetingId , *args, **kwargs):
        if(len(MeetingDate.objects.all().filter(meetingRelated__id = meetingId)) >0):
            obj = MeetingDate.objects.all().filter(meetingRelated__id = meetingId)[0]
            form = CreateFormMeetingDate(request.POST or request.FILES,instance=obj)
        else:
            form = CreateFormMeetingDate( request.POST )
        #فرم دریافت شده
        if form.is_valid():

            instance = form.save(commit=False)
            instance.meetingRelated = Meeting.objects.get(id =meetingId )
            instance.save()
            sweetify.toast(self.request,timer=30000 , icon="success",title =' تاریخ و زمان جلسه با موفقیت ثبت شد    !!!')
            return redirect('ListViewMeeting')
        else:
            sweetify.toast(self.request,timer=30000 , icon="error",title =' تاریخ و زمان جلسه   ثبت نشد    !!!')
            return redirect('ListViewMeeting')


class CreateViewMeetingMembers( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingMembers.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewPerformanceIndex'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MeetingMember,id = id)
        return obj

    def get(self, request , meetingId ,  *args, **kwargs):
        
        membersSecondary = []
        membersOther = ''
        allJob = []
        if(len(MeetingMember.objects.all().filter(meetingRelated__id = meetingId)) >0):
            obj = MeetingMember.objects.all().filter(meetingRelated__id = meetingId)[0]
            membersSecondary = obj.membersSecondary
            membersOther = obj.membersOther
            for job in JobBank.objects.all().filter(~Q(profile = None) ):
                if(job in membersSecondary.all()):
                    allJob.append((job , 1))
                else:
                    allJob.append((job , 0))
        else:
            for job in JobBank.objects.all().filter(~Q(profile = None) ):
                
                allJob.append((job , 0))
            
        
        
       
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "اغضای  جلسه"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        try:
            meetingSelectedDate = MeetingDate.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedDate = None
        try:
            meetingSelectedMembers = MeetingMember.objects.get(meetingRelated = meetingSelected )
            otherMember  = MeetingMember.objects.get(meetingRelated = meetingSelected )
            
        except:
            meetingSelectedMembers = None
            otherMember = None
        
        try:
            meetingSelectedAgendas = MeetingAgenda.objects.all().filter(meetingRelated = meetingSelected)
        except:
            meetingSelectedAgendas = None
        try:
            allEnactment = MeetingEnactment.objects.all().filter(meetingRelated = meetingSelected)
        except:
            allEnactment = None
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'meetingSelected':meetingSelected   , 'meetingSelectedDate':meetingSelectedDate ,'allJob' : allJob , 'membersOther':membersOther , 'meetingSelectedMembers' : meetingSelectedMembers , 'meetingSelectedAgendas' : meetingSelectedAgendas , 'otherMember':otherMember , 'allEnactment' :allEnactment }
        return render(request,self.template_name,contex)


    def post(self, request , meetingId , *args, **kwargs):
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        if(len(MeetingMember.objects.all().filter(meetingRelated__id = meetingId)) >0):
            obj = MeetingMember.objects.all().filter(meetingRelated__id = meetingId)[0]
            jobId = request.POST.getlist('jobSelected')
            jobSelected = JobBank.objects.all().filter(~Q(profile = None) ).filter(id__in = jobId)
            membersOther = request.POST.get('membersOther')
            obj.membersOther = membersOther
            obj.membersSecondary.set(jobSelected)
            obj.save()
            sweetify.toast(self.request,timer=30000 , icon="success",title =' اعضا فرعی و سایر اعضا   جلسه با موفقیت ثبت شد    !!!')
            return redirect('ListViewMeeting')
        else:
            jobId = request.POST.getlist('jobSelected')
            jobSelected = JobBank.objects.all().filter(~Q(profile = None) ).filter(id__in = jobId)
            membersOther = request.POST.get('membersOther')
            instance = MeetingMember.objects.create(meetingRelated = meetingSelected ,membersOther =membersOther  )
            for member in jobSelected.all():
                instanceMember = Member.objects.create(meetingRelated = meetingSelected ,JobBankRelated =member  )
                instanceMember.save()
            allMember = Member.objects.all().filter(meetingRelated = meetingSelected)
            instance.membersSecondary.set(allMember)
            instance.save()
            sweetify.toast(self.request,timer=30000 , icon="success",title =' اعضا فرعی و سایر اعضا   جلسه با موفقیت ثبت شد    !!!')
            return redirect('ListViewMeeting')
        #فرم دریافت شده
      
           


class CreateViewMeetingInvitation( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingInvitation.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewProfileMeeting'
  

    def get(self, request , meetingId ,  *args, **kwargs):
        
      
        if(len(MeetingInvitation.objects.all().filter(meetingRelated__id = meetingId)) >0):
            obj = MeetingInvitation.objects.all().filter(meetingRelated__id = meetingId)[0]
            form = CreateFormMeetingInvitation(instance=obj)
        else:
            form = CreateFormMeetingInvitation()
            
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        try:
            meetingSelectedDate = MeetingDate.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedDate = None
        try:
            meetingSelectedMembers = MeetingMember.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedMembers = None
        try:
            meetingSelectedAgendas = MeetingAgenda.objects.all().filter(meetingRelated = meetingSelected)
        except:
            meetingSelectedAgendas = None
        try:
            allEnactment = MeetingEnactment.objects.all().filter(meetingRelated = meetingSelected)
        except:
            allEnactment = None    
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ارسال دعوت نامه جلسه"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'meetingSelected':meetingSelected  , 'form':form , 'meetingSelectedDate' :meetingSelectedDate , 'meetingSelectedMembers' :meetingSelectedMembers , 'meetingSelectedAgendas' :meetingSelectedAgendas , 'allEnactment': allEnactment}
        return render(request,self.template_name,contex)


    def post(self, request , meetingId , *args, **kwargs):
        if(len(MeetingInvitation.objects.all().filter(meetingRelated__id = meetingId)) >0):
            obj = MeetingInvitation.objects.all().filter(meetingRelated__id = meetingId)[0]
            form = CreateFormMeetingInvitation(request.POST or request.FILES,instance=obj)
        else:
            form = CreateFormMeetingInvitation( request.POST )
        #فرم دریافت شده
        if form.is_valid():

            instance = form.save(commit=False)
            instance.meetingRelated = Meeting.objects.get(id =meetingId )
            instance.save()
            profileSender =  Profile.objects.get(user = self.request.user)
            meetingProfileSelected = instance.meetingRelated.meetingProfileRelated
            meetingSelected = instance.meetingRelated
            membersPrimary = meetingProfileSelected.membersPrimary.all()
         

            membersSecondery = MeetingMember.objects.get(meetingRelated__id = meetingId).membersSecondary.all()
            for member in membersPrimary:
                instanceMsg = Messages.objects.create(title = instance.title ,description =instance.text  ,reciver = member.profile ,sender = profileSender , link = '#',)
                instanceMsg.save()
            for member in membersSecondery:
                instanceMsg = Messages.objects.create(title = instance.title ,description =instance.text  ,reciver = member.JobBankRelated.profile ,sender = profileSender , link = '#',)
                instanceMsg.save()
            #asd
            sweetify.toast(self.request,timer=30000 , icon="success",title ='    دعوت نامه جلسه با موفقیت ثبت شد    !!!')
            return redirect('ViewProfileMeeting')
           

class CreateViewMeetingAgenda( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingAgenda.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewProfileMeeting'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MeetingInvation,id = id)
        return obj

    def get(self, request , meetingId ,  *args, **kwargs):
        
      
        
            
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        try:
            meetingSelectedDate = MeetingDate.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedDate = None
        try:
            meetingSelectedMembers = MeetingMember.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedMembers = None
        try:
            meetingSelectedAgendas = MeetingAgenda.objects.all().filter(meetingRelated = meetingSelected)
        except:
            meetingSelectedAgendas = None
        try:
            allEnactment = MeetingEnactment.objects.all().filter(meetingRelated = meetingSelected)
        except:
            allEnactment = None 
        allAgenda = MeetingAgenda.objects.all().filter(meetingRelated  = meetingSelected)
        form = CreateFormMeetingAgenda()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "تعریف دستور جلسه"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'meetingSelected':meetingSelected  , 'meetingSelectedDate' :meetingSelectedDate , 'meetingSelectedMembers' :meetingSelectedMembers , 'allAgenda':allAgenda , 'form':form , 'meetingSelectedAgendas':meetingSelectedAgendas , 'allEnactment' : allEnactment}
        return render(request,self.template_name,contex)


    def post(self, request , meetingId , *args, **kwargs):
        if(len(MeetingInvitation.objects.all().filter(meetingRelated__id = meetingId)) >0):
            obj = MeetingInvitation.objects.all().filter(meetingRelated__id = meetingId)[0]
            form = CreateFormMeetingInvitation(request.POST or request.FILES,instance=obj)
        else:
            form = CreateFormMeetingInvitation( request.POST )
        #فرم دریافت شده
        if form.is_valid():

            instance = form.save(commit=False)
            instance.meetingRelated = Meeting.objects.get(id =meetingId )
            instance.save()
            sweetify.toast(self.request,timer=30000 , icon="success",title ='    دعوت نامه جلسه با موفقیت ثبت شد    !!!')
            return redirect('ViewProfileMeeting')
           
def add_enactment(request):
    meetingRelatedId = request.POST.get('meetingRelated')
    meetingRelatedSelected = Meeting.objects.get(id =meetingRelatedId )
    responsibleExecutiveId = request.POST.get('responsibleExecutive')
    responsibleExecutive = JobBank.objects.get(id = responsibleExecutiveId)
    responsibleFollowId = request.POST.get('responsibleFollow')
    responsibleFollow = JobBank.objects.get(id = responsibleFollowId)
    titleSelected = request.POST.get('title')
    
    form = CreateFormMeetingEnactment(request.POST)
    daedLine = ''
    if(form.is_valid()):
        f = form.save(commit=False)
        deadLine =f.deadLine
        print(daedLine , 'daedLine')
        instance =  MeetingEnactment.objects.create( meetingRelated = meetingRelatedSelected , title = titleSelected, responsibleExecutive =responsibleExecutive , responsibleFollow= responsibleFollow ,  deadLine= deadLine )
        instance.save()
    else:
        asdasdasd
    
   
    
    
    allEnactment = MeetingEnactment.objects.all().filter(meetingRelated = meetingRelatedSelected)
    
    return render(request , 'partials/enactment-list.html' ,{ 'allEnactment' : allEnactment} )

class CreateViewMeetingMinute( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingMinute.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewProfileMeeting'
    

    def get(self, request , meetingId ,  *args, **kwargs):
        
      
        
            
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        try:
            meetingSelectedDate = MeetingDate.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedDate = None
        try:
            meetingSelectedMembers = MeetingMember.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedMembers = None
        try:
            meetingSelectedAgendas = MeetingAgenda.objects.all().filter(meetingRelated = meetingSelected)
        except:
            meetingSelectedAgendas = None
        allMember = []
        for memberJob in meetingSelected.meetingProfileRelated.membersPrimary.all():
            allMember.append(memberJob)
        allMember = []
        for memberJob in Member.objects.all().filter(meetingRelated =meetingSelected ):
            
            allMember.append(memberJob)
        
        allAgenda = MeetingAgenda.objects.all().filter(meetingRelated  = meetingSelected)
        allEnactment = MeetingEnactment.objects.all().filter(meetingRelated  = meetingSelected)
        form = CreateFormMeetingAgenda()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "تعریف صورت جلسه"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'meetingSelected':meetingSelected  , 'meetingSelectedDate' :meetingSelectedDate , 'meetingSelectedMembers' :meetingSelectedMembers , 'allAgenda':allAgenda , 'form':form , 'meetingSelectedAgendas':meetingSelectedAgendas , 'allMember':allMember , 'allEnactment':allEnactment}
        return render(request,self.template_name,contex)


    def post(self, request , meetingId , *args, **kwargs):
        # if(len(MeetingInvitation.objects.all().filter(meetingRelated__id = meetingId)) >0):
        #     obj = MeetingInvitation.objects.all().filter(meetingRelated__id = meetingId)[0]
        #     form = CreateFormMeetingInvitation(request.POST or request.FILES,instance=obj)
        # else:
        #     form = CreateFormMeetingInvitation( request.POST )
        jobId = request.POST.getlist('jobSelected')
        jobSelected = JobBank.objects.all().filter(~Q(profile = None) ).filter(id__in = jobId)
        
        meetingMembers = Member.objects.all().filter(meetingRelated=meetingId)
        
        for member in meetingMembers:
            if(member.JobBankRelated.id in jobId):
                member.present = True
                member.save()
        meetingSelected = MeetingMember.objects.all().filter(meetingRelated=meetingId)[0]
        meetingSelected.compated = True
        meetingSelected.save()
        #فرم دریافت شده
        # if form.is_valid():

        #     instance = form.save(commit=False)
        #     instance.meetingRelated = Meeting.objects.get(id =meetingId )
        #     instance.save()
        sweetify.toast(self.request,timer=30000 , icon="success",title ='    دعوت نامه جلسه با موفقیت ثبت شد    !!!')
        return redirect('ViewProfileMeeting')
           

class CreateViewMeetingEnactment( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingEnactment.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewProfileMeeting'
    

    def get(self, request , meetingId ,  *args, **kwargs):
        
      
        allJob = JobBank.objects.all().filter(~Q(profile = None) )
            
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        try:
            meetingSelectedDate = MeetingDate.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedDate = None
        try:
            meetingSelectedMembers = MeetingMember.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedMembers = None
        try:
            meetingSelectedAgendas = MeetingAgenda.objects.all().filter(meetingRelated = meetingSelected)
        except:
            meetingSelectedAgendas = None
        allMember = []
        for memberJob in meetingSelected.meetingProfileRelated.membersPrimary.all():
            allMember.append(memberJob)
        if(meetingSelectedMembers!=None):
            for memberJob in meetingSelectedMembers.membersSecondary.all():
                if(memberJob in allMember):
                    continue
                
                allMember.append(memberJob)
        
        allAgenda = MeetingAgenda.objects.all().filter(meetingRelated  = meetingSelected)
        allEnactment = MeetingEnactment.objects.all().filter(meetingRelated  = meetingSelected)
        form = CreateFormMeetingEnactment()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "تعریف صورت جلسه"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'meetingSelected':meetingSelected  , 'meetingSelectedDate' :meetingSelectedDate , 'meetingSelectedMembers' :meetingSelectedMembers , 'allAgenda':allAgenda , 'form':form , 'meetingSelectedAgendas':meetingSelectedAgendas , 'allMember':allMember , 'allEnactment':allEnactment , 'allJob':allJob}
        return render(request,self.template_name,contex)


    def post(self, request , meetingId , *args, **kwargs):
        if(len(MeetingInvitation.objects.all().filter(meetingRelated__id = meetingId)) >0):
            obj = MeetingInvitation.objects.all().filter(meetingRelated__id = meetingId)[0]
            form = CreateFormMeetingInvitation(request.POST or request.FILES,instance=obj)
        else:
            form = CreateFormMeetingInvitation( request.POST )
        #فرم دریافت شده
        if form.is_valid():

            instance = form.save(commit=False)
            instance.meetingRelated = Meeting.objects.get(id =meetingId )
            instance.save()
            sweetify.toast(self.request,timer=30000 , icon="success",title ='    دعوت نامه جلسه با موفقیت ثبت شد    !!!')
            return redirect('ViewProfileMeeting')
           

class CreateViewMeetingDocument( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingDocument.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewProfileMeeting'
    

    def get(self, request , meetingId ,  *args, **kwargs):
        
      
        allJob = JobBank.objects.all().filter(~Q(profile = None) )
            
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        try:
            meetingSelectedDate = MeetingDate.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedDate = None
        try:
            meetingSelectedMembers = MeetingMember.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedMembers = None
        try:
            meetingSelectedAgendas = MeetingAgenda.objects.all().filter(meetingRelated = meetingSelected)
        except:
            meetingSelectedAgendas = None
        try:
            meetingSelectedDocument = MeetingDocument.objects.all().filter(meetingRelated = meetingSelected)[0]
        except:
            meetingSelectedDocument = None
        allMember = []
        for memberJob in meetingSelected.meetingProfileRelated.membersPrimary.all():
            allMember.append(memberJob)
        for memberJob in meetingSelectedMembers.membersSecondary.all():
            if(memberJob in allMember):
                continue
            allMember.append(memberJob)
        
        allAgenda = MeetingAgenda.objects.all().filter(meetingRelated  = meetingSelected)
        allEnactment = MeetingEnactment.objects.all().filter(meetingRelated  = meetingSelected)
        form = CreateFormMeetingEnactment()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "تعریف صورت جلسه"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'meetingSelected':meetingSelected  , 'meetingSelectedDate' :meetingSelectedDate , 'meetingSelectedMembers' :meetingSelectedMembers , 'allAgenda':allAgenda , 'form':form , 'meetingSelectedAgendas':meetingSelectedAgendas , 'allMember':allMember , 'allEnactment':allEnactment , 'allJob':allJob , 'meetingSelectedDocument':meetingSelectedDocument}
        return render(request,self.template_name,contex)


    def post(self, request , meetingId , *args, **kwargs):
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        
        if(len(request.FILES)!=0):
            
            if(MeetingDocument.objects.all().filter(meetingRelated = meetingSelected).exists()):
            # if(MeetingMinute.objects.all().filter(meetingRelated = meetingSelected).exists()):
                MeetingDocumentSelected = MeetingDocument.objects.all().filter(meetingRelated = meetingSelected)[0]
                persentDocumentUploaded = request.FILES['persentDocument']
                minuteDocumentUploaded = request.FILES['minuteDocument']
                MeetingDocumentSelected.persentDocument = persentDocumentUploaded
                MeetingDocumentSelected.minuteDocument = minuteDocumentUploaded
                MeetingDocumentSelected.save()
            else:
                instanceDocument = MeetingDocument.objects.create(meetingRelated = meetingSelected, persentDocument = request.FILES['persentDocument'] , minuteDocument = request.FILES['minuteDocument'] )
                instanceDocument.save()

               
            sweetify.toast(self.request,timer=30000 , icon="success",title ='      فایل های جلسه با موفقیت بارگزاری شد !!!')
            return redirect('ViewProfileMeeting')
        #فرم دریافت شده
        else:
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='          فایلی یافت نشد    !!!')
            return redirect('ViewProfileMeeting')
           

class CreateViewMeetingPlan( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingPlan.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewProfileMeeting'
    

    def get(self, request , meetingId ,  *args, **kwargs):
        
      
        allJob = JobBank.objects.all().filter(~Q(profile = None) )
            
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        try:
            meetingSelectedDate = MeetingDate.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedDate = None
        try:
            meetingSelectedMembers = MeetingMember.objects.get(meetingRelated = meetingSelected )
        except:
            meetingSelectedMembers = None
        try:
            meetingSelectedAgendas = MeetingAgenda.objects.all().filter(meetingRelated = meetingSelected)
        except:
            meetingSelectedAgendas = None
        try:
            meetingSelectedDocument = MeetingDocument.objects.all().filter(meetingRelated = meetingSelected)[0]
        except:
            meetingSelectedDocument = None
        allMember = []
        for memberJob in meetingSelected.meetingProfileRelated.membersPrimary.all():
            allMember.append(memberJob)
        for memberJob in meetingSelectedMembers.membersSecondary.all():
            if(memberJob in allMember):
                continue
            allMember.append(memberJob)
        
        allAgenda = MeetingAgenda.objects.all().filter(meetingRelated  = meetingSelected)
        allEnactment = MeetingEnactment.objects.all().filter(meetingRelated  = meetingSelected)
        form = CreateFormMeetingEnactment()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "بارگزاری طرح  جلسه"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'meetingSelected':meetingSelected  , 'meetingSelectedDate' :meetingSelectedDate , 'meetingSelectedMembers' :meetingSelectedMembers , 'allAgenda':allAgenda , 'form':form , 'meetingSelectedAgendas':meetingSelectedAgendas , 'allMember':allMember , 'allEnactment':allEnactment , 'allJob':allJob , 'meetingSelectedDocument':meetingSelectedDocument}
        return render(request,self.template_name,contex)


    def post(self, request , meetingId , *args, **kwargs):
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        
        if(len(request.FILES)!=0):
            
            if(MeetingPlan.objects.all().filter(meetingRelated = meetingSelected).exists()):
            
                MeetingPlanSelected = MeetingDocument.objects.all().filter(meetingRelated = meetingSelected)[0]
                planDocumentUploaded = request.FILES['planDocument']
           
                MeetingPlanSelected.planDocument = planDocumentUploaded
                
                MeetingPlanSelected.save()
            else:
                instancePlan = MeetingPlan.objects.create(meetingRelated = meetingSelected, planDocument = request.FILES['planDocument'] )
                instancePlan.save()

               
            sweetify.toast(self.request,timer=30000 , icon="success",title ='      فایل های جلسه با موفقیت بارگزاری شد !!!')
            return redirect('ViewProfileMeeting')
        #فرم دریافت شده
        else:
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='          فایلی یافت نشد    !!!')
            return redirect('ViewProfileMeeting')
           

class CreateViewMeetingComplate( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingPlan.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewProfileMeeting'
    

    def get(self, request , meetingId ,  *args, **kwargs):
        
      
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        meetingSelected.complate = True
        meetingSelected.save()
        sweetify.toast(self.request,timer=30000 , icon="success",title ='    جلسه با موفقیت بایگانی شد !!!')
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend , 
        }
        return redirect('ViewProfileMeeting')


        
def add_agenda(request):
    meetingRelatedId = request.POST.get('meetingRelated')
    meetingRelatedSelected = Meeting.objects.get(id =meetingRelatedId )
    title = request.POST.get('title')
    text = request.POST.get('text')
    timeDuration = request.POST.get('timeDuration')
    print(request.POST)
    responsibleId = request.POST.get('responsible')
    responsibleSelected = JobBank.objects.get(id = responsibleId)
    instance =  MeetingAgenda.objects.create( meetingRelated = meetingRelatedSelected , title = title, text = text,timeDuration = timeDuration , responsible = responsibleSelected )
    instance.save()
    allAgenda = MeetingAgenda.objects.all().filter(meetingRelated = meetingRelatedSelected)
    
    return render(request , 'partials/agenda-list.html' ,{ 'allAgenda' : allAgenda} )
class UpdateViewMeetingDate( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'baseEmnployee.html'
    template_name = "create.html"
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MeetingDate,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormMeetingDate(instance=obj)
            
            obj = get_object_or_404(MeetingDate,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش نقطه قوت  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این نقطه قوت  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns ,'extend':self.extend ,}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormMeetingDate(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='نقطه قوت  جدید با موفقیت ساخته شد !!!')
                return redirect('MomayeziListViewMeeting')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='نقطه قوت  مورد نظر ساخته نشد !')           
            context = {'form': form,'object':obj ,'extend':self.extend ,}
        return render(request,self.template_name,context)


class ListViewMeetingReview(ListView):

  
    extend = 'baseEmployee.html'
    menu_link = 'ViewMomayezi'
    
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست جلسات  "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام سوال ممیزی  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = [ 'ردیف' , 'عنوان' , 'تاریخ' ,   ]
        #اسم داده های جدول


        x = self.request.GET.get('type')

       



        #دریافت تمام داده ها
        if(x !=None):
            queryset = Meeting.objects.all().filter(complate=True).filter(meetingProfileRelated__meetingType = 'review')
        else:
            queryset = Meeting.objects.all().filter(complate=True)
        list_data = []
        counter = 0
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            counter += 1
            data.append(counter)
            data.append(query.title)
            data.append(datetime2jalali(query.updated_at).strftime('14%y/%m/%d'))
           
  
           
   
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = Meeting
    ordering = '-created_at' 
    template_name ='listMeetingReview.html'




class ViewMeetingtReview( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "viewMeetingReview.html"
    extend = 'baseEmployee.html'
    

    def get(self, request,meetingId=None ,*args, **kwargs):

          
       
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
        peresents = Member.objects.all().filter(meetingRelated = meetingId).filter(present=True)
        
        absents = Member.objects.all().filter(meetingRelated = meetingId).filter(present=False)
        MeetingDateSelected = MeetingDate.objects.all().filter(meetingRelated = meetingId)[0]
        #endTime = datetime.timedelta(seconds=0) + datetime.timedelta(seconds=15) + datetime.timedelta(MeetingDateSelected.meetingTime.second)
        startTime = '{:02}:{:02}'.format(MeetingDateSelected.meetingTime.hour, MeetingDateSelected.meetingTime.minute )
        endTime = '{:02}:{:02}'.format(MeetingDateSelected.meetingTime.hour + MeetingDateSelected.meetingTimeDuration.hour, MeetingDateSelected.meetingTime.minute + MeetingDateSelected.meetingTimeDuration.minute)
        MeetingSelected = Meeting.objects.all().filter(id = meetingId)[0]
        MeetingProfileSelected = MeetingSelected.meetingProfileRelated
        MeetingInvitationSelected = MeetingInvitation.objects.all().filter(meetingRelated = meetingId)[0]
        MeetingAgendaSelected = MeetingAgenda.objects.all().filter(meetingRelated = meetingId)
        MeetingEnactmentSelected = MeetingEnactment.objects.all().filter(meetingRelated = meetingId)
        MeetingDocumentSelected = MeetingDocument.objects.all().filter(meetingRelated = meetingId)[0]
        MeetingPlanSelected = MeetingPlan.objects.all().filter(meetingRelated = meetingId)[0]
        
        
        
        context =  {'header_title':header_title,'discribtion':discribtion,'icon_name':icon_name,
        'color':color , 'columns':columns ,'extend':self.extend , 'peresents' : peresents,'absents' : absents , 'MeetingDateSelected' : MeetingDateSelected,'MeetingProfileSelected' : MeetingProfileSelected ,'MeetingSelected' : MeetingSelected ,'MeetingInvitationSelected' : MeetingInvitationSelected , 'MeetingAgendaSelected' : MeetingAgendaSelected,'MeetingEnactmentSelected' : MeetingEnactmentSelected ,'MeetingDocumentSelected' : MeetingDocumentSelected ,'MeetingPlanSelected' : MeetingPlanSelected , 'endTime':endTime , 'startTime':startTime}


        return render(request,self.template_name,context)
       
        
   

class ViewMeetingDashboard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "clearDashboard.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
    
    def get(self, request ,*args, **kwargs):
        userProfile = Profile.objects.get(user=self.request.user)
        
        partials = 'partials/meetingDashboard.html'
        
        
        
        profileSelected = None
        
        createNewProfile = None
        
        
       
        responsible_link = None
        member_link =  None
        
        # if(jobBankSelected in profileRiskSelected.committeeRisk.members.all()):
        #     member_link = 'ViewRiskDashboardMember'
       
        
        
            
        
        
        
        
        
        
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "داشبورد جلسات"
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
    

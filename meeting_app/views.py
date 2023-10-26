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
from project_app.models import PlanProfile
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from formtools.wizard.views import SessionWizardView
from .serializers import MeetingProfileSerializer
from report_app.models import Report , ReportActivityManager
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
        header_title  = "انتخاب اعضاء ثابت  "
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
            responsible = None
        else:
            responsible = JobBank.get_Job(self , id = responsibleId)
        
        if(managerId == ''):
            managerSelected = None
        else:
            managerSelected = JobBank.get_Job(self , id = managerId)
        
        if(firstSuccessorId == ''):
            firstSuccessorSelected = None
        else:
            firstSuccessorSelected = JobBank.get_Job(self , id = firstSuccessorId)
        
        if(secondSuccessorId == ''):
            secondSuccessorSelected = None
        else:
            secondSuccessorSelected = JobBank.get_Job(self , id = secondSuccessorId)
        
        text = request.POST.get('text')
        instanceProfile = MeetingProfile.objects.create(meetingType = meetingType ,title = title ,responsible = responsible  ,text = text  ,manager=managerSelected ,firstSuccessor=firstSuccessorSelected ,secondSuccessor=secondSuccessorSelected )
        
        instanceProfile.membersPrimary.set(jobSelected)
      
        sweetify.toast(self.request,timer=30000 , icon="success",title ='پروفایل جلسه با موفقیت ساخته شد!!!')
        return redirect('ViewMeetingDashboard')
        
        
        #بررسی صحت  ورودی
       
            #تابع نمایش پیغام


class ListViewMeetingProfile(ListView):
  


    extend='baseEmployee.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست   پروفایل جلسات"
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
        if(MeetingProfile.objects.all().filter(responsible__profile =profileSelected ).exists() or self.request.user.is_superuser):
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
            data.append(str(query.responsible.profile.firstName) + " " + str(query.responsible.profile.lastName))
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
                instanceMember = Member.objects.create( JobBankRelated =member ,meetingRelated =f )  
                
            sweetify.toast(self.request,timer=30000 , icon="success",title ='جلسه جدید با موفقیت ساخته شد !!!')
            return redirect('ViewMeetingDashboard')
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
            discribtion   = "آیا می خواهید که   پروفایل جلسه  " + obj.title + " "  + " را پاک کنید   ؟"
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
        discribtion   = "در این بخش لیست تمام نوع پست سازمانی ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
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
        if(Meeting.objects.all().filter(meetingProfileRelated__responsible =jobSelected ).exists() or self.request.user.is_superuser):
            link_dict = {'title' : 'تاریخ و زمان' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingDate' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : 'افزودن اعضا' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingMembers' , 'type':'key' }
            link_list.append(link_dict)
            
            link_dict = {'title' : ' دستور جلسه' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingDate' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : 'دعوت به جلسه' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingInvitation' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : 'درخواست گزارش' , 'icon' : 'edit' , 'link' : 'CreateViewReport' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : 'فایل ارائه جلسه' , 'icon' : 'edit' , 'link' : 'CreateViewReport' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : 'صورت جلسه' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingDate' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : ' حاضرین در جلسه' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingDate' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : '  فایل صورت جلسه' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingDate' , 'type':'key' }
            link_list.append(link_dict)
            link_dict = {'title' : '   بایگانی' , 'icon' : 'edit' , 'link' : 'CreateViewMeetingDate' , 'type':'key' }
            link_list.append(link_dict)

        
        header_table   = ['عنوان' , 'نوع جلسه']
        #اسم داده های جدول
        object_name    = ['title','responsible' , 'meetingType']
        #دریافت تمام داده ها
        if(self.request.user.is_superuser):
            queryset = Meeting.objects.all().filter(complate = False)
        else:
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
            #دعوت به جلسه
            
            #دستور جلسه
            if(MeetingAgenda.objects.all().filter(meetingRelated = query ).exists()):
                data.append(done_string.format(reverse('CreateViewMeetingAgenda' , kwargs={'meetingId':query.id})) )
            else:
                data.append(doing_string.format(reverse('CreateViewMeetingAgenda' , kwargs={'meetingId':query.id})) )
            if(MeetingInvitation.objects.all().filter(meetingRelated = query ).exists()):
                data.append(done_string.format(reverse('CreateViewMeetingInvitation' , kwargs={'meetingId':query.id})) )
            else:
                data.append(doing_string.format(reverse('CreateViewMeetingInvitation' , kwargs={'meetingId':query.id})) )
            #درخواست گزارش
            data.append(doing_string.format(reverse('CreateViewReport') ))
            #فایل ارائه جلسه
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
        
                if(MeetingMember.objects.all().filter(meetingRelated = query )[0].complated):
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
        scMember = None
        otherMember = None
        allMember = Member.objects.all().filter(meetingRelated__id = meetingId)
        prMember = allMember.filter(memberType = 'pr')
        if(len(allMember.filter(memberType = 'sc')) > 0):
            scMember = allMember.filter(memberType = 'sc')
        if(len(allMember.filter(memberType = 'other')) > 0):
            otherMember =  allMember.filter(memberType = 'other')
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
        'discribtion':discribtion,'icon_name':icon_name , 'scMember':scMember , 'otherMember':otherMember,
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
            for member in instance.meetingRelated.meetingProfileRelated.membersPrimary.all():
                Event.objects.create( user = member.profile , description = instance.meetingRelated.description , title =instance.meetingRelated.title ,end = instance.meetingDate  , start = instance.meetingDate   )
                Notifications.objects.create( title = 'شما به جلسه ' +instance.meetingRelated.title +' که در تاریخ  ' + str(instance.meetingDate) +' برگزار می شود دعوت شده اید.' , recivers = member.profile )
            sweetify.toast(self.request,timer=30000 , icon="success",title =' تاریخ و زمان جلسه با موفقیت ثبت شد    !!!')
            return redirect('CreateViewMeetingMembers' ,instance.meetingRelated.id )
        else:
            sweetify.toast(self.request,timer=30000 , icon="error",title =' تاریخ و زمان جلسه   ثبت نشد    !!!')
            return redirect('ViewMeetingDashboard')




def add_other_member(request , meetingId ):
    if request.method =="POST":
        memberName = request.POST.get('memberName')
        meetingSelected = Meeting.objects.get(id =meetingId )
        instanceMember = Member.objects.create(meetingRelated = meetingSelected ,otherPerson = memberName ,memberType ='other')
        instanceMember.save()
        memberOtherList = Member.objects.all().filter(meetingRelated = meetingSelected).filter(memberType = 'other')
        
        
        return render(request , 'partials/member-other-list.html' ,{'memberOtherList' : memberOtherList , } )
    else:
        pass
def delete_other_member(request , memberId ):
   
    
    
    instanceMember = Member.objects.get(id = memberId)
    meetingSelected = instanceMember.meetingRelated
    instanceMember.delete()
    memberOtherList = Member.objects.all().filter(meetingRelated = meetingSelected).filter(memberType = 'other')
    
    
    return render(request , 'partials/member-other-list.html' ,{'memberOtherList' : memberOtherList , } )
    




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
        
        
        allJob = JobBank.objects.all().filter(~Q(profile = None) )
        scMember = None
        otherMember = None
        allMember = Member.objects.all().filter(meetingRelated__id = meetingId)
        prMember = allMember.filter(memberType = 'pr')
        if(len(allMember.filter(memberType = 'sc')) > 0):
            scMember = allMember.filter(memberType = 'sc')
        if(len(allMember.filter(memberType = 'other')) > 0):
            otherMember =  allMember.filter(memberType = 'other')
        

       
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "اعضا  جلسه"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        memberOtherList = Member.objects.all().filter(meetingRelated = meetingSelected).filter(memberType = 'other')
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
        contex = {'extend':self.extend , 'header_title':header_title,'prMember':prMember ,'scMember':scMember ,'otherMember':otherMember ,
        'discribtion':discribtion,'icon_name':icon_name ,'memberOtherList':memberOtherList,
        'columns' : columns , 'color' : color , 'meetingSelected':meetingSelected   , 'meetingSelectedDate':meetingSelectedDate ,'allJob' : allJob ,  'meetingSelectedMembers' : meetingSelectedMembers , 'meetingSelectedAgendas' : meetingSelectedAgendas , 'otherMember':otherMember , 'allEnactment' :allEnactment }
        return render(request,self.template_name,contex)


    def post(self, request , meetingId , *args, **kwargs):
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        
        jobId = request.POST.getlist('jobSelected')
        allJobSelected = JobBank.objects.all().filter(~Q(profile = None) ).filter(id__in = jobId)
        for job in allJobSelected:
            instanceMember = Member.objects.create(meetingRelated = meetingSelected ,JobBankRelated = job ,memberType ='sc')
            instanceMember.save()
        try:
            MeetingMember.objects.get( meetingRelated =meetingSelected  )
        except:
            MeetingMember.objects.create( meetingRelated =meetingSelected ,complated = True )
        sweetify.toast(self.request,timer=30000 , icon="success",title =' اعضا فرعی و سایر اعضا   جلسه با موفقیت ثبت شد    !!!')
        return redirect('CreateViewMeetingAgenda' , meetingId =meetingSelected.id )
        
        #فرم دریافت شده
      
           


class CreateViewMeetingInvitation( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingInvitation.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewProfileMeeting'
  

    def get(self, request , meetingId ,  *args, **kwargs):
        
        scMember = None
        otherMember = None
        allMember = Member.objects.all().filter(meetingRelated__id = meetingId)
        prMember = allMember.filter(memberType = 'pr')
        if(len(allMember.filter(memberType = 'sc')) > 0):
            scMember = allMember.filter(memberType = 'sc')
        if(len(allMember.filter(memberType = 'other')) > 0):
            otherMember =  allMember.filter(memberType = 'other')
        
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
        header_title  = "ارسال دعوت به جلسه جلسه"
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
        'discribtion':discribtion,'icon_name':icon_name ,'scMember':scMember , 'otherMember':otherMember,
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
            sweetify.toast(self.request,timer=30000 , icon="success",title ='    دعوت به جلسه جلسه با موفقیت ثبت شد    !!!')
            return redirect('ListViewMeeting')
           

class CreateViewMeetingAgenda( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingAgenda.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewProfileMeeting'
  
    def get(self, request , meetingId ,  *args, **kwargs):
        
      
        scMember = None
        otherMember = None
        allMember = Member.objects.all().filter(meetingRelated__id = meetingId)
        prMember = allMember.filter(memberType = 'pr')
        if(len(allMember.filter(memberType = 'sc')) > 0):
            scMember = allMember.filter(memberType = 'sc')
        if(len(allMember.filter(memberType = 'other')) > 0):
            otherMember =  allMember.filter(memberType = 'other')
            
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
        'discribtion':discribtion,'icon_name':icon_name ,'scMember':scMember , 'otherMember':otherMember ,
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
            sweetify.toast(self.request,timer=30000 , icon="success",title ='    دعوت به جلسه جلسه با موفقیت ثبت شد    !!!')
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
        
        instance =  MeetingEnactment.objects.create( meetingRelated = meetingRelatedSelected , title = titleSelected, responsibleExecutive =responsibleExecutive , responsibleFollow= responsibleFollow ,  deadLine= deadLine )
        instance.save()
        crDate = str(date2jalali(instance.created_at).day) + '-' + str(date2jalali(instance.created_at).month) + '-' + str(date2jalali(instance.created_at).year)
        deadDate = str(date2jalali(deadLine).day) + '-' + str(date2jalali(deadLine).month) + '-' + str(date2jalali(deadLine).year)
        instanceReport = Report.objects.create(title = 'درخواست گزارش مطابق مصوبه جلسه  ' + meetingRelatedSelected.title + ' . ' , description = 'با عرض سلام و خسته نباشید خدمت همکار محترم طبق مصوبه جلسه ' + meetingRelatedSelected.title + 'که در تاریخ ' + crDate + ' برگذار شد، مصوب گشت شما ' + titleSelected +  ' را تا تاریخ ' + deadDate + ' به انجام برسانید ، لطفا نتیجه را از طریق همین گزارش ارسال نمایید.' + 'همچنین می توانید متن کامل مصوبه را از طریق مدیریت جلسات -> سوابق جلسات به صورت کامل مشاهده نمایید .' , source = 'meeting')
        ReportActivityManager.objects.create( sender =meetingRelatedSelected.meetingProfileRelated.manager.profile , reciver =responsibleExecutive.profile  ,ReportRelated = instanceReport ,startTime =instanceReport.created_at  , deadLine = deadLine)
        Notifications.objects.create( title = ' برای شما یک درخواست گزارش مرتبط با مصوبه جلسه ' + meetingRelatedSelected.title + ' ثبت شده است .', recivers =  responsibleExecutive.profile)
    else:
        pass
    
   
    
    
    allEnactment = MeetingEnactment.objects.all().filter(meetingRelated = meetingRelatedSelected)
    
    return render(request , 'partials/enactment-list.html' ,{ 'allEnactment' : allEnactment} )

class CreateViewMeetingMinute( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingMinute.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewProfileMeeting'
    

    def get(self, request , meetingId ,  *args, **kwargs):
        
      
        scMember = None
        otherMember = None
        allMember = Member.objects.all().filter(meetingRelated__id = meetingId)
        prMember = allMember.filter(memberType = 'pr')
        if(len(allMember.filter(memberType = 'sc')) > 0):
            scMember = allMember.filter(memberType = 'sc')
        if(len(allMember.filter(memberType = 'other')) > 0):
            otherMember =  allMember.filter(memberType = 'other')
            
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
        allMemberP = []
        for memberJob in meetingSelected.meetingProfileRelated.membersPrimary.all():
            allMemberP.append(memberJob)
        allMemberS = []
        for memberJob in Member.objects.all().filter(meetingRelated =meetingSelected ):
            
            allMemberS.append(memberJob)
        
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
        contex = {'extend':self.extend , 'header_title':header_title,'prMember' :prMember ,
        'discribtion':discribtion,'icon_name':icon_name ,'scMember' :scMember , 'otherMember':otherMember ,
        'columns' : columns , 'color' : color , 'meetingSelected':meetingSelected  , 'meetingSelectedDate' :meetingSelectedDate , 'meetingSelectedMembers' :meetingSelectedMembers , 'allAgenda':allAgenda , 'form':form , 'meetingSelectedAgendas':meetingSelectedAgendas , 'allMemberP':allMemberP ,'allMemberS':allMemberS  , 'allEnactment':allEnactment}
        return render(request,self.template_name,contex)


    def post(self, request , meetingId , *args, **kwargs):
        # if(len(MeetingInvitation.objects.all().filter(meetingRelated__id = meetingId)) >0):
        #     obj = MeetingInvitation.objects.all().filter(meetingRelated__id = meetingId)[0]
        #     form = CreateFormMeetingInvitation(request.POST or request.FILES,instance=obj)
        # else:
        #     form = CreateFormMeetingInvitation( request.POST )
        MemberId = request.POST.getlist('jobSelected')
        MemberSelected = Member.objects.all().filter(id__in = MemberId)
        
       
        
        for member in MemberSelected:
            
            member.present = True
            member.save()
        meetingSelected = MeetingMember.objects.all().filter(meetingRelated=meetingId)[0]
        meetingSelected.complated = True
        meetingSelected.save()
        #فرم دریافت شده
        # if form.is_valid():

        #     instance = form.save(commit=False)
        #     instance.meetingRelated = Meeting.objects.get(id =meetingId )
        #     instance.save()
        sweetify.toast(self.request,timer=30000 , icon="success",title ='    حاضرین جلسه با موفقیت ثبت شد    !!!')
        return redirect('CreateViewMeetingDocument' , meetingId=meetingId )
           

class CreateViewMeetingEnactment( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingEnactment.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewProfileMeeting'
    

    def get(self, request , meetingId ,  *args, **kwargs):
        
        scMember = None
        otherMember = None
        allMember = Member.objects.all().filter(meetingRelated__id = meetingId)
        prMember = allMember.filter(memberType = 'pr')
        if(len(allMember.filter(memberType = 'sc')) > 0):
            scMember = allMember.filter(memberType = 'sc')
        if(len(allMember.filter(memberType = 'other')) > 0):
            otherMember =  allMember.filter(memberType = 'other')
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
        'discribtion':discribtion,'icon_name':icon_name , 'scMember':scMember , 'otherMember':otherMember ,
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
            sweetify.toast(self.request,timer=30000 , icon="success",title ='    دعوت به جلسه جلسه با موفقیت ثبت شد    !!!')
            return redirect('ViewProfileMeeting')
           

class CreateViewMeetingDocument( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingDocument.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewProfileMeeting'
    

    def get(self, request , meetingId ,  *args, **kwargs):
        
        scMember = None
        otherMember = None
        allMember = Member.objects.all().filter(meetingRelated__id = meetingId)
        prMember = allMember.filter(memberType = 'pr')
        if(len(allMember.filter(memberType = 'sc')) > 0):
            scMember = allMember.filter(memberType = 'sc')
        if(len(allMember.filter(memberType = 'other')) > 0):
            otherMember =  allMember.filter(memberType = 'other')
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
        'discribtion':discribtion,'icon_name':icon_name ,'scMember': scMember, 'otherMember' :otherMember ,
        'columns' : columns , 'color' : color , 'meetingSelected':meetingSelected  , 'meetingSelectedDate' :meetingSelectedDate , 'meetingSelectedMembers' :meetingSelectedMembers , 'allAgenda':allAgenda , 'form':form , 'meetingSelectedAgendas':meetingSelectedAgendas , 'allMember':allMember , 'allEnactment':allEnactment , 'allJob':allJob , 'meetingSelectedDocument':meetingSelectedDocument}
        return render(request,self.template_name,contex)


    def post(self, request , meetingId , *args, **kwargs):
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        
        if(len(request.FILES)!=0):
            
            if(MeetingDocument.objects.all().filter(meetingRelated = meetingSelected).exists()):
            # if(MeetingMinute.objects.all().filter(meetingRelated = meetingSelected).exists()):
                MeetingDocumentSelected = MeetingDocument.objects.get(meetingRelated = meetingSelected)
              
                minuteDocumentUploaded = request.FILES['minuteDocument']
         
                MeetingDocumentSelected.minuteDocument = minuteDocumentUploaded
                MeetingDocumentSelected.save()
            else:
               
              
                minuteDocumentUploaded = None
               
                minuteDocumentUploaded = request.FILES['minuteDocument']
                instanceDocument = MeetingDocument.objects.create(meetingRelated = meetingSelected , minuteDocument = minuteDocumentUploaded)
                instanceDocument.save()

               
            sweetify.toast(self.request,timer=30000 , icon="success",title ='      فایل های جلسه با موفقیت بارگزاری شد !!!')
            return redirect('ListViewMeeting')
        #فرم دریافت شده
        else:
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='          فایلی یافت نشد    !!!')
            return redirect('ListViewMeeting')
           

class CreateViewMeetingPlan( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createMeetingPlan.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewProfileMeeting'
    

    def get(self, request , meetingId ,  *args, **kwargs):
        
        scMember = None
        otherMember = None
        allMember = Member.objects.all().filter(meetingRelated__id = meetingId)
        prMember = allMember.filter(memberType = 'pr')
        if(len(allMember.filter(memberType = 'sc')) > 0):
            scMember = allMember.filter(memberType = 'sc')
        if(len(allMember.filter(memberType = 'other')) > 0):
            otherMember =  allMember.filter(memberType = 'other')
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
        if(meetingSelectedMembers == None):
            pass
        else:
            for memberJob in meetingSelectedMembers.membersSecondary.all():
                if(memberJob in allMember):
                    continue
                allMember.append(memberJob)
        
        allAgenda = MeetingAgenda.objects.all().filter(meetingRelated  = meetingSelected)
        allEnactment = MeetingEnactment.objects.all().filter(meetingRelated  = meetingSelected)
        form = CreateFormMeetingEnactment()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "بارگزاری فایل ارائه جلسه"
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
        'discribtion':discribtion,'icon_name':icon_name ,'scMember' :scMember , 'otherMember':otherMember ,
        'columns' : columns , 'color' : color , 'meetingSelected':meetingSelected  , 'meetingSelectedDate' :meetingSelectedDate , 'meetingSelectedMembers' :meetingSelectedMembers , 'allAgenda':allAgenda , 'form':form , 'meetingSelectedAgendas':meetingSelectedAgendas , 'allMember':allMember , 'allEnactment':allEnactment , 'allJob':allJob , 'meetingSelectedDocument':meetingSelectedDocument}
        return render(request,self.template_name,contex)


    def post(self, request , meetingId , *args, **kwargs):
        meetingSelected = Meeting.objects.all().filter(id =meetingId )[0]
        
        if(len(request.FILES)!=0):
            
            if(MeetingPlan.objects.all().filter(meetingRelated = meetingSelected).exists()):
            
                MeetingPlanSelected = MeetingPlan.objects.get(meetingRelated = meetingSelected)
                planDocumentUploaded = request.FILES['planDocument']
           
                MeetingPlanSelected.planDocument = planDocumentUploaded
                
                MeetingPlanSelected.save()
            else:
                instancePlan = MeetingPlan.objects.create(meetingRelated = meetingSelected, planDocument = request.FILES['planDocument'] )
                instancePlan.save()

               
            sweetify.toast(self.request,timer=30000 , icon="success",title ='      فایل های جلسه با موفقیت بارگزاری شد !!!')
            return redirect('CreateViewMeetingEnactment' , meetingId = meetingId)
        #فرم دریافت شده
        else:
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='          فایلی یافت نشد    !!!')
            return redirect('ListViewMeeting')
           

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
        allEnactments = MeetingEnactment.objects.all().filter(meetingRelated=meetingSelected)
  










        for en in allEnactments:
            Event.objects.create( user =en.responsibleExecutive.profile , title =en.title ,end = en.deadLine , start =en.deadLine   )
            PlanProfile.objects.create( title =en.title  , accountable =en.responsibleFollow  ,  responsible =en.responsibleExecutive ,  sourcePlan ='meeting'  ,  startTiem =datetime.datetime.now().date() , deadLine =en.deadLine )
            Notifications.objects.create( title = 'یک برنامه اجرایی جدید مرتبط با مصوبه جلسه '  + en.meetingRelated.title + en.title + ' برای شما ایجاد شد . ', recivers = en.responsibleExecutive.profile )
        sweetify.toast(self.request,timer=30000 , icon="success",title ='    جلسه با موفقیت بایگانی شد !!!')
        #دیکشنری داده هاperformanceVariable
        contex = {'extend':self.extend , 
        }
        return redirect('ListViewMeetingReview')


        
def add_agenda(request):
    meetingRelatedId = request.POST.get('meetingRelated')
    meetingRelatedSelected = Meeting.objects.get(id =meetingRelatedId )
    title = request.POST.get('title')
    text = request.POST.get('text')
    timeDuration = request.POST.get('timeDuration')
   
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
                return redirect('MomayeziViewMeetingDashboard')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='نقطه قوت  مورد نظر ساخته نشد !')           
            context = {'form': form,'object':obj ,'extend':self.extend ,}
        return render(request,self.template_name,context)


class ListViewMeetingReview(ListView):

  
    extend = 'baseEmployee.html'
    menu_link = 'ViewMomayezi'
    
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست جلسات بازنگری"
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
        
        try:
            MeetingPlanSelected =  MeetingPlan.objects.get(meetingRelated = meetingId)
        except:
            MeetingPlanSelected = None
        
        
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
    

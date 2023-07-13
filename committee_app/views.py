from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CreateFormCommittee 
from .models import Committee 

from django.views.generic import ListView
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from .serializers import CommitteetSerializer
from organization_app.models import JobBank
from profile_app.models import Profile
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from organization_app.models import JobBank
from risk_app.utils import is_dabir




class CommitteeHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "Committee.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name ,{'extend' : self.extend,'riskDabir':is_dabir(self),})


#کلاس ایجاد رکورد جدید
class CreateViewCommittee( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'baseEmployee.html'
    def get(self, request, *args, **kwargs):
        form = CreateFormCommittee()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک کمیته  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک کمیته  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        
        #دیکشنری داده ها
        contex = {'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'extend' : self.extend,}
        return render(request,self.template_name,contex )


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormCommittee(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='کمیته  جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewCommittee')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='کمیته  مورد نظر ساخته نشد !')
        context = {'form': form , 'extend' : self.extend,'riskDabir':is_dabir(self),}
        return render(request,self.template_name,context)


class ListViewCommittee(ListView):
  

    extend = 'baseEmployee.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست کمیته  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام کمیته  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['سرفصل' , 'عنوان' ,'مستند قانونی تشکیل جلسه' , 'حوزه مرتبط' ,'نوع کمیته'   ,'رئیس' , 'جانشین اول' ,'جانشین دوم' , 'دبیر' ,]
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = Committee.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.topic)
            data.append(query.title)
            data.append(query.mostanadGhanoni)
        
            if(query.hoze!=None):
                data.append(str(query.hoze))
            else:
                data.append('اطلاعاتی موجود نیست')
            data.append(query.typeComittee)
            if(query.head!=None):
                data.append(str(query.head))
            else:
                data.append('اطلاعاتی موجود نیست')
            if(query.janeshinAval!=None):
                data.append(str(query.janeshinAval))
            else:
                data.append('اطلاعاتی موجود نیست')
            if(query.janeshinDovom!=None):
                data.append(str(query.janeshinDovom))
            else:
                data.append('اطلاعاتی موجود نیست')
            if(query.dabir!=None):
                data.append(str(query.dabir))
            else:
                data.append('اطلاعاتی موجود نیست')
          
   
            
 

         
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = { 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data, 'extend' : self.extend,'riskDabir':is_dabir(self),}
        return context

    model = Committee
    ordering = '-created_at' 
    template_name ='listCommittee.html'



class ViewCommittee( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detailCommittee.html"
    extend = 'baseEmployee.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Committee,id = id)
        return obj
    
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = Committee.objects.all().filter(id=id)[0]
           
            obj = get_object_or_404(Committee,id = id)
            
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "اطلاعات کمیته   "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "چزییات کمیته را در این صفحه میتوانید مشاهده کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها

            #جدول لیست پرداختی ها
            committee_header_table   = ['سرفصل' , 'عنوان' ,'مستند قانونی تشکیل جلسه' , 'حوزه مرتبط' ,'نوع کمیته' , 'اعضا' ,'رئیس' , 'جانشین اول' ,'جانشین دوم' , 'دبیر' ,]
        
            #Committee_queryset = Committee.objects.all().filter(Committee.id==id)
            
            #class_queryset_filter = CommitteeFilter(self.request.GET, queryset=class_queryset)
            Committee_list_data = []
    
            #ایجاد لیست داده ها
            jobBank_header_table   = ['کد پرسنلی' , 'نام' ,'نام خانوادگی',' کد واحد','نام واحد'  ,'کد نوع پست سازمانی' , 'نام نوع پست سازمانی '  ]
            queryset = JobBank.objects.all()
            jobBonk_list_data = []
            #ایجاد لیست داده ها
            
        
            #جدول لیست کلاس ها
            # عنوان های جدول
            membersProfile = obj.members.all()
            membersJob = []
            
            
            # for member in membersProfile:
            #     # j = JobBank.objects.get(profile=member)
                
            #     j = queryset.filter(id=member)
            #     if(len(j)>0):
            #         membersJob.append(j[0])
                
            context =  {'object':obj , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,
                'color':color , 'columns':columns,'jobBonk_list_data':jobBonk_list_data,
                'jobBank_header_table':jobBank_header_table , 'queryset':queryset , 'form':form , 'members':membersProfile , 'membersJob':membersJob , 'extend' : self.extend,'riskDabir':is_dabir(self),}


        return render(request,self.template_name,context)
 
class EditViewCommittee( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "editCommittee.html"
    extend = 'baseEmployee.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Committee,id = id)
        return obj
    
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = Committee.objects.all().filter(id=id)[0]
           
            obj = get_object_or_404(Committee,id = id)
            
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "اطلاعات کمیته   "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "چزییات کمیته را در این صفحه میتوانید مشاهده کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها

            #جدول لیست پرداختی ها
            committee_header_table   = ['سرفصل' , 'عنوان' ,'مستند قانونی تشکیل جلسه' , 'حوزه مرتبط' ,'نوع کمیته' , 'اعضا' ,'رئیس' , 'جانشین اول' ,'جانشین دوم' , 'دبیر' ,]
        
            #Committee_queryset = Committee.objects.all().filter(Committee.id==id)
            
            #class_queryset_filter = CommitteeFilter(self.request.GET, queryset=class_queryset)
            Committee_list_data = []
    
            #ایجاد لیست داده ها
            jobBank_header_table   = ['کد پرسنلی' , 'نام' ,'نام خانوادگی',' کد واحد','نام واحد'  ,'کد نوع پست سازمانی' , 'نام نوع پست سازمانی '  ]
            queryset = JobBank.objects.all()
            jobBonk_list_data = []
            #ایجاد لیست داده ها
            
        
            #جدول لیست کلاس ها
            # عنوان های جدول
            membersProfile = obj.members.all()
            membersJob = []
            
            
            # for member in membersProfile:
            #     # j = JobBank.objects.get(profile=member)
                
            #     j = queryset.filter(id=member)
            #     if(len(j)>0):
            #         membersJob.append(j[0])
                
            context =  {'object':obj , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,
                'color':color , 'columns':columns,'jobBonk_list_data':jobBonk_list_data,
                'jobBank_header_table':jobBank_header_table , 'queryset':queryset , 'form':form , 'members':membersProfile , 'membersJob':membersJob , 'extend' : self.extend,'riskDabir':is_dabir(self),}


        return render(request,self.template_name,context)
 
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            jobId = request.POST.getlist('jobSelected')
            jobSelected = JobBank.objects.all().filter(id__in = jobId)
            print(jobSelected , 'asdasdasd')
            try:
                
                for job in jobSelected:
                    
                    obj.members.add(job)
        
                sweetify.toast(self.request,timer=30000 , icon="success",title ='عضو با موفقیت افزوده شد !!!')
            except:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='عضو  مورد نظر یافت نشد !')
            context = {'form': 'for','object':obj ,  'extend' : self.extend,'riskDabir':is_dabir(self),}
        return HttpResponseRedirect(reverse('ViewCommittee' , kwargs={'id':obj.id}))
        return render(request,self.template_name,context)


class UpdateViewCommittee( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'baseEmployee.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Committee,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormCommittee(instance=obj)
            
            obj = get_object_or_404(Committee,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش کمیته  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این کمیته  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns, 'extend' : self.extend,'riskDabir':is_dabir(self),}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormCommittee(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='کمیته  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewCommittee')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='کمیته  مورد نظر ساخته نشد !')           
            context = {'form': form,'object':obj, 'extend' : self.extend,'riskDabir':is_dabir(self),}
        return render(request,self.template_name,context)



class DeleteViewCommittee( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'baseEmployee.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Committee,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='کمیته  با موفقیت پاک شد !!!')
            
            return redirect('ViewCommitteeDashboard')
        return render(request,self.template_name,)
   
       
  
class DeleteViewCommitteeMember( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'baseEmployee.html'
    template_name = "deleteMember.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
      
        obj=None
        if id is not None:
            obj = get_object_or_404(Committee,id = id)
        return obj
    def get_member(self):
    
        jobId = self.kwargs.get('jobId')
        obj=None
        if id is not None:
            obj = get_object_or_404(JobBank,id = jobId)
        return obj
    def get(self, request,id=None,jobId=None ,*args, **kwargs):
        
        obj = self.get_obj()
        member = self.get_member()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن  عضو "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید      " + member.profile.lastName + " "  + " را از کمیته " + obj.title  + " حذف نمایید ؟ "
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            
            #دیکشنری داده ها
            context       = {'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color, 'extend' : self.extend,'riskDabir':is_dabir(self),}
            
        return render(request,self.template_name,context)
    def post(self, request,id=None , jobId = None ,*args, **kwargs):
        context = {}
        committeeId = Committee.objects.get(id = id)
        jobMember = JobBank.objects.get(id = jobId)
        
       
        obj = self.get_obj()
        if obj is not None:
            
            
            obj.members.remove(jobMember)
           
           
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='عضو  با موفقیت پاک شد !!!')
            context = { 'extend' : self.extend,'riskDabir':is_dabir(self),}
            return HttpResponseRedirect(reverse('ViewCommittee' , kwargs={'id':committeeId.id}))
        return render(request,self.template_name,context)
     
 
@permission_classes([IsAuthenticated])
class ListCommitteeAPI(APIView):
    def get(self, request,id=None ,*args, **kwargs):
        query = Committee.objects.all()
        serializers = CommitteetSerializer(query , many=True)
        return Response(serializers.data , status = status.HTTP_200_OK)


class ViewCommitteeDashboard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "clearDashboard.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    
 
    def get(self, request ,*args, **kwargs):
        
       
        selectedType =  request.GET.get('type') 
        createNewProfile = None
        allProfile = None
        responsible_link = None
        member_link =  None
     
        partials = 'partials/committeeDashboard.html'
        header_title = "کمیته ها و کارگروه های سازمان"
       
        #دریافت تمام داده ها
        member = Profile.objects.get(user = request.user)
        
        if(request.user.is_superuser):
            responsible_link = None
            member_link = None
            createNewProfile = 'CreateViewCommittee'
     
        allCommitee = Committee.objects.all()
        
        
       
       
       
       
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
     
     
        
        context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,'member_link':member_link,
        'discribtion':discribtion,'icon_name':icon_name,'header_title':header_title,'responsible_link':responsible_link ,
        'color':color  ,'partials':partials,'createNewProfile':createNewProfile,'allProfile':allProfile , 'allCommitee':allCommitee,
        }

        return render(request,self.template_name,context)
    
    
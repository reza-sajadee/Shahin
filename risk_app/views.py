from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CreateFormQuestionDaste ,CreateFormRiskProfile , CreateFormRiskTeam , CreateFormRiskIdentification, CreateFormRiskActivityManager ,CreateFormRiskIdentificationSelecting, CreateFormRiskMeasurement , CreateFormRiskProcessRelated
from .models import QuestionDaste ,RiskProfile , RiskTeam ,RiskIdentification , RiskTopic , RiskActivityManager , RiskIdentificationSelecting , RiskMeasurement , RiskProcessRelated ,RiskProcess  , extraData
from django.urls import reverse
from django.views.generic import ListView
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from risk_app.models import RiskProfile
from django.http.response import HttpResponseRedirect
from notifications_app.models import Notifications
from committee_app.models import Committee
from process_app.models import Hoze , Process ,Group
from profile_app.models import Profile
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Model
from .serializers import RiskIdentificationSerializer
from organization_app.models import JobBank
from profile_app.decorators import  staff_only

from .decorators import user_is_dabir
from risk_app.utils import is_dabir ,avrage , std


#  مدیریت کیفیت --- > مدیریت ریسک  
class ViewRiskMenu( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'
    
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        
            
            
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "مدیریت ریسک"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر بخش های محتلف ریسک را می توانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        #رنگ             
        columns       = 1
        #دیکشنری داده ها

        #جدول لیست پرداختی ها
    

        #ایجاد لیست داده ها
        
        
        list_menu = [
            
            
            { 'staticLink' : '','title' : 'شناسایی ریسک' , 'link' : 'ListViewRiskIdentification' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'ارزیابی ریسک' , 'link' : 'ListViewRiskMeasurement' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'ریسک های سازمانی' , 'link' : 'ViewRiskDashboard' ,'icon':'control-panel' , 'color' : '1' , } ,
            
                ]
        
        risk_profile = RiskProfile.objects.all()
        
        # if(self.request.user.is_superuser):
        #     list_menu.append({ 'staticLink' : '','title' : 'پروفایل ریسک' , 'link' : 'ListViewRiskProfile' ,'icon':'control-panel' , 'color' : '2' , } )
        #     list_menu.append({ 'staticLink' : '','title' : 'تیم ریسک' , 'link' : 'ListViewRiskTeam' ,'icon':'control-panel' , 'color' : '2' , }  )
        #     list_menu.append({ 'staticLink' : '','title' : 'فعالیت های  ریسک' , 'link' : 'ListViewRiskActivityManager' ,'icon':'control-panel' , 'color' : '2' , } )
        #     list_menu.append({ 'staticLink' : '','title' : 'ارتباط ریسک با فرآیند' , 'link' : 'ListViewRiskProcessRelated' ,'icon':'control-panel' , 'color' : '2' , } )
        #     list_menu.append({ 'staticLink' : '','title' : 'بررسی و جمع بندی ریسک های شناسایی شده' , 'link' : 'ListViewRiskIdentificationSelecting' ,'icon':'control-panel' , 'color' : '2' , } )
        #else:
            
        
        if(len(risk_profile) == 0):
            if Profile.objects.filter(user =self.request.user)[0].user.is_superuser :
                
                list_menu.append({ 'staticLink' : '','title' : 'پروفایل ریسک' , 'link' : 'ListViewRiskProfile' ,'icon':'control-panel' , 'color' : '2' , } )
                list_menu.append({ 'staticLink' : '','title' : 'تیم ریسک' , 'link' : 'ListViewRiskTeam' ,'icon':'control-panel' , 'color' : '2' , }  )
                list_menu.append({ 'staticLink' : '','title' : 'فعالیت های  ریسک' , 'link' : 'ListViewRiskActivityManager' ,'icon':'control-panel' , 'color' : '2' , } )
                list_menu.append({ 'staticLink' : '','title' : 'ارتباط ریسک با فرآیند' , 'link' : 'ListViewRiskProcessRelated' ,'icon':'control-panel' , 'color' : '2' , } )
                list_menu.append({ 'staticLink' : '','title' : 'بررسی و جمع بندی ریسک های شناسایی شده' , 'link' : 'ListViewRiskIdentificationSelecting' ,'icon':'control-panel' , 'color' : '2' , } )
        else:
            for risk_profile_selected in risk_profile:
                if risk_profile_selected.committeeRisk.dabir == Profile.objects.filter(user =self.request.user)[0]  or Profile.objects.filter(user =self.request.user)[0].user.is_superuser :
                    
                    list_menu.append({ 'staticLink' : '','title' : 'پروفایل ریسک' , 'link' : 'ListViewRiskProfile' ,'icon':'control-panel' , 'color' : '2' , } )
                    list_menu.append({ 'staticLink' : '','title' : 'تیم ریسک' , 'link' : 'ListViewRiskTeam' ,'icon':'control-panel' , 'color' : '2' , }  )
                    list_menu.append({ 'staticLink' : '','title' : 'فعالیت های  ریسک' , 'link' : 'ListViewRiskActivityManager' ,'icon':'control-panel' , 'color' : '2' , } )
                    list_menu.append({ 'staticLink' : '','title' : 'ارتباط ریسک با فرآیند' , 'link' : 'ListViewRiskProcessRelated' ,'icon':'control-panel' , 'color' : '2' , } )
                    list_menu.append({ 'staticLink' : '','title' : 'بررسی و جمع بندی ریسک های شناسایی شده' , 'link' : 'ListViewRiskIdentificationSelecting' ,'icon':'control-panel' , 'color' : '2' , } )
                    break
        #ایجاد لیست داده ها
    
        #جدول لیست کلاس ها
        # عنوان های جدول
        
            
        context =  {'extend':self.extend , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns,'list_menu':list_menu,
            }


        return render(request,self.template_name,context)

class QuestionDasteHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "QuestionDaste.html"
    @staff_only 
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewQuestionDaste( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'base.html'
    @staff_only 
    def get(self, request, *args, **kwargs):
        form = CreateFormQuestionDaste()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک ارزیابی ریسک سوال  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک ارزیابی ریسک سوال  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    @staff_only
    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormQuestionDaste(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='ارزیابی ریسک سوال  جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewQuestionDaste')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='ارزیابی ریسک سوال  مورد نظر ساخته نشد !')
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewQuestionDaste(ListView):
  
    extend = 'base.html'
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست ارزیابی ریسک سوال  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام ارزیابی ریسک سوال  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان' ,]
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = QuestionDaste.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
         
            data.append(query.title)
           
   
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = QuestionDaste
    ordering = '-created_at' 
    template_name ='list.html'



class ViewQuestionDaste( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detail.html"
    extend = 'base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(QuestionDaste,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = QuestionDaste.objects.all().filter(id=id)[0]
           
            obj = get_object_or_404(QuestionDaste,id = id)
            
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "اطلاعات ارزیابی ریسک سوال   "
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
            
            list_data = {'عنوان' : obj.title}
            #ایجاد لیست داده ها
           
            #جدول لیست کلاس ها
            # عنوان های جدول
            
                
            context =  {'extend':self.extend , 'menuBack':self.menuBack , 'object':obj , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,
                'color':color , 'columns':columns,'list_data':list_data,
                'header_table':header_table , 'form':form , }


        return render(request,self.template_name,context)
 

class UpdateViewQuestionDaste( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(QuestionDaste,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormQuestionDaste(instance=obj)
            
            obj = get_object_or_404(QuestionDaste,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش ارزیابی ریسک سوال  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این ارزیابی ریسک سوال  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend' :self.extend , 'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormQuestionDaste(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='ارزیابی ریسک سوال  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewQuestionDaste')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='ارزیابی ریسک سوال  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewQuestionDaste( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    extend ='base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(QuestionDaste,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک ارزیابی ریسک سوال "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که ارزیابی ریسک سوال   " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend' : self.extend , 'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='ارزیابی ریسک سوال  با موفقیت پاک شد !!!')
            
            return redirect('ListViewQuestionDaste')
        return render(request,self.template_name,context)
    
 
 
 

class RiskProfileHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "RiskProfile.html"
    
    @staff_only 
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewRiskProfile( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only 
    def get(self, request, *args, **kwargs):
        form = CreateFormRiskProfile()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک پروفایل ریسک  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک پروفایل ریسک  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)

    @user_is_dabir
    @staff_only
    def post( self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormRiskProfile(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            rp = form.save()
            committeeSelected = Committee.objects.get(id = rp.committeeRisk.id)
            profileSender = Profile.objects.get(user = request.user)
            jobs = Committee.objects.filter(id = rp.committeeRisk.id)[0].members
            
            instanceRiskActivityManager = RiskActivityManager.objects.create(riskProfile = rp,sender=profileSender, reciver=committeeSelected.dabir.profile ,status='doing' ,activity='team' )
            instanceRiskActivityManager.save()
            for job in jobs.all():
                instance = Notifications.objects.create(link='#',recivers=job.profile,title='عضویت در کمیته ریسک', description='با عرض سلام خدمت همکار محترم شما عضو کمیته ریسک شده اید مراحل کاری در آینده اطلاع رسانی میگردد' ,  status = 'primary' ,  icon = 'alarm')
          
                
                instance.save()
             
           
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='پروفایل ریسک  جدید با موفقیت ساخته شد !!!')
            return redirect('ViewRiskDashboard')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='پروفایل ریسک  مورد نظر ساخته نشد !')
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewRiskProfile(ListView):
  
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
   
    
    @user_is_dabir
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست پروفایل ریسک  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام پروفایل ریسک  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان','کمیته ریسک']
        #اسم داده های جدول
        backMenu = 'ViewRiskMenu'
        #دریافت تمام داده ها
        queryset = RiskProfile.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.committeeRisk)
   
            
 

         
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data , 'backMenu':backMenu}
        return context

    model = RiskProfile
    ordering = '-created_at' 
    template_name ='list.html'



class ViewRiskProfile( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detailRiskProfile.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskProfile,id = id)
        return obj
    
    @user_is_dabir
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        
        obj = self.get_obj()
        if obj is not None:
            form = RiskProfile.objects.all().filter(id=id)[0]
           
            obj = get_object_or_404(RiskProfile,id = id)
            
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "  اطلاعات پروفایل ریسک   "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "چزییات پروفایل ریسک را در این صفحه می توانید مشاهده کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها

            #جدول لیست پرداختی ها
            RiskProfile_header_table   = ['عنوان' , 'کمیته']
        
            #RiskProfile_queryset = RiskProfile.objects.all().filter(RiskProfile.id==id)
            
            #class_queryset_filter = RiskProfileFilter(self.request.GET, queryset=class_queryset)
            RiskProfile_list_data = []

            RiskProfile_queryset = RiskProfile.objects.get(id = id)
            
            
            committeeOfRiskProfile = Committee.objects.filter(id =RiskProfile_queryset.committeeRisk.id )[0]
            
            
            membersOfCommittee = committeeOfRiskProfile.members.all()
        
            
            RiskTopics = RiskTopic.objects.all()
            allHozes = Hoze.objects.all()
            usedHozes = []
            
            header_table   = ['عنوان','پروفایل ریسک' ,'اعضا' ,'سرفصل ریسک' ,'حوزه' ]
            #اسم داده های جدول
            hozes = ''
            #دریافت تمام داده ها
           
            
            queryset = RiskTeam.objects.all().filter(riskProfile=RiskProfile_queryset)
            
            list_data = []
            #ایجاد لیست داده ها
            for query in queryset:
                data = []
                dict_temp = {}
                data.append(query.title)
                data.append(query.riskProfile)
                members = ''
                for member in query.memberProfile.all():
                    members += str(member.lastName) + ' | ' + str(member.employeeNumber) + ' - '
                    
                data.append(str(members))
                
                
                data.append(query.riskTopic)
                
                
                hozes = ''
                
                for hoze in query.hoze.all():
                    hozes += hoze.title + ' - '
                    usedHozes.append(hoze.id)
                data.append(str(hozes))
                
                
                
            
                dict_temp = {query.id : data}
                list_data.append(data)
            
            
            allHozes = allHozes.exclude(id__in=list(set(usedHozes)))
            
            context =  {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'object':obj , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,'RiskTopics':RiskTopics , 'hozes' : hozes,'profileSelected':id,
                'color':color , 'columns':columns,'RiskProfile':RiskProfile_queryset , 'committeeOfRiskProfile' : committeeOfRiskProfile , 'form':form , 'membersOfCommittee':membersOfCommittee ,'header_table':header_table , 'list_data':list_data ,'allHozes' : allHozes}


        return render(request,self.template_name,context)
 
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        title = request.POST.get('teamTitle')
        memberProfileId = request.POST.getlist('member')
        hozesSelected = request.POST.getlist('hoze')
        RiskTopics = request.POST.get('topic')
        riskProfileSelected = RiskProfile.objects.filter(id = id)[0]    
        if(title == ''):
            sweetify.toast(self.request,timer=30000 , icon="error",title ='پروفایل ریسک  مورد نظر ساخته نشد ! وارد کردن یک عنوان برای تیم الزامی است.')           
            return HttpResponseRedirect(reverse('ViewRiskProfile' , kwargs={'id':obj.id}) )
        if(len(memberProfileId) == 0):
            sweetify.toast(self.request,timer=30000 , icon="error",title ='پروفایل ریسک  مورد نظر ساخته نشد ! انتخاب کردن اعضا برای تیم الزامی است.')           
            return HttpResponseRedirect(reverse('ViewRiskProfile' , kwargs={'id':obj.id}) )
        if(len(hozesSelected) == 0):
            sweetify.toast(self.request,timer=30000 , icon="error",title ='پروفایل ریسک  مورد نظر ساخته نشد ! انتخاب کردن حوزه برای تیم الزامی است.')           
            return HttpResponseRedirect(reverse('ViewRiskProfile' , kwargs={'id':obj.id}) )
        if(RiskTopics == ''):
            sweetify.toast(self.request,timer=30000 , icon="error",title ='پروفایل ریسک  مورد نظر ساخته نشد ! انتخاب کردن سرفصل ریسک برای تیم الزامی است.')           
            return HttpResponseRedirect(reverse('ViewRiskProfile' , kwargs={'id':obj.id}) )
        
        
        if obj is not None:
            
            
            
            
            riskProfile = obj
            
            #RiskTopicSelected = RiskTopic.objects.all().filter(id=request.POST.get('topic'))[0] 
            #hozeSelected = Hoze.objects.all().filter(id=request.POST.get('hoze') )[0] 
            
            RiskTopicsSelected = RiskTopic.objects.filter(id = request.POST.get('topic') )[0]
            
            msgdescription = 'با عرض سلام خدمت همکار محترم ، شما در کمیته   ' + str(riskProfile.title) + ' در  ' + title + ' عضو شده اید  .' 
            #msgdescription = request.POST.get('msg')
            profileSender = Profile.objects.filter(user=request.user)[0]
            #try:
            instance = RiskTeam.objects.create(title=title, riskProfile= riskProfile,riskTopic=RiskTopicsSelected  )

            
          
            for hz in hozesSelected :
                instance.hoze.add(hz)
            
            
            for member in memberProfileId:
                profileReciver = Profile.objects.get(id = member)
           
                instanceNoti = Notifications.objects.create(recivers=profileReciver,title=' عضویت در تیم '+ title  , description= msgdescription ,  status = 'primary' )
                
                instanceNoti.link = '/risk/identification/list' 
                instanceNoti.save()
                instance.memberProfile.add(member)
              
            instance.save()
            instanceNoti.save()
            
            del(instanceNoti)  
            
            
            #try:

            for hz in hozesSelected :
                
                
                
                hzSelected = Hoze.objects.all().filter(id=hz)[0]
                
                
                
                for member in memberProfileId:
                    profileReciver = Profile.objects.all().filter(id = member)[0]
                    instanceRiskActivityManager = RiskActivityManager.objects.create(riskProfile = riskProfileSelected,sender=profileSender, reciver=profileReciver ,status='doing' ,activity='identification' ,team = instance , riskTopic=RiskTopicsSelected,hoze=hzSelected,  )
                    instanceRiskActivityManager.save()
            del(instance)  
            del(instanceRiskActivityManager) 
            sweetify.toast(self.request,timer=30000 , icon="success",title ='عضو با موفقیت افزوده شد !!!')
            
                        
                        
            
            context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': 'for','object':obj}
        return HttpResponseRedirect(reverse('ViewRiskProfile' , kwargs={'id':obj.id}))
        return render(request,self.template_name,context)


class ComplateViewRiskProfile( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createCalenderMomayezi.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewRiskDashboard"
    menu_link = 'ViewRiskDashboard'
    def get(self, request,id, *args, **kwargs):
        
        riskProfileSelected = RiskProfile.objects.get(id = id)
        
        activitySelected = RiskActivityManager.objects.get(riskProfile = riskProfileSelected ,activity = 'team' )
        activitySelected.status = 'done'
        activitySelected.save()
        sweetify.toast(self.request,timer=30000 , icon="success",title ='ثبت تیم های ریسک  به اتمام رسید        !!!')
        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        return redirect('ViewRiskDashboardMember' ,id )




class UpdateViewRiskProfile( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskProfile,id = id)
        return obj
    @user_is_dabir
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRiskProfile(instance=obj)
            
            obj = get_object_or_404(RiskProfile,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش پروفایل ریسک  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این پروفایل ریسک  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    @user_is_dabir
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRiskProfile(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='پروفایل ریسک  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewRiskProfile')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='پروفایل ریسک  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewRiskProfile( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskProfile,id = id)
        return obj
    @user_is_dabir
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک پروفایل ریسک "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که پروفایل ریسک   " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    @user_is_dabir
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='پروفایل ریسک  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ListViewRiskProfile')
        return render(request,self.template_name,context)
    
    
    
    

class RiskTeamHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "RiskTeam.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only 
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewRiskTeam( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only 
    def get(self, request, *args, **kwargs):
        form = CreateFormRiskTeam()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک تیم  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک تیم  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)

    @user_is_dabir
    @staff_only
    def post( self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormRiskTeam(request.POST,request.FILES)
        title = self.cleaned_data.get("title")
        
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='تیم  جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewRiskTeam')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='تیم  مورد نظر ساخته نشد !')
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewRiskTeam(ListView):
  
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست تیم  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام تیم  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان' , 'پروفایل ریسک' , 'اعضا تیم' ,'سر فصل ریسک','حوزه فرآیندی']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = RiskTeam.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.riskProfile)
            memberList = ''
            for member in query.memberProfile.all():
                memberList += member.lastName +', '
            data.append(memberList)
          
            
            data.append(query.riskTopic)
            hoze = ''
            for hz in query.hoze.all():
                hoze += hz.title +' - ' 
            data.append(hoze)
   
            

 

         
            
           
            dict_temp = {query.id : data}
            list_data.append(data)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = RiskTeam
    ordering = '-created_at' 
    template_name ='listTeam.html'

class UpdateViewRiskTeam( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskTeam,id = id)
        return obj
    @user_is_dabir
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRiskTeam(instance=obj)
            
            obj = get_object_or_404(RiskTeam,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش تیم  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این تیم  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    @user_is_dabir
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRiskTeam(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='تیم  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewRiskTeam')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='تیم  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewRiskTeam( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskTeam,id = id)
        return obj
    @user_is_dabir
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک تیم "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که تیم   " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    @user_is_dabir
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='تیم  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ListViewRiskTeam')
        return render(request,self.template_name,context)
    

def load_process(request):
    qs_val = list(Process.objects.values())
    
    group_id = request.GET.get('group_id')
    Processes = Process.objects.filter(groupCode=group_id).all()
     
    return JsonResponse({'data': qs_val})

def get_json_group_data(request,group ):
    selected_group = group
    processSelected = list(Process.objects.filter(groupCode=selected_group).values())
    return JsonResponse({'data': processSelected})

@permission_classes([IsAuthenticated])
class ListRiskIdentificationAPI(APIView):
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        query = Committee.objects.all()
        serializers = RiskIdentificationSerializer(query , many=True)
        return Response(serializers.data , status = status.HTTP_200_OK)



class RiskIdentificationHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "RiskIdentification.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @staff_only 
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewRiskIdentification( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createRiskIdentification.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
    @staff_only 
    def get(self, request,activityId, *args, **kwargs):
        form = CreateFormRiskIdentification()
        #عنوان نمایش داده شده در بالای صفحه
        
        header_title  = "ساخت یک شناسایی ریسک  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک شناسایی ریسک  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #دیکشنری داده ها
        header_table   = [ 'ردیف' , 'عنوان ریسک' , 'نام فرآیند','بیشتر' ]
        #اسم داده های جدول
        activitySlected = RiskActivityManager.objects.filter(id =activityId )[0]
        groupFiltered = Group.objects.all().filter(hozeCode = activitySlected.hoze)
        hozeSelected = Hoze.objects.filter(id =activitySlected.hoze.id )[0]
        
        #دریافت تمام داده ها
        queryset = RiskIdentification.objects.all().filter(activity__id = activityId)
        
        list_data = []
       
        #ایجاد لیست داده ها
    
        for query in queryset:
            data = []
            dict_temp = {}
          
        

            
            data.append((0,query.riskFailureModes ))
            data.append((1,query.process ))
            data.append((2,query.id ))
            data.append((3,query.group ))
            data.append((4,query.process.processCode ))
            data.append((5,query.riskCauses ))
            data.append((6,query.riskEffects ))
            data.append((7,query.currentAction ))
            
          
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
            
           
        
        contex= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'list_data':list_data ,'queryset':queryset,
        'header_table':header_table,'activitySlected' : activitySlected ,'groupFiltered':groupFiltered , 'hozeSelected':hozeSelected}
        return render(request,self.template_name,contex)


    @staff_only
    def post( self, request,activityId, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormRiskIdentification(request.POST,request.FILES)
        form.activity = activityId
        form.status = 'identification'
        groupSelected = request.POST.get('group')
        proccessSelected = request.POST.get('process')
        
        
        if(groupSelected == None):
            sweetify.toast(self.request,timer=30000 , icon="error",title ='شناسایی ریسک  مورد نظر ثبت نشد ! انتخاب کردن یک گروه فرآیندی برای شناسایی ریسک الزامی است.')           
            return HttpResponseRedirect(reverse('CreateViewRiskIdentification' , kwargs={'activityId':activityId}) )
        if(proccessSelected == None):
            sweetify.toast(self.request,timer=30000 , icon="error",title ='شناسایی ریسک  مورد نظر ثبت نشد ! انتخاب کردن یک گروه فرآیندی برای شناسایی ریسک الزامی است.')           
            return HttpResponseRedirect(reverse('CreateViewRiskIdentification' , kwargs={'activityId':activityId}) )
        
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='شناسایی ریسک  جدید با موفقیت ساخته شد !!!')
            #return redirect('CreateViewRiskIdentification' , id=32)
            return HttpResponseRedirect(reverse('CreateViewRiskIdentification' , kwargs={'activityId':activityId}))
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='شناسایی ریسک  مورد نظر ساخته نشد !')
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)
    
    # @staff_only
    # def put( self, request, *args, **kwargs):
    #     #فرم دریافت شده
    #     form = CreateFormRiskActivityManager(request.PUT,request.FILES)
     
    #     #بررسی صحت اطلاعات ورودی
    #     if form.is_valid():
    #         form.save()
    #         #تابع نمایش پیغام
    #         sweetify.toast(self.request,timer=30000 , icon="success",title ='شناسایی ریسک  جدید با موفقیت ساخته شد !!!')
    #         #return redirect('CreateViewRiskIdentification' , id=32)
    #         return HttpResponseRedirect(reverse('CreateViewRiskIdentification' , kwargs={'activityId':32}))
    #     else :
    #         sweetify.toast(self.request,timer=30000 , icon="error",title ='شناسایی ریسک  مورد نظر ساخته نشد !')
    #     context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form}
    #     return render(request,self.template_name,context)


class ListViewRiskIdentification(ListView):
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'

    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست شناسایی ریسک  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام شناسایی ریسک  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['فرستنده','نوع فعالیت','حوزه','سرفصل ریسک','وضعیت','تیم', ]
        #اسم داده های جدول
        profileReciver = Profile.objects.filter(user=self.request.user)[0]
        allProfileActivity = RiskActivityManager.objects.filter(reciver = profileReciver).filter(activity = 'identification')
        
        #دریافت تمام داده ها
        queryset = RiskIdentification.objects.all().filter(activity__activity = 'identification')
      
        list_data = []
       
        #ایجاد لیست داده ها
        for query in allProfileActivity:
            data = []
            dict_temp = {}
            
            data.append(query.sender)
            
            data.append('شناسایی ریسک')
            data.append(query.hoze)
            data.append(query.riskTopic)
            if(query.status == 'doing'):
                data.append('در حال انجام')
            else:
                data.append('به اتمام رسید')
            
            
            
            data.append(query.team)
            
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = RiskIdentification
    ordering = '-created_at' 
    template_name ='listRiskIdentification.html'


class ListViewRiskIdentificationConcule(ListView):
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست جمع بندی شناسایی ریسک  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام شناسایی ریسک  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['فرستنده','نوع فعالیت','حوزه','سرفصل ریسک','وضعیت','تیم', ]
        #اسم داده های جدول
        riskProfile = RiskProfile.objects.all().filter(id=self.kwargs.get('id'))[0]
        
        profileReciver = Profile.objects.filter(user=self.request.user)[0]
        allProfileActivity = RiskActivityManager.objects.filter(reciver = profileReciver).filter(activity = 'جمع یندی identification').filter(team__riskProfile = riskProfile)
        
        
        #دریافت تمام داده ها
        
        list_data = []
        #ایجاد لیست داده ها
        hozes= []
        riskTopics = []

        
        for query in allProfileActivity:
            data = []
            dict_temp = {}
            if(query.riskTopic not in riskTopics):
                
                data.append(query.activity)
                
                data.append(query.status)
            
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = RiskIdentification
    ordering = '-created_at' 
    template_name ='listRiskIdentification.html'


class UpdateViewRiskIdentification( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskIdentification,id = id)
        return obj

    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRiskIdentification(instance=obj)
            
            obj = get_object_or_404(RiskIdentification,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش شناسایی ریسک  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این شناسایی ریسک  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRiskIdentification(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='شناسایی ریسک  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewRiskIdentification')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='شناسایی ریسک  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)


class ChangeViewRiskIdentification( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskIdentification,id = id)
        return obj

    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        activitySelected = RiskActivityManager.objects.get(id = kwargs.get('activityId'))
        
        activitySelected.status='done'
        
        
        instanceRiskActivityManager = RiskActivityManager.objects.create(riskProfile = activitySelected.riskProfile ,sender=activitySelected.reciver, reciver=activitySelected.team.riskProfile.committeeRisk.dabir.profile ,status='doing' ,activity='Conclusion' ,team = activitySelected.team , riskTopic=activitySelected.riskTopic,hoze=activitySelected.hoze , previousActivity = activitySelected)
        instanceRiskActivityManager.save()
        activitySelected.nextActivity = instanceRiskActivityManager
        activitySelected.save()
        del(instanceRiskActivityManager)
        #activitySelected.save()
        #ListViewRiskIdentification
        
         #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست شناسایی ریسک  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام شناسایی ریسک  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['فرستنده','نوع فعالیت','حوزه','سرفصل ریسک','وضعیت','تیم', ]
        #اسم داده های جدول
        profileReciver = Profile.objects.filter(user=self.request.user)[0]
        allProfileActivity = RiskActivityManager.objects.filter(reciver = profileReciver)
        
        #دریافت تمام داده ها
        queryset = RiskIdentification.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        # for query in allProfileActivity:
        #     data = []
        #     dict_temp = {}
            
        #     data.append(query.sender)
        #     data.append(query.activity)
        #     data.append(query.team.hoze)
        #     data.append(query.team.riskTopic)
        #     data.append(query.status)
        #     data.append(query.team)
            
            
           
        #     dict_temp = {query.id : data}
        #     list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
         }
        #return context
        #return render(request,self.template_name,context)
        #return redirect('ListViewRiskIdentification')
        return HttpResponseRedirect(reverse('ViewRiskDashboardMember' , kwargs={'profileId':activitySelected.team.riskProfile.id}))

    model = RiskIdentification
    ordering = '-created_at' 
    template_name ='list.html'




class DeleteViewRiskIdentification( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskIdentification,id = id)
        return obj
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        activitySelected = obj.activity
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک شناسایی ریسک "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که شناسایی ریسک   " + obj.riskFailureModes + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='شناسایی ریسک  با موفقیت پاک شد !!!')
            return redirect('CreateViewRiskIdentification' , activitySelected.id)
            
            
        return render(request,self.template_name)
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='شناسایی ریسک  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ListViewRiskIdentification')
        return render(request,self.template_name,context)
    
    
    
    
#RISK ACTIVITY MANAGER

class RiskActivityManagerHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "RiskActivityManager.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only 
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewRiskActivityManager( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only 
    def get(self, request, *args, **kwargs):
        form = CreateFormRiskActivityManager()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک فعالیت  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک فعالیت  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #دیکشنری داده ها
        contex= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)

    @user_is_dabir
    @staff_only
    def post( self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormRiskActivityManager(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='فعالیت  جدید با موفقیت ساخته شد !!!')
            return redirect('OrganizationListViewRiskActivityManager')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='فعالیت  مورد نظر ساخته نشد !')
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewRiskActivityManager(ListView):
  
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست فعالیت  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام فعالیت  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
        
        
        header_table   = ['فرستنده','گیرنده','وضعیت','نوع فعالیت']
        #اسم داده های جدول
        #object_name    = ['title','RiskActivityManagerCode','created_at','updated_at']
        #دریافت تمام داده ها
        queryset = RiskActivityManager.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.sender)
            data.append(query.reciver)
            if(query.status == 'done'):
                data.append('انجام شده')
            else:
                data.append('در حال انجام')
            
            if(query.activity == 'identification'):
                data.append('شناسایی ریسک')
            elif(query.activity == 'Conclusion'):
                data.append('بررسی ریسک ها')
            elif(query.activity == 'measurement'):
                data.append('ارزیابی ریسک')
            


            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data }
        return context

    model = RiskActivityManager
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewRiskActivityManager( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskActivityManager,id = id)
        return obj
    @user_is_dabir
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRiskActivityManager(instance=obj)
            
            obj = get_object_or_404(RiskActivityManager,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش فعالیت  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این فعالیت  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend' : self.extend ,'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    @user_is_dabir
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRiskActivityManager(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='فعالیت  جدید با موفقیت ساخته شد !!!')
                return redirect('OrganizationListViewRiskActivityManager')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='فعالیت  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewRiskActivityManager( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskActivityManager,id = id)
        return obj
    @user_is_dabir
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک فعالیت "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که فعالیت   " + obj.activity + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    @user_is_dabir
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='فعالیت  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('OrganizationListViewRiskActivityManager')
        return render(request,self.template_name,context)
    
    



class RiskIdentificationSelectingHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "RiskIdentificationSelecting.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only 
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewRiskIdentificationSelecting( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createRiskIdentificationSelecting.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only 
    def get(self, request,hoze , profileId, *args, **kwargs):
        
        
        
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک انتخاب ریسک شناسایی شده  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک انتخاب ریسک شناسایی شده  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        header_table   = [ 'شناسه' , 'عنوان ریسک' , 'علل بروز' , 'اثرات بروز' , 'کنترل های فعلی' , 'نام فرآیند' ,'گروه' ]
        #اسم داده های جدول

        #دریافت تمام داده ها
        allGroups = Group.objects.all().filter(hozeCode = hoze)
        
        allDoneActivity = RiskActivityManager.objects.filter(activity = 'Conclusion').filter(status = 'done').filter(hoze__id = hoze)
        allRiskIdentificaion = RiskIdentification.objects.filter()
        queryset = RiskIdentification.objects.all().filter(status = 'identification').filter(hoze = hoze).filter(activity__riskProfile__id = profileId)
        list_data = []
        if(len(queryset) ==0):
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='ریسکی برای بررسی وجود ندارد          !!!')
            return redirect('ListViewRiskIdentificationSelecting' ,profileId )
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.id)
            data.append(query.riskFailureModes)
            data.append(query.riskCauses)
            data.append(query.riskEffects)
            data.append(query.currentAction)
            data.append(query.process)
            data.append(query.group)
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        contex= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'header_table':header_table ,
        'list_data':list_data, 'allGroups':allGroups , 'allDoneActivity':allDoneActivity}
        return render(request,self.template_name,contex)

    @user_is_dabir
    @staff_only
    def post(self, request,hoze ,  *args, **kwargs):
        #فرم دریافت شده
        post_data = request.POST.copy() # to make it mutable
        
        if(post_data['group'] == ''):
            sweetify.toast(self.request,timer=30000 , icon="error",title ='باید یک گروه فرآیندی انتخاب شود!')
            context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
            return HttpResponseRedirect(reverse('CreateViewRiskIdentificationSelecting' , kwargs={'hoze':hoze}) )
        if(post_data['process'] == ''):
            sweetify.toast(self.request,timer=30000 , icon="error",title ='باید یک  فرآیند انتخاب شود!')
            context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
            return HttpResponseRedirect(reverse('CreateViewRiskIdentificationSelecting' , kwargs={'hoze':hoze}) )
        if(post_data['riskIdentifications'] == ''):
            sweetify.toast(self.request,timer=30000 , icon="error",title ='باید از لیست ریسک های شناسایی شده انتخاب نمایید !')
            context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
            return HttpResponseRedirect(reverse('CreateViewRiskIdentificationSelecting' , kwargs={'hoze':hoze}) )
            
        

        profileRecomnder = Profile.objects.filter(user=request.user)[0]
        processSelected = Process.objects.filter(id = post_data['process'] )[0] 
        
        groupSelected = Group.objects.filter(id =post_data['group'])[0]
        teamSelected = RiskTeam.objects.filter(Q(hoze =hoze) & Q())[0]
        #teamSelected = RiskTeam.objects.filter(id =94)[0]
        
        riskTopicSelected = RiskTopic.objects.all().filter(id =teamSelected.riskTopic.id )[0]
  
        allRiskIdentificationsSelectedId = list(map(int, post_data['riskIdentifications'].split(',')))
        hozeSelected = Hoze.objects.all().filter(id=hoze)[0]
       
        
        
        riskProfileSelected = RiskIdentification.objects.filter(id =allRiskIdentificationsSelectedId[0] )[0].activity.riskProfile
        
        for reciver in teamSelected.memberProfile.all():    
            profileReciver = Profile.objects.all().filter(id = reciver.id)[0]
            
            instanceRiskActivityManager = RiskActivityManager.objects.create(
                riskProfile = riskProfileSelected , sender=profileRecomnder, reciver=profileReciver ,
                status='doing' ,activity='measurement' ,
                team = teamSelected ,
                riskTopic=riskTopicSelected,
                hoze=hozeSelected, )
            instanceRiskActivityManager.save()
      
            
            instanceRisk = RiskIdentification.objects.create(
            riskFailureModes=post_data['riskFailureModes'] ,riskCauses=post_data['riskCauses'] ,
            riskEffects=post_data['riskEffects'],team = teamSelected, currentAction=post_data['currentAction'],
            recommender =profileRecomnder ,process =processSelected ,
            group =groupSelected,activity =instanceRiskActivityManager  , hoze = hozeSelected , status = 'measurement'  )
  
            instanceRisk.save()
            
            instanceMeasurement = RiskMeasurement.objects.create(riskIdentificated =instanceRisk ,activity = instanceRiskActivityManager   )    
            instanceMeasurement.save()
        
        
        
     
       
        
            
        
        
        for member in teamSelected.memberProfile.all():
            instance = Notifications.objects.create(recivers=member,title='ارزیابی ریسک', description='با عرض سلام خدمت همکار محترم ، شما یک ارزیابی ریسک در حوزه  ' + str(hozeSelected.title) + ' باید انجام دهید .' ,  status = 'primary' ,  icon = 'alarm')
            instance.link = '/risk/measurement/list'
            instance.save()   
          
        
        
        
        for riskSelectedId in allRiskIdentificationsSelectedId:
            riskSelected = RiskIdentification.objects.filter(id =riskSelectedId )[0]
            riskSelected.status = 'done'
            riskSelected.activity.status = 'done'
            riskSelected.save()
            
        #     #تابع نمایش پیغام
        sweetify.toast(self.request,timer=30000 , icon="success",title ='انتخاب ریسک شناسایی شده  جدید با موفقیت ساخته شد !!!') , 
        return HttpResponseRedirect(reverse('CreateViewRiskIdentificationSelecting' , kwargs={'profileId':instanceRiskActivityManager.riskProfile.id , 'hoze':hoze}) )
        
        # except:
            
        #     sweetify.toast(self.request,timer=30000 , icon="error",title ='انتخاب ریسک شناسایی شده  مورد نظر ساخته نشد !')
        #     context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        #     return render(request,self.template_name,context)


class ListViewRiskIdentificationSelecting(ListView):
  
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "listRiskIdentificationSelecting.html"
    
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only
    
    def get(self, request,profileId, *args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست انتخاب ریسک شناسایی شده  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام انتخاب ریسک شناسایی شده  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['حوزه های ریسک','تعداد ریسک های شناسایی شده']
        #اسم داده های جدول
        riskProfileSelected = RiskProfile.objects.get(id = profileId)
        #دریافت تمام داده ها
       
        activitysForSelecting = RiskActivityManager.objects.filter(activity = 'Conclusion')
        riskSelecting = RiskIdentification.objects.all().filter(activity__riskProfile =riskProfileSelected )
        
       
        alltopics = RiskTopic.objects.all()
        allhozes  = Hoze.objects.all()
        hozes = {}
        finalActivity = []
        for risk in riskSelecting:
           
            if(risk.status != "identification"):
                continue
          
            if risk.hoze in hozes:
                hozes[risk.hoze] +=1
            else:
                hozes[risk.hoze] = 1
        
        list_data = []
        
            
            
        #ایجاد لیست داده ها
        for query in hozes:
            data = []
            dict_temp = {}
         





            data.append(query)
            data.append(hozes[query])
      
           
   
            
           
            dict_temp = {allhozes.filter(title =query )[0].id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,'profileId':profileId,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data ,}
        
        return render(request,self.template_name,context)
    

class ComplateViewRiskProfile( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createCalenderMomayezi.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewRiskDashboard"
    menu_link = 'ViewRiskDashboard'
    def get(self, request,id, *args, **kwargs):
        
        riskProfileSelected = RiskProfile.objects.get(id = id)
        
        activitySelected = RiskActivityManager.objects.all().filter(riskProfile = riskProfileSelected ,activity = 'Conclusion' )
        for activity in activitySelected:

            activity.status = 'done'
            activity.save()
        sweetify.toast(self.request,timer=30000 , icon="success",title ='ثبت تیم های ریسک  به اتمام رسید        !!!')
        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        return redirect('ViewRiskDashboardMember' ,id )




class ViewRiskIdentificationSelecting( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detail.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskIdentificationSelecting,id = id)
        return obj
    @user_is_dabir
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = RiskIdentificationSelecting.objects.all().filter(id=id)[0]
           
            obj = get_object_or_404(RiskIdentificationSelecting,id = id)
            
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "اطلاعات انتخاب ریسک شناسایی شده   "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "چزییات انتخاب ریسک شناسایی شده را در این صفحه می توانید مشاهده کنید"
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
            
            list_data = {'عنوان' : obj.riskFailureModes}
            #ایجاد لیست داده ها
           
            #جدول لیست کلاس ها
            # عنوان های جدول
            
                
            context =  {'object':obj , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,
                'color':color , 'columns':columns,'list_data':list_data,
                'header_table':header_table , 'form':form , }


        return render(request,self.template_name,context)
 

class UpdateViewRiskIdentificationSelecting( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskIdentificationSelecting,id = id)
        return obj
    @user_is_dabir
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRiskIdentificationSelecting(instance=obj)
            
            obj = get_object_or_404(RiskIdentificationSelecting,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش انتخاب ریسک شناسایی شده  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این انتخاب ریسک شناسایی شده  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    @user_is_dabir
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRiskIdentificationSelecting(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='انتخاب ریسک شناسایی شده  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewRiskIdentificationSelecting')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='انتخاب ریسک شناسایی شده  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewRiskIdentificationSelecting( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    @user_is_dabir
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskIdentificationSelecting,id = id)
        return obj
    @user_is_dabir
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک انتخاب ریسک شناسایی شده "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که انتخاب ریسک شناسایی شده   " + obj.riskFailureModes + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    @user_is_dabir
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='انتخاب ریسک شناسایی شده  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ListViewRiskIdentificationSelecting')
        return render(request,self.template_name,context)
    







class RiskMeasurementHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "RiskMeasurement.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class  CreateViewRiskMeasurement( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createRiskMeasurement.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @staff_only
    def get(self, request,hoze , profileId, *args, **kwargs):
        form = CreateFormRiskMeasurement()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک ارزیابی ریسک سازمانی جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک ارزیابی ریسک سازمانی جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        profilereciver = Profile.objects.get(user = request.user)
        if(request.user.is_superuser):
            allActivityRiskMeasurement = RiskMeasurement.objects.all().filter(activity__riskProfile__id = profileId).filter(activity__hoze = hoze)
        else:
            allActivityRiskMeasurement = RiskMeasurement.objects.all().filter(activity__reciver = profilereciver).filter(activity__riskProfile__id = profileId).filter(activity__hoze = hoze)
        #teamSelected = allActivityRiskMeasurement[0].activity.team
        tiskTopicSelected = allActivityRiskMeasurement[0].activity.riskTopic
        hozeSelected = allActivityRiskMeasurement[0].activity.hoze.title
        #دیکشنری داده ها
        contex= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'allActivityRiskMeasurement' : allActivityRiskMeasurement,
        'riskTopicSelected':tiskTopicSelected,'hozeSelected':hozeSelected}
        return render(request,self.template_name,contex  )

    @staff_only
    def post(self, request, hoze, profileId,*args, **kwargs):
        #فرم دریافت شده
        form = CreateFormRiskMeasurement(request.POST,request.FILES)
   
        
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='ارزیابی ریسک سازمانی جدید با موفقیت ساخته شد !!!')
            return redirect('OrganizationListViewRiskMeasurement')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='ارزیابی ریسک سازمانی مورد نظر ساخته نشد !')
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewRiskMeasurement(ListView):
  
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "listRiskMeasurement.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @staff_only
    def get(self, request,profileId, *args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست ریسک‌های قابل ارزیابی "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام انتخاب ریسک شناسایی شده  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['حوزه های ریسک','تعداد ریسک های شناسایی شده' , 'تعداد باقی مانده']
        #اسم داده های جدول

        #دریافت تمام داده ها
        profileReciver = Profile.objects.filter(user=self.request.user)[0]
        if (self.request.user.is_superuser):
            activitysForMeasurement = RiskActivityManager.objects.filter(activity = 'measurement').filter(riskProfile = profileId)
        else:
            activitysForMeasurement = RiskActivityManager.objects.filter(activity = 'measurement').filter(reciver = profileReciver).filter(riskProfile = profileId)
        riskSelecting = RiskIdentification.objects.all()
        
       
        alltopics = RiskTopic.objects.all()
        allhozes  = Hoze.objects.all()
        hozeList = []
        finalActivity = []
        counter = 0

        for hozeSelected in allhozes:
            temp = {}
            if(activitysForMeasurement.filter(hoze =hozeSelected ).count() == 0 ):
                pass
            else:
                temp = {'hoze' :hozeSelected , 'activityDoing' : activitysForMeasurement.filter(hoze=hozeSelected).count() - activitysForMeasurement.filter(hoze=hozeSelected).filter(status = 'done').count() , 'activityDone' : activitysForMeasurement.filter(hoze=hozeSelected).filter(status = 'done').count()  }
                hozeList.append(temp)

        # for activitySelected in activitysForMeasurement:
        #     risk = RiskIdentification.objects.get(activity = activitySelected)[0]
         
        #     if(risk.status != "measurement"):
        #         continue
           
        #     if risk.hoze in hozes :
        #         hozes[risk.hoze] +=1
        #     else:
        #         hozes[risk.hoze] = 1
        #     if(risk.activity.status == 'doing'):
        #         counter+=1
        list_data = []
        allLenght = 0
        # for alls in hozes:
        #     allLenght+= hozes[alls]
            
            
        #ایجاد لیست داده ها
        # for query in hozes:
        #     data = []
        #     dict_temp = {}
         





        #     data.append(query)
        #     data.append(hozes[query])
        #     data.append(counter)
           
   
            
           
        #     dict_temp = {allhozes.filter(title =query )[0].id : data}
        #     list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,'profileId':profileId,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data , 'hozeList': hozeList}

        return render(request,self.template_name,context  )



class ChangeViewRiskMeasurement( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            
            obj = get_object_or_404(RiskMeasurement,id = id)
     
        return obj
    @staff_only
    def post(self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        post_data = request.POST.copy()
        riskId = str(id)
        riskSeverity =  post_data[str('riskSeverity')]
        riskOccurrence =  post_data[str('riskOccurrence')]
        riskDetection =  post_data[str('riskDetection')]
        hozeSelected = post_data['hoze']
        if ((riskSeverity == '' or riskOccurrence =='' or riskDetection =='') and riskSeverity + riskOccurrence + riskDetection != '' ):
            
         
            sweetify.toast(self.request,timer=30000 , icon="error",title ='ارزیابی ریسک  مورد نظر ثبت نشد، در ارزیابی یا باید تمام المان های خواسته شده را وارد کنید و یا هیچ کدام را وارد نکنید. !')
            return HttpResponseRedirect(reverse('CreateViewRiskMeasurement' , kwargs={'hoze':hozeSelected}) )

        hozeSelected = post_data['hoze']
        obj = self.get_obj()
        
        activitySelected = obj.activity
        activitySelected.status = 'done'
        activitySelected.save()
       
        if obj is not None:
            form = CreateFormRiskMeasurement(request.POST or request.FILES,instance=obj)
            
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='ارزیابی ریسک سازمانی جدید با موفقیت ساخته شد !!!')
                return redirect('CreateViewRiskMeasurement' , hozeSelected , obj.activity.riskProfile.id )
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='ارزیابی ریسک سازمانی مورد نظر ساخته نشد !')           
            context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class UpdateViewRiskMeasurement( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskMeasurement,id = id)
        return obj
    @staff_only
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRiskMeasurement(instance=obj)
            
            obj = get_object_or_404(RiskMeasurement,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش ارزیابی ریسک سازمانی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این ارزیابی ریسک سازمانی ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    @staff_only
    def post(self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRiskMeasurement(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='ارزیابی ریسک سازمانی جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewRiskMeasurement')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='ارزیابی ریسک سازمانی مورد نظر ساخته نشد !')           
            context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewRiskMeasurement( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    extend ='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    @staff_only
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskMeasurement,id = id)
        return obj
    @staff_only
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک ارزیابی ریسک سازمانی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که ارزیابی ریسک سازمانی  " + obj.RiskIdentificated.riskFailureModes + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    @staff_only
    def post(self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='ارزیابی ریسک سازمانی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('OrganizationListViewRiskMeasurement')
        return render(request,self.template_name,context)
    

class RiskProcessRelatedHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    menuBack = 'ViewRiskDashboard'
    template_name = "RiskProcessRelated.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewRiskProcessRelated( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    def get(self, request , profileId, *args, **kwargs):
        form = CreateFormRiskProcessRelated()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک ارتباط ریسک با فرآیند جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک ارتباط ریسک با فرآیند جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        allProccess = Process.objects.all()
        allMeasurement = RiskMeasurement.objects.all().filter(riskIdentificated__activity__riskProfile__id = profileId) 
        for process in allProccess:
            processMeasurements = allMeasurement.filter(riskIdentificated__process = process)
            
            if(len(processMeasurements)!= 0):
                riskSeverityList    = []
                riskOccurrenceList  = []
                riskDetectionList   = []
                for processMeasurement in processMeasurements:
                    if(processMeasurement.riskSeverity == None or processMeasurement.riskOccurrence == None or processMeasurement.riskDetection ==None ):
                        if(processMeasurement.riskSeverity == None and processMeasurement.riskOccurrence == None and processMeasurement.riskDetection ==None ):
                            
                            continue
                        
                    riskSeverityList.append(processMeasurement.riskSeverity)
                    riskOccurrenceList.append(processMeasurement.riskOccurrence)
                    riskDetectionList.append(processMeasurement.riskDetection)
                if(len(riskSeverityList) == 0 or len(riskOccurrenceList) == 0  or len(riskDetectionList) == 0):
                    
                    continue
                
                avgRiskSeverity   = avrage(riskSeverityList)
                stdRiskSeverity   = std(riskSeverityList)
                avgRiskOccurrence = avrage(riskOccurrenceList)
                stdRiskOccurrence   = std(riskOccurrenceList)
                avgRiskDetection  = avrage(riskDetectionList)
                stdRiskDetection   = std(riskDetectionList)
                rpn = avgRiskSeverity *avgRiskOccurrence * avgRiskDetection
                rpnAdjusted = float(rpn) *process.impactFactor
                
                #instanceRiskProcessRelated = RiskProcessRelated.objects.create(riskProfile = RiskProfile.objects.get(id=profileId) ,title = '1' )
                instance = RiskProcess.objects.create(riskProfileRelated =RiskProfile.objects.get(id = profileId)  , riskMeasurement = processMeasurements[0],process = process,avgRiskSeverity = avgRiskSeverity,avgRiskOccurrence = avgRiskOccurrence,avgRiskDetection =avgRiskDetection ,rpn = rpn,rpnAdjusted = rpnAdjusted)
                instance.save()
        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return redirect('ViewRiskDashboard')


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormRiskProcessRelated(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            instanceRiskProfileRelated = form.save()
            allProccess = Process.objects.all()
            allMeasurement = RiskMeasurement.objects.all().filter(riskIdentificated__activity__riskProfile = instanceRiskProfileRelated.riskProfile) 
            for process in allProccess:
                processMeasurements = allMeasurement.filter(riskIdentificated__process = process)
                if(len(processMeasurements)!= 0):
                    riskSeverityList    = []
                    riskOccurrenceList  = []
                    riskDetectionList   = []
                    for processMeasurement in processMeasurements:
                        if(processMeasurement.riskSeverity == None or processMeasurement.riskOccurrence == None or processMeasurement.riskDetection ==None ):
                            if(processMeasurement.riskSeverity == None and processMeasurement.riskOccurrence == None and processMeasurement.riskDetection ==None ):
                               
                                continue
                            
                        riskSeverityList.append(processMeasurement.riskSeverity)
                        riskOccurrenceList.append(processMeasurement.riskOccurrence)
                        riskDetectionList.append(processMeasurement.riskDetection)
                    if(len(riskSeverityList) == 0 or len(riskOccurrenceList) == 0  or len(riskDetectionList) == 0):
                       
                        continue
                    
                    avgRiskSeverity   = avrage(riskSeverityList)
                    stdRiskSeverity   = std(riskSeverityList)
                    avgRiskOccurrence = avrage(riskOccurrenceList)
                    stdRiskOccurrence   = std(riskOccurrenceList)
                    avgRiskDetection  = avrage(riskDetectionList)
                    stdRiskDetection   = std(riskDetectionList)
                    rpn = avgRiskSeverity *avgRiskOccurrence * avgRiskDetection
                    rpnAdjusted = float(rpn) *process.impactFactor
                    
                    
                    instance = RiskProcess.objects.create(riskProcessRelated = instanceRiskProfileRelated , riskMeasurement = processMeasurements[0],process = process,avgRiskSeverity = avgRiskSeverity,avgRiskOccurrence = avgRiskOccurrence,avgRiskDetection =avgRiskDetection ,rpn = rpn,rpnAdjusted = rpnAdjusted)
                    instance.save()
                    
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='ارتباط ریسک با فرآیند جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewRiskProcessRelated')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='ارتباط ریسک با فرآیند مورد نظر ساخته نشد !')
        context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewRiskProcessRelated(ListView):
  


    extend='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only 
    
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست ارتباط ریسک با فرآیند ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام ارتباط ریسک با فرآیند ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
    
        
        header_table   = ['ریسک پروفایل','عنوان']
        #اسم داده های جدول
        object_name    = ['title','RiskProcessRelated']
        #دریافت تمام داده ها
        queryset = RiskProcessRelated.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.riskProfile)
            data.append(query.title)
            
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data }
        return context

    model = RiskProcessRelated
    ordering = '-created_at' 
    template_name ='listRiskProcessRelated.html'

class UpdateViewRiskProcessRelated( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend='baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @user_is_dabir
    @staff_only 
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskProcessRelated,id = id)
        return obj
    @user_is_dabir
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRiskProcessRelated(instance=obj)
            
            obj = get_object_or_404(RiskProcessRelated,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش ارتباط ریسک با فرآیند "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این ارتباط ریسک با فرآیند ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self) ,'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    @user_is_dabir
    @staff_only 
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRiskProcessRelated(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='ارتباط ریسک با فرآیند جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewRiskProcessRelated')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='ارتباط ریسک با فرآیند مورد نظر ساخته نشد !')           
            context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewRiskProcessRelated( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    menuBack = 'ViewRiskDashboard'
    template_name = "delete.html"
    extend = 'baseEmployee.html'
    #تایع یافتن رکورد خاص
    @user_is_dabir
    @staff_only 
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RiskProcessRelated,id = id)
        return obj
    @user_is_dabir
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک ارتباط ریسک با فرآیند"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که ارتباط ریسک با فرآیند  " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    @user_is_dabir
    @staff_only 
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='ارتباط ریسک با فرآیند با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ListViewRiskProcessRelated')
        return render(request,self.template_name,context)
    


class ListViewRiskProcess(ListView):
  

    menuBack = 'ViewRiskDashboard'
    extend='baseEmployee.html'
    @staff_only 
    def get(self, request , profileId,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "گزارش ریسک های شناسایی شده"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام ریسک فرآیند ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        

        
        header_table   = ['ریسک پروفایل','عنوان']
        #اسم داده های جدول
        object_name    = ['title','RiskProcessRelated']
        #دریافت تمام داده ها
        allRiskProcess = RiskProcess.objects.all().filter(riskProfileRelated__id = profileId)
        allProcess = Process.objects.all()
        allGroupProcess = Group.objects.all()
        
        list_data = []
        highRisk = []
        medianRisk =[]
        lowRisk = []
        allRpn = []
        allRpnAdjusted = []
        maxRpnAdjustedGroup = 0
        riskGroupProccesList = []
        riskGroupProccess = []
        riskBarez1 = 0
        riskBarez2 = 0
        riskMedian = 0
        riskLow    = 0

        for riskProcess in allRiskProcess:
         
            
            allRpn.append(riskProcess.rpn)
            allRpnAdjusted.append(riskProcess.rpnAdjusted)
            
        
        avgAllRpn           = avrage(allRpn)
        avgAllRpnAdjusted   = avrage(allRpnAdjusted)
        
        stdAllRpn           = std(allRpn)
        stdAllRpnAdjusted   = std(allRpnAdjusted)
        
        for risk in allRiskProcess:
            
            if(risk.rpnAdjusted > avgAllRpnAdjusted +stdAllRpnAdjusted ):
                riskTemp = (risk , '1' , 'ریسک بارز 1')
                #highRisk.append(risk)
                highRisk.append(riskTemp)
                riskBarez1 +=1
                continue
            
            if(risk.avgRiskSeverity >= 9 or risk.avgRiskOccurrence >= 9):
                riskTemp = (risk , '2' ,'ریسک بارز 2' )
                #highRisk.append(riskProcess)
                highRisk.append(riskTemp)
                riskBarez2 +=1
                continue
            
            if(risk.process.groupCode.id not in riskGroupProccess):
                
                riskGroupProccess.append(risk.process.groupCode.id)
                
            else:
                
                # if(risk.rpnAdjusted > sum(riskGroupProccess) ):
                #     riskGroupProccess.append(risk)
                pass
            riskGroupProccesList.append(riskGroupProccess)
            
            
            
            
            if(risk.rpnAdjusted > abs(avgAllRpnAdjusted -stdAllRpnAdjusted) and risk.rpnAdjusted < avgAllRpnAdjusted +stdAllRpnAdjusted):
                riskTemp = (risk , '4' , 'ریسک متوسط')
                #highRisk.append(risk)
                highRisk.append(riskTemp)
                riskMedian +=1
                continue
          
            if(risk.rpnAdjusted <abs( avgAllRpnAdjusted -stdAllRpnAdjusted) ):
                riskTemp = (risk , '5' , 'ریسک پایین')
                riskLow+=1
                #highRisk.append(risk)
                highRisk.append(riskTemp)

        selectedLevel =  request.GET.get('level') 
        selectedHoze =  request.GET.get('hoze') 
        
        
        
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data ,'highRisk' : highRisk , 'riskGroupProccesList':riskGroupProccesList,
         'riskBarez1' : riskBarez1 ,'riskBarez2' : riskBarez2 ,'riskMedian' : riskMedian ,'riskLow' : riskLow  , 'selectedLevel':selectedLevel , 'selectedHoze':selectedHoze}
        return render(request,self.template_name , context)

    model = RiskProcessRelated
    ordering = '-title' 
    template_name ='riskProcces1.html'
    


class ListViewRiskProcess2(ListView):
  

    menuBack = 'ViewRiskDashboard'
    extend='baseEmployee.html'
    @staff_only 
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست ریسک فرآیند ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام ریسک فرآیند ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        

        
        header_table   = ['ریسک پروفایل','عنوان']
        #اسم داده های جدول
        object_name    = ['title','RiskProcessRelated']
        #دریافت تمام داده ها
        allRiskProcess = RiskProcess.objects.all()
        allProcess = Process.objects.all()
        allGroupProcess = Group.objects.all()
        
        list_data = []
        highRisk = []
        medianRisk =[]
        lowRisk = []
        allRpn = []
        allRpnAdjusted = []
        maxRpnAdjustedGroup = 0
        riskGroupProccesList = []
        riskGroupProccess = []
        
        for riskProcess in allRiskProcess:
         
            
            allRpn.append(riskProcess.rpn)
            allRpnAdjusted.append(riskProcess.rpnAdjusted)
            
            if(riskProcess.avgRiskSeverity > 8 or riskProcess.avgRiskOccurrence > 8):
                riskTemp = (riskProcess , '2')
                #highRisk.append(riskProcess)
                highRisk.append(riskTemp)
                continue
            
            if(riskProcess.process.groupCode.id not in riskGroupProccess):
                
                riskGroupProccess.append(riskProcess.process.groupCode.id)
                
            else:
             
                if(riskProcess.rpnAdjusted > riskGroupProccess ):
                    riskGroupProccess.append(riskProcess)
            riskGroupProccesList.append(riskGroupProccess)
        avgAllRpn           = avrage(allRpn)
        avgAllRpnAdjusted   = avrage(allRpnAdjusted)
        
        stdAllRpn           = std(allRpn)
        stdAllRpnAdjusted   = std(allRpnAdjusted)
        
        for risk in allRiskProcess:
          
            if(risk.rpnAdjusted > avgAllRpn +stdAllRpnAdjusted ):
                riskTemp = (risk , '1')
                #highRisk.append(risk)
                highRisk.append(riskTemp)
                
            if(risk.rpnAdjusted > avgAllRpn -stdAllRpnAdjusted and risk.rpnAdjusted < avgAllRpn +stdAllRpnAdjusted):
                riskTemp = (risk , '4')
                #highRisk.append(risk)
                highRisk.append(riskTemp)
                
            if(risk.rpnAdjusted < avgAllRpn -stdAllRpnAdjusted ):
                riskTemp = (risk , '5')
                #highRisk.append(risk)
                highRisk.append(riskTemp)
        
        
        
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data ,'highRisk' : highRisk , 'riskGroupProccesList':riskGroupProccesList}
        return context

    model = RiskProcessRelated
    ordering = '-created_at' 
    template_name ='riskProcces.html'
    

    
    
class ViewRiskDashboard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "clearDashboard.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
     
    def get(self, request ,*args, **kwargs):
        profileSelected = Profile.objects.get(user = request.user)
        
        visio = 'شناسایی و  ارزیابی ریسک‌ها و فرصت‌ها.vsdx'
        createNewProfile = None
        responsible_link = None
        member_link =  None
        if(request.GET.get('profileId',None)):
            profileRiskSelected = RiskProfile.objects.get(id = request.GET['profileId'])
        else:
            profileRiskSelected = RiskProfile.objects.all().last()
        memberCount = RiskActivityManager.objects.all().filter(Q(riskProfile = profileRiskSelected)& Q(reciver__user = request.user) &Q(status = 'doing')).count()
        responsibleCount = RiskActivityManager.objects.all().filter(Q(riskProfile = profileRiskSelected)  &Q(status = 'doing')).count()
        partials = 'partials/riskDashboard.html'
        header_title = " ریسک های سازمان"
        header_table   = ['ریسک پروفایل','عنوان']
        #اسم داده های جدول
        object_name    = ['title','RiskProcessRelated']
        #دریافت تمام داده ها
        jobBankSelected = JobBank.objects.get(profile__id = profileSelected.id)
        allRiskProcess = RiskProcess.objects.all().filter(riskProfileRelated = profileRiskSelected)
        if(profileRiskSelected.committeeRisk.dabir.profile ==profileSelected or profileSelected.user.is_superuser):
            responsible_link = 'ViewRiskDashboardResponsible'    
            createNewProfile = 'CreateViewRiskProfile'
        if(jobBankSelected in profileRiskSelected.committeeRisk.members.all()):
            member_link = 'ViewRiskDashboardMember'
        allProcess = Process.objects.all()
        allGroupProcess = Group.objects.all()
        allProfile = RiskProfile.objects.all()
        list_data = []
        highRisk = []
        medianRisk =[]
        lowRisk = []
        allRpn = []
        allRpnAdjusted = []
        maxRpnAdjustedGroup = 0
        riskGroupProccesList = []
        riskGroupProccess = []

        riskBarez1 = 0
        riskBarez2 = 0
        riskMedian = 0
        riskLow    = 0

        riskBarez1Percent = 0.0
        riskBarez2Percent = 0.0
        riskMedianPercent = 0.0
        riskLowPercent    = 0.0

        totalRisk = 0
        
        for riskProcess in allRiskProcess:
         
            x = riskProcess.id
            allRpn.append(riskProcess.rpn)
            allRpnAdjusted.append(riskProcess.rpnAdjusted)
            
        
        avgAllRpn           = avrage(allRpn)
        avgAllRpnAdjusted   = avrage(allRpnAdjusted)
        
        stdAllRpn           = std(allRpn)
        stdAllRpnAdjusted   = std(allRpnAdjusted)
        
        for risk in allRiskProcess:
            
            if(risk.rpnAdjusted > avgAllRpnAdjusted +stdAllRpnAdjusted ):
                riskTemp = (risk , '1' , 'ریسک بارز 1')
                #highRisk.append(risk)
                highRisk.append(riskTemp)
                riskBarez1 +=1
                continue
            
            if(risk.avgRiskSeverity >= 9 or risk.avgRiskOccurrence >= 9):
                riskTemp = (risk , '2' ,'ریسک بارز 2' )
                #highRisk.append(riskProcess)
                highRisk.append(riskTemp)
                riskBarez2 +=1
                continue
            
            if(risk.process.groupCode.id not in riskGroupProccess):
                
                riskGroupProccess.append(risk.process.groupCode.id)
                
            else:
                
                # if(risk.rpnAdjusted > sum(riskGroupProccess) ):
                #     riskGroupProccess.append(risk)
                pass
            riskGroupProccesList.append(riskGroupProccess)
            
            
            
            
            if(risk.rpnAdjusted > abs(avgAllRpnAdjusted -stdAllRpnAdjusted) and risk.rpnAdjusted < avgAllRpnAdjusted +stdAllRpnAdjusted):
                riskTemp = (risk , '4' , 'ریسک متوسط')
                #highRisk.append(risk)
                highRisk.append(riskTemp)
                riskMedian +=1
                continue
         
            if(risk.rpnAdjusted <abs( avgAllRpnAdjusted -stdAllRpnAdjusted) ):
                riskTemp = (risk , '5' , 'ریسک پایین')
                riskLow+=1
                #highRisk.append(risk)
                highRisk.append(riskTemp)
        
        
        
        #عنوان نمایش داده شده در بالای صفحه
    
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        totalRisk =riskBarez1 +riskBarez2 +riskMedian +riskLow
        if(totalRisk == 0):
            riskBarez1Percent = 0
            riskBarez2Percent = 0
            riskMedianPercent = 0
            riskLowPercent = 0
        else:    
            riskBarez1Percent = (riskBarez1 / totalRisk)*100
            riskBarez2Percent = (riskBarez2 / totalRisk)*100
            riskMedianPercent = (riskMedian / totalRisk)*100
            riskLowPercent = (riskLow / totalRisk)*100
        
        
            
        
        #رنگ             
        columns       = 1
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,'member_link':member_link,
        'discribtion':discribtion,'icon_name':icon_name,'header_title':header_title,'responsible_link':responsible_link,
        'columns':columns , 'color':color , 'header_table': header_table ,'partials':partials,'profileSelected':profileRiskSelected,
         'object_name' : object_name ,  'list_data' : list_data ,'highRisk' : highRisk , 'riskGroupProccesList':riskGroupProccesList,'createNewProfile':createNewProfile ,
         'riskBarez1' : riskBarez1 ,'riskBarez2' : riskBarez2 ,'riskMedian' : riskMedian ,'riskLow' : riskLow ,'totalRisk':totalRisk ,'riskBarez1Percent':riskBarez1Percent ,'riskBarez2Percent':riskBarez2Percent ,'riskMedianPercent':riskMedianPercent ,'riskLowPercent':riskLowPercent ,'allProfile' :allProfile ,
         'responsibleCount':responsibleCount , 'memberCount': memberCount , 'visio':visio , 'profileRiskSelected':profileRiskSelected}

        return render(request,self.template_name,context)
    
    
    
class ViewRiskDashboardResponsible( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "dashboardResponsible.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @staff_only 
    def get(self, request,profileId=None ,*args, **kwargs):


        header_table   = ['ریسک پروفایل','عنوان']
        #اسم داده های جدول
        object_name    = ['title','RiskProcessRelated']
        #دریافت تمام داده ها
        
        
        list_data = []
       
        profileSelected = RiskProfile.objects.get(id = profileId)
      
        steps_link = ['#','ViewRiskProfile','ListViewRiskIdentification' , 'ListViewRiskIdentificationSelecting','ListViewRiskMeasurement' ]
        steps = []
        for idx, step in enumerate(profileSelected.STEP_LIST):
        
            dict_temp = {}
            dict_temp['step'] = step[0]
            dict_temp['title'] = step[1]
            dict_temp['link'] = steps_link[idx]
            dict_temp['stepId'] = idx
            dict_temp['profileId'] = profileSelected.id

            steps.append(dict_temp)
            
        currentStep = int(profileSelected.step) - 1
        lenStep = len(profileSelected.STEP_LIST) -1
        linkChange = 'ViewChangeRiskProfileStep'
        allActivity = RiskActivityManager.objects.all().filter(riskProfile = profileSelected).order_by('status')
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "داشبور دیبر ریسک"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

       
            
        
        #رنگ             
        columns       = 1
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name, 'currentStep':currentStep,'lenStep':lenStep ,
        'columns':columns , 'color':color , 'header_table': header_table ,'linkChange':linkChange,
         'object_name' : object_name ,  'list_data' : list_data , 'profileSelected' :profileSelected ,'steps':steps , 'allActivity':allActivity}

        return render(request,self.template_name,context)
    
    
class ViewRiskDashboardMember( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "dashboardMember.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @staff_only 
    def get(self, request,profileId=None ,*args, **kwargs):


        header_table   = ['ریسک پروفایل','عنوان']
        #اسم داده های جدول
        object_name    = ['title','RiskProcessRelated']
        #دریافت تمام داده ها
        
        
        list_data = []
       
        profileSelected = RiskProfile.objects.get(id = profileId)
      
        steps_link = ['#','ViewRiskProfile' ,'ListViewRiskIdentification' , 'ListViewRiskIdentificationSelecting','ListViewRiskMeasurement' ,'#']
        steps = []
        for idx, step in enumerate(profileSelected.STEP_LIST):
        
            dict_temp = {}
            dict_temp['step'] = step[0]
            dict_temp['title'] = step[1]
            dict_temp['link'] = steps_link[idx]

            steps.append(dict_temp)
        allActivity = []
        if(request.user.is_superuser):
            query = RiskActivityManager.objects.all().filter(riskProfile = profileSelected)
        else:
            query = RiskActivityManager.objects.all().filter(Q(riskProfile = profileSelected)& Q(reciver__user = request.user)).order_by('status')
        for item in query:
            if(item.activity == 'identification' and item.status =='doing'):
                allActivity.append(('CreateViewRiskIdentification',item , item.id , -1))    
            elif(item.activity == 'measurement' and item.status =='doing'):
                if(item.activity == item.ACTIVITY_LIST[int(profileSelected.step)-1][0]):
                    allActivity.append(('ListViewRiskMeasurement',item , profileSelected.id,-1))    
                else:
                    #allActivity.append(('#' , item))
                    allActivity.append(('ListViewRiskMeasurement',item , profileSelected.id,-1))
                    
            elif(item.activity == 'team' and item.status =='doing'):
                allActivity.append(('ViewRiskProfile'  ,item , item.riskProfile.id , -1))  
            elif(item.activity == 'Conclusion' and item.status =='doing') :
                if(item.activity == item.ACTIVITY_LIST[int(profileSelected.step)-1][0]):
                    allActivity.append(('ListViewRiskIdentificationSelecting'  ,item ,item.riskProfile.id, -1))  
                else:
                    #allActivity.append(('#' , item))
                    allActivity.append(('ListViewRiskIdentificationSelecting'  ,item ,item.riskProfile.id, -1))  
            else:
                allActivity.append(('#' , item))
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "داشبور اعضا ریسک"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

       
            
        
        #رنگ             
        columns       = 1
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,'profileSelected':profileSelected,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data , 'profileSelected' :profileSelected ,'steps':steps , 'allActivity':allActivity , 'stepsLink':steps_link}

        return render(request,self.template_name,context)
    

class ViewChangeRiskProfileStep( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
   
    template_name = "dashboardResponsible.html"
    
    @staff_only 
    def get(self, request,profileId=None , stepId=None ,*args, **kwargs):

        profileSelected = RiskProfile.objects.get(id = profileId)
        lenSteps = len(profileSelected.STEP_LIST)
        profileSelected.STEP_LIST[stepId]
        
        x = profileSelected.STEP_LIST[stepId]
        
        
        
        allActivity = RiskActivityManager.objects.all().filter(Q(riskProfile = profileSelected)& Q(status = 'doing'))
        for activity in allActivity:
            x= activity.ACTIVITY_LIST[stepId]
            y= activity.activity 
            
            if(activity.activity == activity.ACTIVITY_LIST[stepId][0]):
                
                activity.status = 'doNot'
                activity.save()
        if(stepId +2 != (lenSteps)):
            x = profileSelected.STEP_LIST[stepId+2]
            
            
            profileSelected.step = x[0]
            
            profileSelected.save()
          
            
        else:
            
            x = profileSelected.STEP_LIST[-1]
            
            
            profileSelected.step = x[0]
            
            
            profileSelected.save()
            y=  profileSelected.step
        g= profileSelected.step
        
        if(profileSelected.step == '4'):
            
            return redirect('CreateViewRiskProcessRelated', profileId=profileSelected.id)
      
        #دیکشنری داده ها
        context = {}

        return redirect('ViewRiskDashboardResponsible', profileId=profileSelected.id)
    
  
    
class ViewRiskProcces( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "viewRiskProcces.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):


        allRiskProcess = RiskProcess.objects.all()
        allProcess = Process.objects.all()
        allGroupProcess = Group.objects.all()
        riskProcessSelected = RiskProcess.objects.all().filter(id = id)[0]
        proccessSelected = riskProcessSelected.process
        
        extraDataSelected = extraData.objects.all().filter(RiskProcessRelated =riskProcessSelected )[0]
        riskProcess = riskProcessSelected
        list_data = []
        highRisk = []
        medianRisk =[]
        lowRisk = []
        allRpn = []
        allRpnAdjusted = []
        maxRpnAdjustedGroup = 0
        riskGroupProccesList = []
        riskGroupProccess = []
        
        for riskProcess in allRiskProcess:
         
            
            allRpn.append(riskProcess.rpn)
            allRpnAdjusted.append(riskProcess.rpnAdjusted)
            
        
        avgAllRpn           = avrage(allRpn)
        avgAllRpnAdjusted   = avrage(allRpnAdjusted)
        
        stdAllRpn           = std(allRpn)
        stdAllRpnAdjusted   = std(allRpnAdjusted)
        
        
        
        
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
        context =  {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self),'discribtion':discribtion,'icon_name':icon_name,
        'color':color , 'columns':columns , 'proccessSelected' : proccessSelected ,  'riskProcess' : riskProcessSelected ,  'avgAllRpn' : avgAllRpn , 'avgAllRpnAdjusted' : avgAllRpnAdjusted , 'stdAllRpn' : stdAllRpn , 'stdAllRpnAdjusted' : stdAllRpnAdjusted , 'extraDataSelected':extraDataSelected} 

        return render(request,self.template_name,context)
    
    
    

class UpdateRiskManualy( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    template_name = "CorrectiveAction.html"
    def get(self, request,*args, **kwargs):
        #CorrectiveActionActivityManager.objects.create( sender =  , reciver =  , status =  , activity =  , CorrectiveActionRelated =  , texts =  , previousActivity =  , nextActivity =  , confirmations =  )
        import pandas as pd
        ed = pd.read_excel("ed.xlsx")
        ed= ed.astype(str)
        ri = pd.read_excel("ri.xlsx")
        ri= ri.astype(str)
        rm = pd.read_excel("rm.xlsx")
        rm= rm.astype(str)
        riskTeamSelected = RiskTeam.objects.get(id = 44)
        riskProfileSelected = RiskProfile.objects.get(id = 12) 
        riskActivitySelected = RiskActivityManager.objects.get(id = 321)
        riskRecomenderSelected = Profile.objects.get(id = 324)


        
        for index, row in ri.iterrows():
            riCreated = RiskIdentification.objects.create(id = row['id']	,riskFailureModes = row['riskFailureModes'] , riskCauses= row['riskCauses'] ,	riskEffects= row['riskEffects'] ,	currentAction= row['currentAction'] ,	team= riskTeamSelected ,	recommender= riskRecomenderSelected ,	process=Process.objects.get(id = row['process'])  ,	group=Group.objects.get(id = row['group'])  ,	activity= riskActivitySelected ,		hoze=Hoze.objects.get(id = row['hoze'])  )
            rmCreated = RiskMeasurement.objects.create(id = row['id'] , riskSeverity = int(float(rm.loc[index:index]['riskSeverity'])) , riskOccurrence = int(float(rm.loc[index:index]['riskOccurrence'])) , riskDetection = int(float(rm.loc[index:index]['riskDetection'])) , riskIdentificated = RiskIdentification.objects.get(id = row['id']) , activity = riskActivitySelected ,  ) 
            rpCreated = RiskProcess.objects.create(id = row['id'] , riskProfileRelated = riskProfileSelected ,  riskMeasurement = rmCreated, process =Process.objects.get(id = row['process'])   , avgRiskSeverity = (rm.loc[index:index]['riskSeverity']) , avgRiskOccurrence = (rm.loc[index:index]['riskOccurrence']) , avgRiskDetection = (rm.loc[index:index]['riskDetection']) ,  rpn = (ed.loc[index:index]['rpn']), rpnAdjusted =(ed.loc[index:index]['rpnAdjusted']) )
            #edCreated = extraData.objects.create(id = row['id'], RiskProcessRelated = rpCreated , control = str(ed.loc[index:index]['control'][0]), eghdam = str(ed.loc[index:index]['eghdam'][0]),masol = str(ed.loc[index:index]['masol'][0]) , tarikh = str(ed.loc[index:index]['tarikh'][0]),natije = str(ed.loc[index:index]['natije'][0]) , newRisk = str(ed.loc[index:index]['newRisk'][0]),tarif = str(ed.loc[index:index]['tarif'][0]) , dec = str(ed.loc[index:index]['dec'][0]))
            

            
            
            


        return redirect('ViewCorrectiveActionDashboard')
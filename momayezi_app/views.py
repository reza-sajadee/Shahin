from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse
from organization_app.models import Vahed
from standardTable_app.models import RequirementStandards
from standardTable_app.models import Standard
from .forms import CreateFormReportMomayezi ,CreateFormTypeMomayezi ,CreateFormForsatBehbod , CreateFormNoghatGhovat ,CreateFormAdamEntebagh ,CreateFormCalenderMomayezi , CreateFormRoleMomayezi , CreateFormMomayeziTeam , CreateFormMomayeziActivityManager , CreateFormCheckListMomayezi  , CreateMomayeziTeamRequest , CreateFormQuestionMomayeziList
from .models import TypeMomayezi ,ReportMomayezi , ForsatBehbod ,NoghatGhovat ,AdamEntebagh , CalenderMomayezi , RoleMomayezi , MomayeziTeam , MomayeziActivityManager , CheckListMomayezi ,MomayeziTeamRequest,QuestionMomayeziList 
from profile_app.decorators import  staff_only
from profile_app.models import Profile
from .decorators import  user_is_modir
from django.views.generic import ListView
import json
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from jalali_date import datetime2jalali, date2jalali
from .utils import convert_day_name
from datetime import timedelta
from risk_app.utils import is_dabir
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from event_app.models import Event
from django.db.models import Avg, F, Window
from django.db.models.functions import  Rank, DenseRank, CumeDist , window
from django.db.models import Count
from django.urls import resolve
from corrective_app.models import CorrectiveAction ,TextDataBase  , CorrectiveActionActivityManager
from organization_app.models import JobBank

def get_json_bands_data(request,system ):
    selected_system = system
    bands = list(RequirementStandards.objects.filter(standard=selected_system).values())
    return JsonResponse({'data': bands})


#تایپ


class TypeMomayeziHome( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    template_name = "TypeMomayezi.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)



class CreateViewTypeMomayezi( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'baseEmployee.html'
   
    menu_link = 'ViewCalenderMomayezi'
    menuBack ="ViewMomayeziDashboard"
    def get(self, request, *args, **kwargs):
        form = CreateFormTypeMomayezi()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت نوبت  ممیزی  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormTypeMomayezi(request.POST,request.FILES)
        profileSender  = Profile.objects.all().filter(user=self.request.user)[0]
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            instance = form.save()
            instanceActivity  = MomayeziActivityManager.objects.create(typeMomayeziRelated = instance , sender=profileSender, reciver=instance.modir ,status='doing' ,activity='team'   )    
            instanceActivitycl  = MomayeziActivityManager.objects.create(typeMomayeziRelated = instance , sender=profileSender, reciver=instance.modir ,status='doing' ,activity='calender' , previousActivity = instanceActivity  )    
            instanceActivity.nextActivity = instanceActivitycl
            instanceActivity.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='نوع ممیزی  جدید با موفقیت ساخته شد !!!')
            return redirect('ViewMomayeziDashboard')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='نوع ممیزی  مورد نظر ساخته نشد !')
        context = {'extend':self.extend , 'menuBack':self.menuBack,'form': form }
        return render(request,self.template_name,context)


class ListViewTypeMomayezi(ListView):
  

    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست نوبت ممیزی  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوبت ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['نوبت ممیزی' , 'کد نوبت ممیزی' , 'مسئول بهبود']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = TypeMomayezi.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.typeMomayeziCode)
            data.append(query.modir.lastName)
   
            
 

         
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = { 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return context

    model = TypeMomayezi
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewTypeMomayezi( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(TypeMomayezi,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormTypeMomayezi(instance=obj)
            
            obj = get_object_or_404(TypeMomayezi,id = id)
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
            'color':color , 'columns':columns ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}


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



class DeleteViewTypeMomayezi( LoginRequiredMixin,View):
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
            obj = get_object_or_404(TypeMomayezi,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک نوبت ممیزی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که نوبت ممیزی   " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
            
        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='نوبت ممیزی  با موفقیت پاک شد !!!')
            context ={'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
            return redirect('MomayeziListViewTypeMomayezi')
        return render(request,self.template_name,context)
    
    



class ReportMomayeziHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "ReportMomayezi.html"
    extend = 'base.html'
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)



class CreateViewReportMomayezi( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'base.html'
    def get(self, request, *args, **kwargs):
        form = CreateFormReportMomayezi()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک گزارش ممیزی  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک گزارش ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex = {'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormReportMomayezi(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='گزارش ممیزی  جدید با موفقیت ساخته شد !!!')
            return redirect('MomayeziListViewReportMomayezi')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='گزارش ممیزی  مورد نظر ساخته نشد !')
        context = {'form': form ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return render(request,self.template_name,context)


class ListViewReportMomayezi(ListView):
  
    extend = 'base.html'
    menuBack = 'ViewMomayeziDashboard'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست گزارش ممیزی  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام گزارش ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['کد گزارش ممیزی','واحد','نوبت ممیزی','استاندارد','تاریخ ممیزی','تیم ممیزی']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = ReportMomayezi.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
          
            
            data.append(query.id)
           
      

            

            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = { 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return context

    model = ReportMomayezi
    ordering = '-created_at' 
    template_name ='list.html'

class ListViewReportType(ListView):
  

    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'

    
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست گزارش های نوبت ممیزی"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوبت ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['ردیف', 'نوع ممیزی', ]
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = TypeMomayezi.objects.all()
        list_data = []
        external_link = 'ListViewVahedReportMomayezi'

        counter = 1
        for query in queryset:
            data = []
            dict_temp = {}
        
            data.append(counter)
            
           
            data.append(query.title)
          
            
            

            counter += 1



        
            
        
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        
            
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data , 'external_link':external_link }
        return context

    model = TypeMomayezi
    ordering = '-created_at' 
    template_name ='listView.html'


class UpdateViewReportMomayezi( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(ReportMomayezi,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormReportMomayezi(instance=obj)
            
            obj = get_object_or_404(ReportMomayezi,id = id)
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
            context =  {'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormReportMomayezi(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='گزارش ممیزی  جدید با موفقیت ساخته شد !!!')
                return redirect('MomayeziListViewReportMomayezi')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='گزارش ممیزی  مورد نظر ساخته نشد !')           
            context = {'form': form,'object':obj ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return render(request,self.template_name,context)



class DeleteViewReportMomayezi( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(ReportMomayezi,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک گزارش ممیزی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که گزارش ممیزی   " + obj.reportMomayeziCode + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
            
        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='گزارش ممیزی  با موفقیت پاک شد !!!')
            context={'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
            return redirect('MomayeziListViewReportMomayezi')
        return render(request,self.template_name,context)
    




class ListViewVahedReportMomayezi(ListView):
  
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = ''
    #4
    model = ReportMomayezi
    ordering = '-created_at' 
    template_name ='listMomayeziReport.html'
    def get(self, request,typeId=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست گزارش ممیزی  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام گزارش ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان واحد' ,]
        #اسم داده های جدول
        listVahed = []
        q = request.GET.get('q')
        
        
        #دریافت تمام داده ها
        allReport = ReportMomayezi.objects.all().filter(typeMomayeziRelated__id = typeId)
        list_data = []
        
        if(q == 'vahed'):
            for report in allReport:
                    
                    if(report.activityRelated.calender.vahedMomayezi not in listVahed):
                        listVahed.append(report.vahedRelated)
                        header_table   = ['عنوان واحد' ,]
        if(q == 'ghovat'):
            allReport = allReport.filter(result = 'ghovat')
            header_table   = ['عنوان ' ,'نتیجه ممیزی'  , 'واحد' ,  ]
        elif(q=='adam'):
            allReport = allReport.filter(result = 'adam')
            header_table   = ['عنوان ' ,'نتیجه ممیزی'  , 'واحد' ,  ]
        elif(q=='behbod'):
            allReport = allReport.filter(result = 'behbod')
            header_table   = ['عنوان ' ,'نتیجه ممیزی'  , 'واحد' ,  ]
        #ایجاد لیست داده ها
        if(q == 'vahed'):
            for vahed in listVahed:
                data = []
                dict_temp = {}
                data.append(vahed.title)
                dict_temp = {vahed.id : data}
                list_data.append(dict_temp)
        
        elif(q == 'ghovat'):
            for report in allReport:
                data = []
                dict_temp = {}
                data.append(report.report)
                data.append('نقطه قوت')
                data.append(report.vahedRelated.title)
                dict_temp = {report.id : data}
                list_data.append(dict_temp)
        elif(q=='adam'):
            for report in allReport:
                data = []
                dict_temp = {}
                data.append(report.report)
                data.append('عدم انطباق')
                data.append(report.vahedRelated.title)
                dict_temp = {report.id : data}
                list_data.append(dict_temp)
        elif(q=='behbod'):
            for report in allReport:
                data = []
                dict_temp = {}
                data.append(report.report)
                data.append('فرصت بهبود')
                data.append(report.vahedRelated.title)
                dict_temp = {report.id : data}
                list_data.append(dict_temp)

        
            
        #دیکشنری داده ها
        context = { 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,'q':q,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'typeId':typeId}
        return render(request,self.template_name , context)
   

   


class ViewReportMomayezi( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "ViewReport.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    

    def get(self, request,typeId = None,vahedId=None   ,*args, **kwargs):

        vahedSelected = Vahed.objects.all().filter(id = vahedId)[0]
        allReport = ReportMomayezi.objects.all().filter(typeMomayeziRelated__id = typeId).filter(vahedRelated = vahedId)
        allNoghat  = allReport.filter(result = 'ghovat') 
        allForsat = allReport.filter(result = 'behbod') 
        allAdam = allReport.filter(result = 'adam') 
        calenderSelected = CalenderMomayezi.objects.all().filter(vahedMomayezi__id =vahedId ).filter(teamMomayezi__typeMomayeziRelated__id = typeId)[0]
        
        
       
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
        context =  {'header_title':header_title, 'allNoghat':allNoghat , 'allForsat' :allForsat , 'allAdam' :allAdam ,
        'discribtion':discribtion,'icon_name':icon_name,
        'color':color , 'columns':columns ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self) , 'vahedSelected':vahedSelected , 'calenderSelected':calenderSelected}


        return render(request,self.template_name,context)
    
    


class ForsatBehbodHome( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    template_name = "ForsatBehbod.html"
    extend = 'base.html'
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)



class CreateViewForsatBehbod( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'base.html'
    def get(self, request, *args, **kwargs):
        form = CreateFormForsatBehbod()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک فرصت بهبود  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک فرصت بهبود  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex = {'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormForsatBehbod(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='فرصت بهبود  جدید با موفقیت ساخته شد !!!')
            return redirect('MomayeziListViewForsatBehbod')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='فرصت بهبود  مورد نظر ساخته نشد !')
        context = {'form': form,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return render(request,self.template_name,context)


class ListViewForsatBehbod(ListView):
  

    extend = 'base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست فرصت بهبود  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام فرصت بهبود  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان' , 'گزارش ممیزی']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = ForsatBehbod.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.reportMomayeziCode)
    

            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = { 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return context

    model = ForsatBehbod
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewForsatBehbod( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(ForsatBehbod,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormForsatBehbod(instance=obj)
            
            obj = get_object_or_404(ForsatBehbod,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش فرصت بهبود  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این فرصت بهبود  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormForsatBehbod(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='فرصت بهبود  جدید با موفقیت ساخته شد !!!')
                return redirect('MomayeziListViewForsatBehbod')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='فرصت بهبود  مورد نظر ساخته نشد !')           
            context = {'form': form,'object':obj ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return render(request,self.template_name,context)



class DeleteViewForsatBehbod( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(ForsatBehbod,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک فرصت بهبود "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که فرصت بهبود   " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
            
        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='فرصت بهبود  با موفقیت پاک شد !!!')
            context = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
            return redirect('MomayeziListViewForsatBehbod')
        return render(request,self.template_name,context)
    
    


class NoghatGhovatHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "NoghatGhovat.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)



class CreateViewNoghatGhovat( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'base.html'
    def get(self, request, *args, **kwargs):
        form = CreateFormNoghatGhovat()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک نقطه قوت  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نقطه قوت  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex = {'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormNoghatGhovat(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='نقطه قوت  جدید با موفقیت ساخته شد !!!')
            return redirect('MomayeziListViewNoghatGhovat')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='نقطه قوت  مورد نظر ساخته نشد !')
        context = {'form': form ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return render(request,self.template_name,context)


class ListViewNoghatGhovat(ListView):
  

    extend = 'base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست نقطه قوت  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نقطه قوت  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان' , 'گزارش ممیزی']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = NoghatGhovat.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.reportMomayeziCode)
    

            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = { 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return context

    model = NoghatGhovat
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewNoghatGhovat( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'base.html'
    template_name = "create.html"
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(NoghatGhovat,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormNoghatGhovat(instance=obj)
            
            obj = get_object_or_404(NoghatGhovat,id = id)
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
            'color':color , 'columns':columns ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormNoghatGhovat(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='نقطه قوت  جدید با موفقیت ساخته شد !!!')
                return redirect('MomayeziListViewNoghatGhovat')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='نقطه قوت  مورد نظر ساخته نشد !')           
            context = {'form': form,'object':obj ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return render(request,self.template_name,context)



class DeleteViewNoghatGhovat( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(NoghatGhovat,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک نقطه قوت "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که نقطه قوت   " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
            
        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='نقطه قوت  با موفقیت پاک شد !!!')
            context = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self) ,}
            return redirect('MomayeziListViewNoghatGhovat')
        return render(request,self.template_name,context)
    
    



class AdamEntebaghHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "AdamEntebagh.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)



class CreateViewAdamEntebagh( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'base.html'
    def get(self, request, *args, **kwargs):
        form = CreateFormAdamEntebagh()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک عدم انطباق  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک عدم انطباق  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex = {'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormAdamEntebagh(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='عدم انطباق  جدید با موفقیت ساخته شد !!!')
            return redirect('MomayeziListViewAdamEntebagh')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='عدم انطباق  مورد نظر ساخته نشد !')
        context = {'form': form ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return render(request,self.template_name,context)


class ListViewAdamEntebagh(ListView):
  

    extend = 'base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست عدم انطباق  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام عدم انطباق  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان','کد گزارش','بند استاندارد']
        #اسم داده های جدول







        #دریافت تمام داده ها
        queryset = AdamEntebagh.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.reportMomayeziCode)
            data.append(query.bandStandard)
       
    

            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = { 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return context

    model = AdamEntebagh
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewAdamEntebagh( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(AdamEntebagh,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormAdamEntebagh(instance=obj)
            
            obj = get_object_or_404(AdamEntebagh,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش عدم انطباق  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این عدم انطباق  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormAdamEntebagh(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='عدم انطباق  جدید با موفقیت ساخته شد !!!')
                return redirect('MomayeziListViewAdamEntebagh')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='عدم انطباق  مورد نظر ساخته نشد !')           
            context = {'form': form,'object':obj ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
        return render(request,self.template_name,context)



class DeleteViewAdamEntebagh( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(AdamEntebagh,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک عدم انطباق "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که عدم انطباق   " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self)}
            
        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='عدم انطباق  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('MomayeziListViewAdamEntebagh')
        return render(request,self.template_name,context)
    
    

#تقویم

class CalenderMomayeziHome( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    template_name = "CalenderMomayezi.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)



class CreateViewCalenderMomayezi( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createCalenderMomayezi.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    def get(self, request,typeMomayezi, *args, **kwargs):
        form = CreateFormCalenderMomayezi()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک برنامه ممیزی  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک برنامه ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        typeMomayeziId = typeMomayezi
        typeMomayeziSelected = TypeMomayezi.objects.all().filter(id = typeMomayeziId)
        allSystem = Standard.objects.all()
        allTeam = MomayeziTeam.objects.all().filter(typeMomayeziRelated__id = typeMomayezi)
        allVahed = Vahed.objects.all()
        
        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,'columns' : columns , 'color' : color , 'allSystem':allSystem , 'allTeam' :allTeam , 'allVahed':allVahed}
        return render(request,self.template_name,contex)


    def post(self, request,typeMomayezi, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormCalenderMomayezi(request.POST,request.FILES)
        teamId = form['teamMomayezi'].value()
        teamSelected = MomayeziTeam.objects.all().filter(id = teamId)[0]
        typeSelected = TypeMomayezi.objects.all().filter(id = typeMomayezi)[0]
        sarMomayezSelected =  Profile.objects.all().filter(id = teamSelected.sarMomayez.id)[0]
        profileSender  = Profile.objects.all().filter(user=self.request.user)[0]
        allBandsId = request.POST.getlist('bandMomayezi')
        teamAllMember = teamSelected.memberMomayezi
        profileSelected = TypeMomayezi.objects.get(id = typeMomayezi)
        
        #بررسی صحت اطلاعات ورودی
        
        if form.is_valid():
            instance = form.save()
            instance.typeMomayezi = typeSelected
        
            for band in allBandsId:
                instance.bandMomayezi.add(band)
            instance.save()

            instanceMomayeziActivityManagerSarMomayez = MomayeziActivityManager.objects.create( typeMomayeziRelated = profileSelected,sender=profileSender, reciver=sarMomayezSelected ,status='doing' ,activity='cheakListQuestion' , calender = instance )    
            
            instanceMomayeziActivityManagerSarMomayez.save()
            Event.objects.create(  title ='ممیزی واحد ' + instance.vahedMomayezi.title + ' ' + 'در ساعت ' + str(instance.timeStart) ,end = (instance.dateMomayezi) , start =(instance.dateMomayezi)  ,allUser = True , color='red' )
            #instanceMomayeziActivityManagerSarMomayez = MomayeziActivityManager.objects.create( typeMomayeziRelated = profileSelected ,sender=profileSender, reciver=sarMomayezSelected ,status='doing' ,activity='report' , calender = instance )    
            #instanceMomayeziActivityManagerSarMomayez.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='برنامه ممیزی  جدید با موفقیت ساخته شد !!!')
            return redirect('ViewCalenderMomayezi' ,typeMomayezi )
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='برنامه ممیزی  مورد نظر ساخته نشد !')
        context = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)
    

class ComplateViewCalenderMomayezi( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createCalenderMomayezi.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    def get(self, request,typeMomayezi, *args, **kwargs):
        
      
        typeMomayeziSelected = TypeMomayezi.objects.get(id = typeMomayezi)
        activitySelected = MomayeziActivityManager.objects.get(typeMomayeziRelated = typeMomayeziSelected ,activity = 'calender' )
        activitySelected.status = 'done'
        activitySelected.save()
        sweetify.toast(self.request,timer=30000 , icon="success",title ='ثبت برنامه زمانی به اتمام رسید        !!!')
        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        return redirect('ViewMomayeziDashboardMember' ,typeMomayezi )


   



class CreateViewCalenderMomayeziListType(ListView):
  

    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'

    
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "    لیست ممیزی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوبت ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['ردیف', 'نوع ممیزی', 'مدیر']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = TypeMomayezi.objects.all()
        list_data = []
        
        counter = 1
        for query in queryset:
            data = []
            dict_temp = {}
        
            data.append(counter)
            
           
            data.append(query.title)
            data.append(query.modir)
            
            

            counter += 1



        
            
        
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        
            
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data ,  }
        return context

    model = TypeMomayezi
    ordering = '-created_at' 
    template_name ='CreateViewCalenderMomayeziListType.html'




class ListViewCalenderMomayezi(ListView):
  

    extend = 'base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست نوبت ممیزی  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوبت ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['زمان ممیزی' , 'واحد' , 'ساعت' , 'تیم' ,'سیستم' , 'بند', 'نوع ممیزی']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = CalenderMomayezi.objects.all()
        list_data = []
        
        profileUser = Profile.objects.all().filter(user=self.request.user)[0]
        
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            
            data.append(datetime2jalali(query.dateMomayezi).strftime('14%y/%m/%d'))
            data.append(query.vahedMomayezi)
            data.append(query.timeDuration)
            data.append(query.teamMomayezi)
            data.append(query.systemMomayezi)
            data.append(query.bandMomayezi)
            data.append(query.typeMomayezi)
   
            
 


         
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = CalenderMomayezi
    ordering = '-created_at' 
    template_name ='list.html'



class ListViewCalenderMomayeziType(ListView):
  

    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'

    
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست نوبت ممیزی  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوبت ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['ردیف', 'نوع ممیزی', 'مدیر']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = TypeMomayezi.objects.all()
        list_data = []
        external_link = 'ViewCalenderMomayezi'

        counter = 1
        for query in queryset:
            data = []
            dict_temp = {}
        
            data.append(counter)
            
           
            data.append(query.title)
            data.append(query.modir)
            
            

            counter += 1



        
            
        
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        
            
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data , 'external_link':external_link }
        return context

    model = TypeMomayezi
    ordering = '-created_at' 
    template_name ='listView.html'



class ViewCalenderMomayezi(ListView):
  

    extend = 'baseEmployee.html'
    menuBack = 'ViewMomayeziDashboard'
    menu_link = 'ViewMomayeziDashboard'
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "listCalenderMomayezi.html"
    

    @staff_only 
    def get(self, request,typeMomayezi, *args, **kwargs):
        
        
        
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک انتخاب ریسک شناسایی شده  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک انتخاب ریسک شناسایی شده  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        header_table   = ['زمان ممیزی' , 'واحد' , 'ساعت' ,'ساعت پایان', 'تیم' ,'سیستم' , 'بند', 'نوع ممیزی']
        #اسم داده های جدول
        typeMomayeziSelected = TypeMomayezi.objects.all().filter(id = typeMomayezi )[0]
     
        #دریافت تمام داده ها
        queryset = CalenderMomayezi.objects.all().filter(teamMomayezi__typeMomayeziRelated__id=typeMomayezi)
        list_data = []
        profileUser = Profile.objects.all().filter(user=self.request.user)[0]
        modir = False
        if(typeMomayeziSelected.modir ==profileUser or profileUser.user.is_superuser):
            modir = True
        if(len(queryset)>0):
            
            yearMomayeziSelected = datetime2jalali(queryset[0].dateMomayezi).strftime('%Y')
            
            #ایجاد لیست داده ها
            counter = 1
            for query in queryset:
                data = []
                dict_temp = {}
            
                data.append(counter)
                data.append(datetime2jalali(query.dateMomayezi).strftime('14%y/%m/%d'))
                data.append((query.dateMomayezi.strftime('%a')))
                data.append(query.timeStart.strftime('%H:%M'))
                data.append(query.vahedMomayezi.title)
                
                if(str(query.timeDuration.strftime('%H')) != '00'):
                    data.append(query.timeDuration.strftime('%H'))
                else:
                    data.append(0)
                if(str(query.timeDuration.strftime('%M')) != '00'):
                    data.append(query.timeDuration.strftime('%M'))
                else:
                    data.append(0)
                
                teams = []
                for member in query.teamMomayezi.memberMomayezi.all():
                    teams.append( (member.firstName + ' ' + member.lastName) )
                data.append(teams)
                                
                
                
                system = []
               
                data.append(query.systemMomayezi.standardNumber+ '  ' + query.systemMomayezi.standardTitlePersian  )
                bands = []
                for band in query.bandMomayezi.all():
                    if(band.clauseNumber != None):
                        if(band.title != None):
                            bands.append(( band.clauseNumber + '  ' + band.title))
                        else:
                            bands.append(( band.clauseNumber))
                    else:
                        bands.append('عنوان ندارد' )
                data.append(bands[:-1])
                
                
    
                counter += 1
    


            
                
            
                dict_temp = {query.id : data}
                list_data.append(dict_temp)
        else:
            
            yearMomayeziSelected = 'یافت نشد'
            
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack ,'modir':modir, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data , 'typeMomayeziSelected':typeMomayeziSelected.title , 'yearMomayeziSelected':yearMomayeziSelected , 'typeMomayezi' : typeMomayezi }
        
        return render(request,self.template_name,context)

   



class UpdateViewCalenderMomayezi( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    template_name = "createCalenderMomayezi.html"
    extend = 'base.html'
    menu_link = 'ViewCalenderMomayezi'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(CalenderMomayezi,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormCalenderMomayezi(instance=obj)
            
            obj = get_object_or_404(CalenderMomayezi,id = id)
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
            context =  {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
       
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormCalenderMomayezi(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='نوبت ممیزی  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewCalenderMomayezi')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='نوبت ممیزی  مورد نظر ساخته نشد !')           
            context = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewCalenderMomayezi( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(CalenderMomayezi,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک نوبت ممیزی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که نوبت ممیزی   " + str(obj.dateMomayezi) + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):
        
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='نوبت ممیزی  با موفقیت پاک شد !!!')
            context={'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
            return redirect('ListViewCalenderMomayezi')
        return render(request,self.template_name,context)
    

#نقش

class CreateViewRoleMomayezi( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'base.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormRoleMomayezi()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک نقش ممیزی  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نقش ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


   
    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormRoleMomayezi(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='نقش ممیزی  جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewRoleMomayezi')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='نقش ممیزی  مورد نظر ساخته نشد !')
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewRoleMomayezi(ListView):
    extend = 'base.html'

   
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست نقش ممیزی  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نقش ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
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
        queryset = RoleMomayezi.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
         
            data.append(query.title)
           
   
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = RoleMomayezi
    ordering = '-created_at' 
    template_name ='list.html'



class ViewRoleMomayezi( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detail.html"
    extend = 'base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RoleMomayezi,id = id)
        return obj
     
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = RoleMomayezi.objects.all().filter(id=id)[0]
           
            obj = get_object_or_404(RoleMomayezi,id = id)
            
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "اطلاعات نقش ممیزی   "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "چزییات نقش ممیزی را در این صفحه می توانید مشاهده کنید"
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
            
                
            context =  {'extend' : self.extend , 'object':obj , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,
                'color':color , 'columns':columns,'list_data':list_data,
                'header_table':header_table , 'form':form , }


        return render(request,self.template_name,context)
 

class UpdateViewRoleMomayezi( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
   
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RoleMomayezi,id = id)
        return obj
   
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRoleMomayezi(instance=obj)
            
            obj = get_object_or_404(RoleMomayezi,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش نقش ممیزی  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این نقش ممیزی  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend , 'menuBack':self.menuBack  , 'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
   
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRoleMomayezi(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='نقش ممیزی  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewRoleMomayezi')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='نقش ممیزی  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewRoleMomayezi( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    extend ='base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RoleMomayezi,id = id)
        return obj
   
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک نقش ممیزی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که نقش ممیزی   " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend' :self.extend , 'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
   
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='نقش ممیزی  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ListViewRoleMomayezi')
        return render(request,self.template_name,context)
    
 
 
 #تیم

class MomayeziTeamHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "MomayeziTeam.html"
    @staff_only 
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)



class CreateViewMomayeziTeam( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    @staff_only 
    def get(self, request , typeId, *args, **kwargs):
        form = CreateFormMomayeziTeam(initial={'typeMomayeziRelated' : typeId})
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک تیم ممیزی  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک تیم ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    @staff_only
    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormMomayeziTeam(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        profileSender = Profile.objects.all().filter(user=self.request.user)[0]
        profileReciver = Profile.objects.all().filter(id=form['sarMomayez'].value())[0]


        if form.is_valid():
            f = form.save()
            #teamId = f.pk
            #teamSelected = MomayeziTeam.objects.all().filter(id = teamId)[0]
            #instanceMomayeziActivityManager = MomayeziActivityManager.objects.create(sender=profileSender, reciver=profileReciver ,status='doing' ,activity='cheakListQuestion' , )
            #instanceMomayeziActivityManager.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='تیم ممیزی  جدید با موفقیت ساخته شد !!!')
           
            return redirect(reverse('ListViewMomayeziTeam')+"?typeId=" +str(f.typeMomayeziRelated.id) )
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='تیم ممیزی  مورد نظر ساخته نشد !')
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewMomayeziTeam(ListView):
  
    extend='baseEmployee.html'
    menu_link = 'ViewCalenderMomayezi'
    menuBack =  'ViewMomayeziDashboard'
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست تیم ممیزی  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام تیم ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان' ,'اعضا ',' عنوان استاندارد','شماره استاندارد' ,'نوبت ممیزی']
        #اسم داده های جدول
        finish = ''
        #دریافت تمام داده ها
        if(self.request.GET.get('typeId') != None):
            queryset = MomayeziTeam.objects.all().filter(typeMomayeziRelated = self.request.GET.get('typeId'))
            finish = self.request.GET.get('typeId')
            
        else:
            queryset = MomayeziTeam.objects.all()
            
        
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            memberList = ''
            data.append(query.title)
            allMember = ''
            for member in query.memberMomayezi.all():
                allMember+= member.lastName
                allMember += ' - '
            data.append(allMember[:-1])
            data.append(query.standardRelated.standardTitlePersian)
            data.append(query.standardRelated.standardNumber)
            data.append(query.typeMomayeziRelated.title)
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data , 'finish':finish}
        return context

    model = MomayeziTeam
    ordering = '-created_at' 
    template_name ='listTeam.html'



class ListViewMomayeziTeamComplate( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createCalenderMomayezi.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    def get(self, request,typeMomayezi, *args, **kwargs):
        
      
        typeMomayeziSelected = TypeMomayezi.objects.get(id = typeMomayezi)
        activitySelected = MomayeziActivityManager.objects.get(typeMomayeziRelated = typeMomayeziSelected ,activity = 'team' )
        activitySelected.status = 'done'
        activitySelected.save()
        sweetify.toast(self.request,timer=30000 , icon="success",title ='  تعریف تیم های ممیزی به اتمام رسید        !!!')
        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        return redirect('ViewMomayeziDashboardMember' ,typeMomayezi )


   



class ViewMomayeziTeam( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detail.html"
    extend='baseEmployee.html'
    menu_link = 'ViewCalenderMomayezi'
    menuBack ="ViewMomayeziDashboard"
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MomayeziTeam,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = MomayeziTeam.objects.all().filter(id=id)[0]
           
            obj = get_object_or_404(MomayeziTeam,id = id)
            
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "اطلاعات تیم ممیزی   "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "چزییات تیم ممیزی را در این صفحه می توانید مشاهده کنید"
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
            
                
            context =  {'extend':self.extend , 'menuBack':self.menuBack  , 'object':obj , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,
                'color':color , 'columns':columns,'list_data':list_data,
                'header_table':header_table , 'form':form , }


        return render(request,self.template_name,context)
 

class UpdateViewMomayeziTeam( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend='baseEmployee.html'
    menu_link = 'ViewCalenderMomayezi'
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MomayeziTeam,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormMomayeziTeam(instance=obj)
            
            obj = get_object_or_404(MomayeziTeam,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش تیم ممیزی  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این تیم ممیزی  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend , 'menuBack':self.menuBack  , 'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormMomayeziTeam(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='تیم ممیزی  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewMomayeziTeam')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='تیم ممیزی  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewMomayeziTeam( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    extend ='baseEmployee.html'
    
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MomayeziTeam,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک تیم ممیزی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که تیم ممیزی   " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend' :self.extend,'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':'base.html','riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='تیم ممیزی  با موفقیت پاک شد !!!')
            
            return redirect('ListViewMomayeziTeam')
        return render(request,self.template_name,context)
    

#عضویت

class RegisterViewMomayeziTeamRequest( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "registermomayezi.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    @staff_only 
    def get(self, request, *args, **kwargs):
        form = CreateFormMomayeziTeam()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک تیم ممیزی  جدید "
        profile = Profile.objects.filter(user=self.request.user)[0]
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک تیم ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #دیکشنری داده ها
        contex= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'profile' : profile}
        return render(request,self.template_name,contex)


    @staff_only
    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateMomayeziTeamRequest(request.POST,request.FILES)
        
        ProfileSelected = Profile.objects.filter( user=self.request.user)[0]
        try:
             
            #form.memberMomayezi = ProfileSelected
            sabegheYear = request.POST.get('sabegheYear')
            document = request.FILES['document']
        
            instance = MomayeziTeamRequest.objects.create(memberMomayezi =ProfileSelected  , sabegheYear = sabegheYear,document =document  ,status ='not'  ,)
            instance.save()
            sweetify.toast(self.request,timer=30000 , icon="success",title ='درخواست عضویت در تیم ممیزی با موفقیت ثبت شد .')
            return redirect('ViewMomayezi')
        except:
            sweetify.toast(self.request,timer=30000 , icon="error",title ='درخواست عضویت در تیم ممیزی   ثبت نشد .')
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)

        
#فعالیت

class MomayeziActivityManagerHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "MomayeziActivityManager.html"
    @staff_only 
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)



class CreateViewMomayeziActivityManager( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'base.html'
    @staff_only 
    def get(self, request, *args, **kwargs):
        form = CreateFormMomayeziActivityManager()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک فعالیت ممیزی  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک فعالیت ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    @staff_only
    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormMomayeziActivityManager(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='فعالیت ممیزی  جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewMomayeziActivityManager')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='فعالیت ممیزی  مورد نظر ساخته نشد !')
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewMomayeziActivityManager(ListView):
  
    extend = 'base.html'
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست فعالیت ممیزی  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام فعالیت ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['فرستنده' , 'گیرنده' , 'وضعیت', 'فعالیت', 'تیم']
        #اسم داده های جدول


        #دریافت تمام داده ها
        queryset = MomayeziActivityManager.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            teamList = ''
            data.append(query.sender)
            data.append(query.reciver)
            data.append(query.status)
            data.append(query.activity)
            data.append(query.team)
           
   
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = MomayeziActivityManager
    ordering = '-created_at' 
    template_name ='list.html'



class ViewMomayeziActivityManager( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detail.html"
    extend = 'base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MomayeziActivityManager,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = MomayeziActivityManager.objects.all().filter(id=id)[0]
           
            obj = get_object_or_404(MomayeziActivityManager,id = id)
            
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "اطلاعات فعالیت ممیزی   "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "چزییات فعالیت ممیزی را در این صفحه می توانید مشاهده کنید"
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
            
            list_data = {'فرستنده' : obj.sender  ,'گیرنده' : obj.reciver ,'وضعیت' : obj.status ,'نوع فعالیت' : obj.activity ,'تیم' : obj.team , 'فعالیت قبلی' :obj.previousActivity , 'فعالیت بعدی' :obj.nextActivity  , 'تاریخ ایجاد' :datetime2jalali(obj.created_at).strftime('14%y/%m/%d') , 'آخرین به روز رسانی' :datetime2jalali(obj.updated_at).strftime('14%y/%m/%d') }
            #ایجاد لیست داده ها
           
            #جدول لیست کلاس ها
            # عنوان های جدول
            
                
            context =  {'extend':self.extend , 'menuBack':self.menuBack  , 'object':obj , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,
                'color':color , 'columns':columns,'list_data':list_data,
                'header_table':header_table , 'form':form , }


        return render(request,self.template_name,context)
 

class UpdateViewMomayeziActivityManager( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MomayeziActivityManager,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormMomayeziActivityManager(instance=obj)
            
            obj = get_object_or_404(MomayeziActivityManager,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش فعالیت ممیزی  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این فعالیت ممیزی  ، موارد جدید را وارد کنید"
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
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormMomayeziActivityManager(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='فعالیت ممیزی  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewMomayeziActivityManager')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='فعالیت ممیزی  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewMomayeziActivityManager( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    extend ='base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MomayeziActivityManager,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک فعالیت ممیزی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که فعالیت ممیزی   " + obj.sender.lastName + " "  + " را پاک کنید   ؟"
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
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='فعالیت ممیزی  با موفقیت پاک شد !!!')
            
            return redirect('ListViewMomayeziActivityManager')
        return render(request,self.template_name,context)
    

#چکلیست

class CheckListMomayeziHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "CheckListMomayezi.html"
    @staff_only 
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)



class ViewCheckListMomayeziList( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "ViewCheckListMomayeziList.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    @staff_only 
    def get(self, request,calenderId=None ,*args, **kwargs):
        form = CreateFormCheckListMomayezi()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک چک لیست ممیزی جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک چک لیست ممیزی جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        calenderSelected = CalenderMomayezi.objects.get(id = calenderId)
        profileSelected = calenderSelected.teamMomayezi.typeMomayeziRelated

        allCheckList = CheckListMomayezi.objects.all().filter(Q(activity__activity = "cheakList") & Q(typeMomayeziRelated = profileSelected))
        
        
        #allCheckList = CheckListMomayezi.objects.all().filter(activity = calenderSelected.activity.nextActivity)
        clusesCode = []
        clusesFull = []
        for checkList in allCheckList:
            tempCode = []
            tempFull = []
            for cluse in checkList.question.requirementStandardQuestion.all():
                x= cluse.clauseNumber
                y= cluse.title
                if(cluse.clauseNumber):
                    tempFull.append(cluse.clauseNumber + ' ' + cluse.title )
                    tempCode.append(cluse.clauseNumber )
            clusesCode.append(tempCode)
            clusesFull.append(tempFull)

      
        zipCheckList = zip(clusesCode ,clusesFull  ,allCheckList )
        
        #دیکشنری داده ها
        contex= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'calenderSelected':calenderSelected   , 'zipCheckList' : zipCheckList}
        return render(request,self.template_name,contex)


    @staff_only
    def post(self, request,calenderId=None , *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormCheckListMomayezi(request.POST,request.FILES)
        calenderSelected = CalenderMomayezi.objects.get(id = calenderId)
        
        teamSelected = MomayeziTeam.objects.get(id = calenderSelected.teamMomayezi.id)
        profileSelected = teamSelected.typeMomayeziRelated
        profileSender  = Profile.objects.all().filter(user=self.request.user)[0]
        sarMomayezSelected =teamSelected.sarMomayez
        activitySelected = MomayeziActivityManager.objects.get(calender = calenderId)
        activitySelected.status = 'done'
        activitySelected.save()
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            instanceMomayeziActivityManager = MomayeziActivityManager.objects.create( typeMomayeziRelated = profileSelected,sender=profileSender, reciver=sarMomayezSelected ,status='doing' ,activity='report'   ,calender = calenderSelected)
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='چک لیست ممیزی جدید با موفقیت ساخته شد !!!')
            return HttpResponseRedirect(reverse('ViewCheckListMomayeziList' , kwargs={'calenderId':calenderId}) )
        
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='چک لیست ممیزی مورد نظر ساخته نشد !')
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewCheckListMomayezi(ListView):
  
    extend = 'base.html'
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست چک لیست ممیزی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام چک لیست ممیزی ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['موضوع' , 'فعالیت' , 'مشاهدات' , 'نتیجه']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = CheckListMomayezi.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
         
            data.append(query.title)
            data.append(query.activity)
            data.append(query.observed)
            data.append(query.result)
           
   
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = CheckListMomayezi
    ordering = '-created_at' 
    template_name ='list.html'



class ListViewCheckListMomayeziSelecting(ListView):
  
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست چک لیست ممیزی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام چک لیست ممیزی ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['تیم' , 'نام واحد تحت ممیزی' , 'واحد سازمانی مافوق' , ]
       
        
        #اسم داده های جدول
        profileSelected = TypeMomayezi.objects.get(id = self.kwargs['profileId'])
        
        profile = Profile.objects.filter(user=self.request.user)[0]
        
        allActivity = MomayeziActivityManager.objects.all().filter(Q(status = 'doing') & Q(activity= 'cheakListQuestion') & Q(typeMomayeziRelated = profileSelected))
        list_data = []
        counter = 1
        for activity in allActivity:
            x = activity.calender
            data = []
            dict_temp = {}
            data.append(activity.calender.teamMomayezi)
            data.append(activity.calender.vahedMomayezi.title)
            data.append(activity.calender.vahedMomayezi.vahedMafogh.title)
            
            dict_temp = {activity.id : data}
            list_data.append(dict_temp)
        
        
        doneActivity = MomayeziActivityManager.objects.all().filter(status = 'done').filter(activity= 'cheakListQuestion')
        list_data_done = []
        counter = 1
        for activity in doneActivity:
            
            data = []
            dict_temp = {}
            data.append(activity.calender.teamMomayezi.title)
            data.append(activity.calender.vahedMomayezi.title)
            data.append(activity.calender.vahedMomayezi.vahedMafogh.title)
            
            dict_temp = {activity.id : data}
           
            list_data_done.append(dict_temp)
        
        
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data , 'list_data_done' : list_data_done }
        return context

    model = CheckListMomayezi
    ordering = '-created_at' 
    template_name ='listCalenderCheckList.html'

class ListViewCheckListMomayeziEntering(ListView):
  
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست چک لیست ممیزی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام چک لیست ممیزی ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['تیم' , 'نام واحد تحت ممیزی' , 'واحد سازمانی مافوق' , ]
        #اسم داده های جدول
        profile = Profile.objects.filter(user=self.request.user)[0]
        #2
        allActivity = MomayeziActivityManager.objects.all().filter(status = 'doing').filter(activity= 'cheakList')
        print('allActivity' , allActivity)
        list_data = []
        counter = 1
        vaheds = []
        for activity in allActivity:
            if(activity.reciver == profile or profile.user.is_superuser):
                data = []
                dict_temp = {}
                if(activity.calender.vahedMomayezi.title in vaheds):
                    continue
                vaheds.append((activity.calender.vahedMomayezi.title))
                data.append(activity.calender.teamMomayezi.title)
                data.append(activity.calender.vahedMomayezi.title)
                data.append(activity.calender.vahedMomayezi.vahedMafogh.title)
                
                dict_temp = {activity.calender.id : data}
                list_data.append(dict_temp)
        
        
        doneActivity = MomayeziActivityManager.objects.all().filter(status = 'done').filter(activity= 'cheakList').filter(reciver = profile)
        list_data_done = []
        counter = 1
        for activity in doneActivity:
            
            data = []
            dict_temp = {}
            data.append(activity.calender.teamMomayezi.title)
            data.append(activity.calender.vahedMomayezi.title)
            data.append(activity.calender.vahedMomayezi.vahedMafogh.title)
            
            dict_temp = {activity.id : data}
           
            list_data_done.append(dict_temp)
        
        
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data , 'list_data_done' : list_data_done }
        return context

    model = CheckListMomayezi
    ordering = '-created_at' 
    template_name ='listEnteringCheckList.html'


class CreateViewCheckListQuestion( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "CreateViewCheackListQuestion.html"
    
    extend ='baseEmployee.html'
    menu_link = 'ViewCalenderMomayezi'
    menuBack ="ViewMomayeziDashboard"
    @staff_only 
    def get(self, request,activityId, *args, **kwargs):
        
        
        
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "  انتخاب ریسک شناسایی شده  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک انتخاب ریسک شناسایی شده  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        header_table   = [   'عنوان سوال' , 'شماره استاندارد' , 'بند ها'  ]
        #اسم داده های جدول

        #دریافت تمام داده ها
        activitySelected = MomayeziActivityManager.objects.all().filter(id = activityId )[0]
        
        vahedSelected = activitySelected.calender.vahedMomayezi
        
        allquestion = QuestionMomayeziList.objects.all().filter(vahedQuestion = vahedSelected).filter(requirementStandardQuestion__in = activitySelected.calender.bandMomayezi.all())
        teamSelected = activitySelected.calender.teamMomayezi
        profileSelected = activitySelected.typeMomayeziRelated
        
        if(len(allquestion) ==0):
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='سوالی برای انتخاب وجود ندارد          !!!')
            return redirect('ListViewCheckListMomayeziSelecting' , profileId = profileSelected.id)
        
        #ایجاد لیست داده ها
        list_data = []
        for query in allquestion:
            data = []
            dict_temp = {}
            
            data.append(query.question)
            data.append(query.standardQuestion.standardNumber)
            allrs = ''
            for rs in query.requirementStandardQuestion.all():
                if(rs.clauseNumber != None):
                    allrs += rs.clauseNumber + '- ' + rs.title + ','
                else:
                    allrs +=  rs.title + ','

            data.append(allrs[:-1])
           




           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)

        
        #دیکشنری داده ها
        
        contex= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'header_table':header_table ,
        'list_data':list_data,  'vahedSelected' : vahedSelected }
        
       # return HttpResponseRedirect(reverse('ListViewCheckListMomayeziSelecting' ,profileId = profileSelected.id  ))
        return render(request,self.template_name,contex)
    @staff_only
    def post(self, request,activityId ,  *args, **kwargs):
        #فرم دریافت شده
        activitySelected = MomayeziActivityManager.objects.all().filter(id = activityId )[0]
        profileSelected = activitySelected.typeMomayeziRelated
        vahedSelected = activitySelected.calender.vahedMomayezi
        
        sarMomayezSelected = activitySelected.calender.teamMomayezi.sarMomayez

        post_data = request.POST.copy() # to make it mutable
        questions = request.POST.getlist('question')
        profileSender  = Profile.objects.all().filter(user=self.request.user)[0]
        
        questions = QuestionMomayeziList.objects.all().filter(id__in = questions)
        calender = activitySelected.calender
 
        
          
            
        for qs in questions:
            instanceMomayeziActivityManager = MomayeziActivityManager.objects.create( typeMomayeziRelated = profileSelected,sender=profileSender, reciver=sarMomayezSelected ,status='doing' ,activity='cheakList'  ,previousActivity = activitySelected ,calender = calender)
            instanceCheackList = CheckListMomayezi.objects.create(typeMomayeziRelated =profileSelected , title = qs.question ,activity= instanceMomayeziActivityManager ,question = qs   )
            instanceCheackList.save()
            
        del(instanceMomayeziActivityManager)
        activitySelected.status='done'
        activitySelected.save()
        sweetify.toast(self.request,timer=30000 , icon="success",title ='انتخاب ریسک شناسایی شده  جدید با موفقیت ساخته شد !!!')
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        return redirect('ListViewCheckListMomayeziSelecting' ,profileId = profileSelected.id  )
           
        

       
        #     #تابع نمایش پیغام
        
        
  



class ViewCheckListMomayezi( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detail.html"
    extend = 'base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(CheckListMomayezi,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CheckListMomayezi.objects.all().filter(id=id)[0]
           
            obj = get_object_or_404(CheckListMomayezi,id = id)
            
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "اطلاعات چک لیست ممیزی  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "چزییات چک لیست ممیزیرا در این صفحه می توانید مشاهده کنید"
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
            
            list_data = {'عنوان' : obj.title ,'فعالیت' : obj.activity ,'مشاهدات' : obj.observed ,'نتیجه' : obj.result}
            #ایجاد لیست داده ها
           
            #جدول لیست کلاس ها
            # عنوان های جدول
            
                
            context =  {'extend':self.extend , 'menuBack':self.menuBack  , 'object':obj , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,
                'color':color , 'columns':columns,'list_data':list_data,
                'header_table':header_table , 'form':form , }


        return render(request,self.template_name,context)
 

class UpdateViewCheckListMomayezi( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "updateCheckListMomayezi.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(CheckListMomayezi,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        checkListSelected = CheckListMomayezi.objects.get(id = id)
        standardSelected = checkListSelected.activity.calender.systemMomayezi
        allBandMomayezi = checkListSelected.activity.calender.bandMomayezi.all()
        calenderId = checkListSelected.activity.calender.id
        bands = []
        
        for band in checkListSelected.question.requirementStandardQuestion.all() :
            bands.append( band)

      
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormCheckListMomayezi(instance=obj)
            
            obj = get_object_or_404(CheckListMomayezi,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ثبت یافته های ممیزی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این چک لیست ممیزی ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend' :self.extend ,'menuBack':self.menuBack, 'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns , 'standardSelected':standardSelected , 'bands' : bands , 'calenderId' :calenderId}


        return render(request,self.template_name,context)
    
    @staff_only
    @csrf_exempt
    def post( self, request,id=None ,*args, **kwargs):
        checkListSelected = CheckListMomayezi.objects.all().filter(id = id)[0]
        calenderId = checkListSelected.activity.calender.id
        profileSelected = checkListSelected.typeMomayeziRelated
        sarMomayezSelected = checkListSelected.activity.calender.teamMomayezi.sarMomayez
        calenderSelected = CalenderMomayezi.objects.get(id = calenderId)
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        
        if obj is not None:
            form = CreateFormCheckListMomayezi(request.POST or request.FILES,instance=obj )
            title = obj.title 
            observed = request.POST.get('observed') 
            activityId = request.POST.get('activity')
            activity = MomayeziActivityManager.objects.all().filter(id= activityId)[0]
            result   = request.POST.get('result')
            profileSender  = Profile.objects.all().filter(user=self.request.user)[0]
            try:
                if(len(request.FILES)>0):
                    document = request.FILES['document']
                    checkListSelected.document = document


                updated_data = request.POST.copy()
                updated_data.update({'title': title ,'observed':observed ,'activity' : activity , 'result' :result }) 
                form = CreateFormCheckListMomayezi(data=updated_data) 
                
                checkListSelected.result = result
                checkListSelected.observed = observed
                
                checkListSelected.save()
                activity.status = 'done'
                activity.save()
                instanceActivity  = MomayeziActivityManager.objects.create(typeMomayeziRelated = profileSelected , sender=profileSender, reciver=sarMomayezSelected ,status='doing' ,activity='report' ,  calender = calenderSelected )    
                sweetify.toast(self.request,timer=30000 , icon="success",title ='چک لیست ممیزی جدید با موفقیت ساخته شد !!!')
                return HttpResponseRedirect(reverse('ViewCheckListMomayeziList' , kwargs={'calenderId':calenderId}) )
            except:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='چک لیست ممیزی مورد نظر ساخته نشد  !!!')
                return HttpResponseRedirect(reverse('ViewCheckListMomayeziList' , kwargs={'calenderId':calenderId}) )
            # if form.is_valid():
                
                
            #     #form.save(commite=False)
            #     sweetify.toast(self.request,timer=30000 , icon="success",title ='چک لیست ممیزی جدید با موفقیت ساخته شد !!!')
            #     #return redirect('ListViewCheckListMomayezi')
            #     return HttpResponseRedirect(reverse('ViewCheckListMomayeziList' , kwargs={'calenderId':calenderId}) )
            # else:
            #     sweetify.toast(self.request,timer=30000 , icon="error",title ='چک لیست ممیزی مورد نظر ساخته نشد !')           
            #context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form,'object':obj}
        
        
        return render(request,self.template_name,context)



class DeleteViewCheckListMomayezi( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    extend ='base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(CheckListMomayezi,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک چک لیست ممیزی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که چک لیست ممیزی  " + obj.title + " "  + " را پاک کنید   ؟"
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
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='چک لیست ممیزی با موفقیت پاک شد !!!')
            
            return redirect('ListViewCheckListMomayeziSelecting')
        return render(request,self.template_name,context)
    
 
class ChangeViewCheckListMomayeziSelecting( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'



    @staff_only 
    def get(self, request,calenderId=None ,*args, **kwargs):
        
        calenderSelected = get_object_or_404(CalenderMomayezi , id = calenderId)
        activityNext = get_object_or_404(MomayeziActivityManager , id = calenderSelected.activity.nextActivity.id) 
        activityNext.status  = 'done'
        activityNext.save()
        
        calenderSelected.activity.nextActivity.status = 'done'
        
        calenderSelected.save()
        
        
        # calenderSelected.activity.nextActivity.status= 'done'
        # calenderSelected.save()
        #return context
        #return render(request,self.template_name,context)
        return redirect('ListViewCheckListMomayeziSelecting')


class DeleteViewCheckListMomayeziCalender( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    extend ='base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(CheckListMomayezi,id = id)
        return obj
    
    @staff_only 
    def get(self, request ,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک چک لیست ممیزی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که چک لیست ممیزی  " + obj.title + " "  + " را پاک کنید   ؟"
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
    def post( self, request ,id=None ,*args, **kwargs):
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        
        obj = self.get_obj()
        
        if obj is not None:
            prvActivity = obj.activity.previousActivity
            calenderId = CalenderMomayezi.objects.get(activity__id=prvActivity.id)
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='چک لیست ممیزی با موفقیت پاک شد !!!')
            
            return HttpResponseRedirect(reverse('ViewCheckListMomayeziList' , kwargs={'calenderId':calenderId.id}) )
            
        return render(request,self.template_name,context)


#سوالممیزی

class CreateViewQuestionMomayeziList( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "CreateQuestionMomayeziList.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    @staff_only 
    def get(self, request, *args, **kwargs):
        form = CreateFormQuestionMomayeziList(initial={'standardQuestion': 1})
        allSystem = Standard.objects.all()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک سوال ممیزی  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک سوال ممیزی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'allSystem':allSystem}
        return render(request,self.template_name,contex)


    @staff_only
    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormQuestionMomayeziList(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='سوال ممیزی  جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewQuestionMomayeziListVahed')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='سوال ممیزی  مورد نظر ساخته نشد !')
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewQuestionMomayeziList(ListView):
  
    extend = 'base.html'
    menu_link = 'ViewCalenderMomayezi'
    menuBack ="ViewMomayeziDashboard"
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست سوال ممیزی  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام سوال ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['واحد' , 'سوال' , 'استاندارد', 'بند ها', ]
        #اسم داده های جدول






        #دریافت تمام داده ها
        queryset = QuestionMomayeziList.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            teamList = ''
            data.append(query.vahedQuestion)
            data.append(query.question[:50])
            data.append(query.standardQuestion.standardNumber)
            requirementStandardList = ''
            for rs in query.requirementStandardQuestion.all():
                requirementStandardList += rs.clauseNumber + '-' + rs.title + ','
            
            data.append(requirementStandardList[:-1])
  
           
   
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = QuestionMomayeziList
    ordering = '-created_at' 
    template_name ='list.html'

class ListViewQuestionMomayeziListVahed(ListView):
    
    extend ='baseEmployee.html'
    menu_link = 'ViewCalenderMomayezi'
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = " واحد های تحت ممیزی"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام شناسایی ریسک  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['نام واحد تحت ممیزی','واحد سازمانی مافوق', ]
        #اسم داده های جدول
        profile = Profile.objects.filter(user=self.request.user)[0]
        allTeams  = MomayeziTeam.objects.filter(sarMomayez = profile)
        allVaheds = []
        for team in allTeams.all() :
            for vahed in team.vahedMomayezi.all():
                allVaheds.append(vahed)
        
        
      
        #دریافت تمام داده ها
        
      
        list_data = []
       
        #ایجاد لیست داده ها
        for query in allVaheds:
            data = []
            dict_temp = {}
            
            data.append(query.title)
            data.append(query.vahedMafogh.title)
        
            
            
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = QuestionMomayeziList
    ordering = '-created_at' 
    template_name ='ListViewQuestionMomayeziListVahed.html'

class ViewQuestionMomayeziList( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detail.html"
    extend = 'base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(QuestionMomayeziList,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = QuestionMomayeziList.objects.all().filter(id=id)[0]
           
            obj = get_object_or_404(QuestionMomayeziList,id = id)
            
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "اطلاعات سوال ممیزی   "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "چزییات سوال ممیزی را در این صفحه می توانید مشاهده کنید"
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
            
            list_data = {'فرستنده' : obj.sender  ,'گیرنده' : obj.reciver ,'وضعیت' : obj.status ,'نوع فعالیت' : obj.activity ,'تیم' : obj.team , 'فعالیت قبلی' :obj.previousActivity , 'فعالیت بعدی' :obj.nextActivity  , 'تاریخ ایجاد' :datetime2jalali(obj.created_at).strftime('14%y/%m/%d') , 'آخرین به روز رسانی' :datetime2jalali(obj.updated_at).strftime('14%y/%m/%d') }
            #ایجاد لیست داده ها
           
            #جدول لیست کلاس ها
            # عنوان های جدول
            
                
            context =  {'extend':self.extend , 'menuBack':self.menuBack  , 'object':obj , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,
                'color':color , 'columns':columns,'list_data':list_data,
                'header_table':header_table , 'form':form , }


        return render(request,self.template_name,context)
 


class CreateViewQuestionSelecting( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "CreateViewQuestionSelecting.html"
    menu_link = 'ViewCalenderMomayezi'
    extend ='baseEmployee.html'

    @staff_only 
    def get(self, request,vahed, *args, **kwargs):
        
        
        
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک انتخاب ریسک شناسایی شده  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک انتخاب ریسک شناسایی شده  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        header_table   = [  'واحد', 'عنوان سوال' , 'شماره استاندارد' , 'بند ها'  ]
        #اسم داده های جدول

        #دریافت تمام داده ها
        vahedSelected = Vahed.objects.all().filter(id=vahed)[0]
        allquestion = QuestionMomayeziList.objects.all().filter(vahedQuestion = vahed)
        
        
        #allDoneActivity = RiskActivityManager.objects.filter(activity = 'Conclusion').filter(status = 'done').filter(hoze__id = hoze)
        #allRiskIdentificaion = RiskIdentification.objects.filter()
        #queryset = RiskIdentification.objects.all().filter(status = 'identification').filter(hoze = hoze)
        
        if(len(allquestion) ==0):
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='سوالی برای انتخاب وجود ندارد          !!!')
            return redirect('ListViewQuestionMomayeziListVahed')
        #ایجاد لیست داده ها
        list_data_not = []
        for query in allquestion:
            data = []
            dict_temp = {}
            data.append(query.vahedQuestion.title)
            data.append(query.question)
            data.append(query.standardQuestion.standardNumber)
            allrs = ''
            for rs in query.requirementStandardQuestion.all():
                if(rs.clauseNumber != None):
                    allrs += rs.clauseNumber + '-' + rs.title + ','
                else:
                    allrs +=  rs.title + ','

            data.append(allrs[:-1])
           




           
            dict_temp = {query.id : data}
            list_data_not.append(dict_temp)

        list_data_yes = []
        for query in allquestion:
            data = []
            dict_temp = {}
            data.append(query.vahedQuestion.title)
            data.append(query.question)
            data.append(query.standardQuestion.standardNumber)
            allrs = ''
            for rs in query.requirementStandardQuestion.all():
                if(rs.clauseNumber != None):
                    allrs += rs.clauseNumber + '-' + rs.title + ','
                else:
                    allrs +=  rs.title + ','
               

            data.append(allrs[:-1])
           




           
            dict_temp = {query.id : data}
            list_data_yes.append(dict_temp)
        #دیکشنری داده ها
     
        contex= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'header_table':header_table ,
        'list_data_not':list_data_not, 'list_data_yes' : list_data_yes , 'vahedSelected' : vahedSelected }
        return render(request,self.template_name,contex)

  
    @staff_only
    def post(self, request,vahed ,  *args, **kwargs):
        #فرم دریافت شده
        post_data = request.POST.copy() # to make it mutable
        questions = request.POST.getlist('question')
        
        for question in questions:
            qs = QuestionMomayeziList.objects.all().filter(id = question)

            
       

        profileRecomnder = Profile.objects.filter(user=request.user)[0]
        processSelected = Process.objects.filter(id = post_data['process'] )[0] 
        
        groupSelected = Group.objects.filter(id =post_data['group'])[0]
        teamSelected = RiskTeam.objects.filter(hoze =hoze)[0]
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
            print(processSelected.id , 'before instance')
            
            instanceRisk = RiskIdentification.objects.create(
            riskFailureModes=post_data['riskFailureModes'] ,riskCauses=post_data['riskCauses'] ,
            riskEffects=post_data['riskEffects'],team = teamSelected, currentAction=post_data['currentAction'],
            recommender =profileRecomnder ,process =processSelected ,
            group =groupSelected,activity =instanceRiskActivityManager  , hoze = hozeSelected , status = 'measurement'  )
            print(instanceRisk.id , 'after instance')
            instanceRisk.save()
            
            instanceMeasurement = RiskMeasurement.objects.create(riskIdentificated =instanceRisk ,activity = instanceRiskActivityManager   )    
            instanceMeasurement.save()
        
        
        
     
       
        
            
          
        
        for member in teamSelected.memberProfile.all():
            instance = Notifications.objects.create(recivers = member,title='ارزیابی ریسک', description='با عرض سلام خدمت همکار محترم ، شما یک ارزیابی ریسک در حوزه  ' + str(hozeSelected.title) + ' باید انجام دهید .' ,  status = 'primary' ,  icon = 'alarm')
            instance.link = '/risk/measurement/list'
            
            instance.save() 
          
        
        
        
        for riskSelectedId in allRiskIdentificationsSelectedId:
            riskSelected = RiskIdentification.objects.filter(id =riskSelectedId )[0]
            riskSelected.status = 'done'
            riskSelected.activity.status = 'done'
            riskSelected.save()
            
        #     #تابع نمایش پیغام
        sweetify.toast(self.request,timer=30000 , icon="success",title ='انتخاب ریسک شناسایی شده  جدید با موفقیت ساخته شد !!!')
        return HttpResponseRedirect(reverse('CreateViewRiskIdentificationSelecting' , kwargs={'hoze':hoze}) )
  

 



class UpdateViewQuestionMomayeziList( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(QuestionMomayeziList,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormQuestionMomayeziList(instance=obj)
            
            obj = get_object_or_404(QuestionMomayeziList,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش سوال ممیزی  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این سوال ممیزی  ، موارد جدید را وارد کنید"
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
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormQuestionMomayeziList(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='سوال ممیزی  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewQuestionMomayeziList')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='سوال ممیزی  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewQuestionMomayeziList( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    extend ='base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(QuestionMomayeziList,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک سوال ممیزی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که سوال ممیزی   " + obj.question + " "  + " را پاک کنید   ؟"
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
        context= {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='سوال ممیزی  با موفقیت پاک شد !!!')
            
            return redirect('ListViewQuestionMomayeziList')
        return render(request,self.template_name,context)
    



class ListViewReportEntering(ListView):
  

    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'

    
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "  لیست نوبت های ممیزی  "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوبت ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['ردیف', 'نوع ممیزی', ]
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = TypeMomayezi.objects.all()
        list_data = []
        external_link = 'ListViewVahedReportEnteringVahed'

        counter = 1
        for query in queryset:
            data = []
            dict_temp = {}
        
            data.append(counter)
            
           
            data.append(query.title)
          
            
            

            counter += 1



        
            
        
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        
            
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data , 'external_link':external_link }
        return context

    model = TypeMomayezi
    ordering = '-created_at' 
    template_name ='listView.html'


class ListViewVahedReportEnteringVahed(ListView):
  
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = ''
    #4
    model = ReportMomayezi
    ordering = '-created_at' 
    template_name ='listMomayeziReportEnteringVahed.html'
    def get(self, request,typeId=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست واحد ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام گزارش ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان واحد' ,]
        #اسم داده های جدول
        listVahed = []
        typeSelected = TypeMomayezi.objects.get(id = typeId)
        teamSelected = MomayeziTeam.objects.all().filter(typeMomayezi =typeSelected )[0]
        
        queryset = CalenderMomayezi.objects.all().filter(teamMomayezi__id = teamSelected.id)
        allActivity = MomayeziActivityManager.objects.all().filter(activity = 'report')
        #allActivity = MomayeziActivityManager.objects.all().filter(activity = 'report').filter()
        #دریافت تمام داده ها
        
        list_data = []
        #ایجاد لیست داده ها
       
        #دیکشنری داده ها
        context = { 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'allActivity' : allActivity ,'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),'typeId':typeId , 'queryset':queryset}
        return render(request,self.template_name , context)
   

class CreateViewReportEntering( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "enterReport.html"
    menu_link = 'ViewCalenderMomayezi'
    extend ='baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    @staff_only 
    def get(self, request,typeId= None , actId= None, *args, **kwargs):
        
        
        
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک انتخاب ریسک شناسایی شده  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک انتخاب ریسک شناسایی شده  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        header_table   = [  'واحد', 'عنوان سوال' , 'شماره استاندارد' , 'بند ها'  ]
        #اسم داده های جدول

        #دریافت تمام داده ها
       
        activitySelected = MomayeziActivityManager.objects.get(id = actId)
        calenderSelected = activitySelected.calender
        vahedSelected = calenderSelected.vahedMomayezi
        
        allReportGhovat = ReportMomayezi.objects.all().filter(Q(typeMomayeziRelated = typeId) & Q(result ='ghovat') & Q(activityRelated = actId))
        allReportForsat = ReportMomayezi.objects.all().filter(Q(typeMomayeziRelated = typeId) & Q(result ='behbod') & Q(activityRelated = actId))
        allReportAdam = ReportMomayezi.objects.all().filter(Q(typeMomayeziRelated = typeId) & Q(result ='adam') & Q(activityRelated = actId))
      
        #ایجاد لیست داده ها
       

       
        #دیکشنری داده ها
     
        contex= {'extend':self.extend , 'allReportGhovat':allReportGhovat,'allReportForsat':allReportForsat , 'allReportAdam':allReportAdam, 'activity' : activitySelected.id , 'type':typeId , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'header_table':header_table , 'menuBack':self.menuBack , 'vahedSelected':vahedSelected , 'calenderSelected':calenderSelected}
        return render(request,self.template_name,contex)

  
    @staff_only
    def post(self, request ,typeId = None ,actId = None ,  *args, **kwargs):
        #فرم دریافت شده
        
        report = request.POST.get('report')
        if(report == ''):
            sweetify.toast(self.request,timer=30000 , icon="error",title ='متن گزارش را وارد کنید!!!')
            return HttpResponseRedirect(reverse('CreateViewReportEntering' , kwargs={'typeId':typeId , 'actId':actId }) )
            
        result = request.POST.get('result')
        if(result == None):
            sweetify.toast(self.request,timer=30000 , icon="error",title ='باید نوع نتیجه را انتخاب کنید!!!')
            return HttpResponseRedirect(reverse('CreateViewReportEntering' , kwargs={'typeId':typeId , 'actId':actId }) )
            
        typeSelected = TypeMomayezi.objects.get(id = typeId)
        activitySelected = MomayeziActivityManager.objects.get(id = actId)
        
        instanceReport = ReportMomayezi.objects.create(report = report ,typeMomayeziRelated = typeSelected , activityRelated =activitySelected , result = result  , vahedRelated = activitySelected.calender.vahedMomayezi)
        






        profileSender  = Profile.objects.get(id=246)
        profileReciver = self.getMafogh(profileSender)

        instanceCorrective = CorrectiveAction.objects.create(problem = 'correctiveAction' , demandantVahed = 21 ,
                                        standardRelated =activitySelected.calender.systemMomayezi , source = 'MomayeziDakheli' )
      
        instanceCorrective.demandantId = 'CA-' + str(instanceCorrective.id)
        instanceCorrective.save()

        textBox = TextDataBase.objects.create(title = 'شرح مسئله / درخواست' , text = instanceReport.report)


        instanceCorrectiveActionActivityManagerRegister = CorrectiveActionActivityManager.objects.create(reciver = profileSender , sender  = profileSender ,status='done', activity = 'register' , CorrectiveActionRelated  =instanceCorrective ,)
        instanceCorrectiveActionActivityManagerRegister.texts.add(textBox)
        
        instanceCorrectiveActionActivityManagerRegister.save()
        instanceCorrectiveActionActivityManager = CorrectiveActionActivityManager.objects.create(reciver = profileReciver , sender  = profileSender , activity = 'barresiMafogh',previousActivity = instanceCorrectiveActionActivityManagerRegister , CorrectiveActionRelated  =f)
        
        instanceCorrectiveActionActivityManager.save()
        instanceCorrectiveActionActivityManagerRegister.nextActivity = instanceCorrectiveActionActivityManager
        instanceCorrectiveActionActivityManagerRegister.save()

        sweetify.toast(self.request,timer=30000 , icon="success",title ='   گزارش مورد نظر ثبت شد  !!!')
        return HttpResponseRedirect(reverse('CreateViewReportEntering' , kwargs={'typeId':typeId , 'actId':actId }) )
        #     #تابع نمایش پیغام



class ComplateViewReportEntering( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createCalenderMomayezi.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    menu_link = 'ViewCalenderMomayezi'
    def get(self, request,actId, *args, **kwargs):
        
      
     
        activitySelected = MomayeziActivityManager.objects.get(id =actId )
        activitySelected.status = 'done'
        activitySelected.save()
        sweetify.toast(self.request,timer=30000 , icon="success",title ='ثبت برنامه زمانی به اتمام رسید        !!!')
        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menuBack':self.menuBack ,'riskDabir':is_dabir(self),}
        return redirect('ViewMomayeziDashboardMember' ,activitySelected.typeMomayeziRelated.id )

def getMafogh(profileSender):
        psotMafoghSelected = JobBank.objects.all().filter(profile=profileSender)[0].jobBankPost.postMafogh
        jobBankMafoghSelected = JobBank.objects.all().filter(jobBankPost = psotMafoghSelected)[0]

        profileReciver = jobBankMafoghSelected.profile
        return profileReciver
      
def add_report(request):
    report = request.POST.get('report')
    typeId = request.POST.get('typeMomayeziRelated')
    actId = request.POST.get('activityRelated')
   
    if(report == ''):
        sweetify.toast(request,timer=30000 , icon="error",title ='متن گزارش را وارد کنید!!!')
        return HttpResponseRedirect(reverse('CreateViewReportEntering' , kwargs={'typeId':typeId , 'actId':actId }) )
        
    result = request.POST.get('result')
    if(result == None):
        sweetify.toast(request,timer=30000 , icon="error",title ='باید نوع نتیجه را انتخاب کنید!!!')
        return HttpResponseRedirect(reverse('CreateViewReportEntering' , kwargs={'typeId':typeId , 'actId':actId }) )
    
    typeSelected = TypeMomayezi.objects.get(id = typeId)
    
    activitySelected = MomayeziActivityManager.objects.get(id = actId)
    
    instanceReport = ReportMomayezi.objects.create(report = report ,typeMomayeziRelated = typeSelected , activityRelated =activitySelected , result = result ,vahedRelated = activitySelected.calender.vahedMomayezi )
    if (instanceReport.result == 'behbod' or instanceReport.result == 'adam'):
        profileSender  = Profile.objects.get(id=246)
        profileReciver = getMafogh(profileSender)
        vahedSelected = Vahed.objects.get(id = 21)
        instanceCorrective = CorrectiveAction.objects.create(problem = 'correctiveAction' , demandantVahed = vahedSelected ,
                                        standardRelated =activitySelected.calender.systemMomayezi , source = 'MomayeziDakheli' )
        
        instanceCorrective.demandantId = 'CA-' + str(instanceCorrective.id)
        instanceCorrective.save()

        textBox = TextDataBase.objects.create(title = 'شرح مسئله / درخواست' , text = instanceReport.report)


        instanceCorrectiveActionActivityManagerRegister = CorrectiveActionActivityManager.objects.create(reciver = profileSender , sender  = profileSender ,status='done', activity = 'register' , CorrectiveActionRelated  =instanceCorrective ,)
        instanceCorrectiveActionActivityManagerRegister.texts.add(textBox)
        
        instanceCorrectiveActionActivityManagerRegister.save()
        instanceCorrectiveActionActivityManager = CorrectiveActionActivityManager.objects.create(reciver = profileReciver , sender  = profileSender , activity = 'barresiMafogh',previousActivity = instanceCorrectiveActionActivityManagerRegister , CorrectiveActionRelated  =instanceCorrective)
        
        instanceCorrectiveActionActivityManager.save()
        instanceCorrectiveActionActivityManagerRegister.nextActivity = instanceCorrectiveActionActivityManager
        instanceCorrectiveActionActivityManagerRegister.save()



    sweetify.toast(request,timer=30000 , icon="success",title ='   گزارش مورد نظر ثبت شد  !!!')
    allReportGhovat = ReportMomayezi.objects.all().filter(Q(typeMomayeziRelated = typeSelected) & Q(result ='ghovat'))
    allReportForsat = ReportMomayezi.objects.all().filter(Q(typeMomayeziRelated = typeSelected) & Q(result ='behbod'))
    allReportAdam = ReportMomayezi.objects.all().filter(Q(typeMomayeziRelated = typeSelected) & Q(result ='adam'))
    
    return render(request , 'partials/report-list.html' ,{ 'allReportGhovat' : allReportGhovat ,
                                                          'allReportForsat'  : allReportForsat ,
                                                          'allReportAdam'    : allReportAdam ,
                                                          'color' :"info"} )   
    #return HttpResponseRedirect(reverse('CreateViewReportEntering' , kwargs={'typeId':typeId , 'actId':actId }) )
   
        
        
  
def select_type_momayezi(request):
        profileSelected = Profile.objects.get(user = request.user)
      
        selectedType = request.GET.get('profileId')
        
        responsible_link = None
        member_link =  None
        if(selectedType):
            profileMomayeziSelected = TypeMomayezi.objects.get(id = selectedType)
            print(profileMomayeziSelected.id) 
        else:
            profileMomayeziSelected = TypeMomayezi.objects.all().first()
         
        partials = 'partials/momayeziDashboard.html'
        header_title = "ممیزی های سازمان"
        
        #دریافت تمام داده ها
        
        
        if(profileMomayeziSelected.modir ==profileSelected or profileSelected.user.is_superuser):
            responsible_link = None  
        for team in MomayeziTeam.objects.all().filter(typeMomayezi= profileMomayeziSelected):
            if(profileMomayeziSelected in team.memberMomayezi.all()):
                member_link = None
        
        allProfile = TypeMomayezi.objects.all()
       
        allAdam = AdamEntebagh.objects.all().filter(typeMomayeziRelated = profileMomayeziSelected)
        allGhovat = NoghatGhovat.objects.all().filter(typeMomayeziRelated = profileMomayeziSelected)
        allForsat = ForsatBehbod.objects.all().filter(typeMomayeziRelated = profileMomayeziSelected)
        allAdamLenght = len(allAdam)
        allGhovatLenght = len(allGhovat)
        allForsatLenght = len(allForsat)
        allAdamPercent = 0.0
        allGhovatPercent = 0.0
        allForsatPercent = 0.0
        listMaxAdam = {}
        listMaxGhovat = {}
        listMaxForsat = {}
        maxAdamValue = []
        maxAdamVahed = []
        maxAdamTitle = []
        maxGhovatValue = []
        maxGhovatVahed = []
        maxGhovatTitle = []
        maxForsatValue = []
        maxForsatVahed = []
        maxForsatTitle = []
      
        for forsat in allForsat:
            
            listMaxForsat[forsat.vahedBehbod] =  ForsatBehbod.objects.filter(vahedBehbod =forsat.vahedBehbod).count()
        listMaxForsat = sorted(listMaxForsat.items(), key=lambda x:x[1] , reverse=True)
        listMaxForsat = listMaxForsat[:3]
        for forsat in listMaxForsat:
            maxForsatVahed.append(forsat[0])
            maxForsatValue.append(forsat[1])
            maxForsatTitle.append(forsat[0].title)
        for ghovat in allGhovat:
            
            listMaxGhovat[ghovat.vahedGhovat] =  NoghatGhovat.objects.filter(vahedGhovat =ghovat.vahedGhovat).count()
        listMaxGhovat = sorted(listMaxGhovat.items(), key=lambda x:x[1] , reverse=True)
        listMaxGhovat = listMaxGhovat[:3]
        for ghovat in listMaxGhovat:
            maxGhovatVahed.append(ghovat[0])
            maxGhovatValue.append(ghovat[1])
            maxGhovatTitle.append(ghovat[0].title)
        for adam in allAdam:
            
            listMaxAdam[adam.vahedAdamEntebagh] =  AdamEntebagh.objects.filter(vahedAdamEntebagh =adam.vahedAdamEntebagh).count()
        listMaxAdam = sorted(listMaxAdam.items(), key=lambda x:x[1] , reverse=True)
        listMaxAdam = listMaxAdam[:3]
        for adam in listMaxAdam:
            maxAdamVahed.append(adam[0])
            maxAdamValue.append(adam[1])
            maxAdamTitle.append(adam[0].title)
        
        total =  allAdamLenght+allGhovatLenght +allForsatLenght
        
        
        #عنوان نمایش داده شده در بالای صفحه
        if(total != 0):
            allAdamPercent = ((allAdamLenght)/ total) * 100
            allGhovatPercent = ((allGhovatLenght)/ total) * 100
            allForsatPercent = ((allForsatLenght)/ total) * 100
            
        
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        context = {  'header_title':header_title,'member_link':member_link,
        'discribtion':discribtion,'icon_name':icon_name,'header_title':header_title,'responsible_link':responsible_link ,
        'color':color  ,'partials':partials,'profileMomayeziSelected':profileMomayeziSelected,'total':total,
        'allProfile' :allProfile , 'allAdamLenght' :allAdamLenght , 'allGhovatLenght' :allGhovatLenght , 'allForsatLenght' :allForsatLenght,
        'allAdamPercent' :allAdamPercent ,'allGhovatPercent' : allGhovatPercent,'allForsatPercent' :allForsatPercent
        ,'maxAdamValue' :maxAdamValue , 'maxAdamVahed' :maxAdamVahed , 'maxGhovatValue' :maxGhovatValue , 'maxGhovatVahed' :maxGhovatVahed , 'maxForsatValue' :maxForsatValue , 'maxForsatVahed' :maxForsatVahed , 'maxForsatTitle' :maxForsatTitle , 'maxGhovatTitle' :maxGhovatTitle , 'maxAdamTitle' :maxAdamTitle }
    
        return render(request , 'partials/momayeziDashboard.html' ,context )  
 
 
    
class ViewMomayeziDashboard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "clearDashboard.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    
    @staff_only 
    def get(self, request ,*args, **kwargs):
        
        visio = 'ممیزی داخلی سیستم‌ها.vsdx'
        selectedType =  request.GET.get('type') 
        createNewProfile = None
        
        responsible_link = None
        member_link =  None
        if(request.GET.get('profileId',None)):
            profileSelected = TypeMomayezi.objects.get(id = request.GET['profileId'])
        else:
            profileSelected = TypeMomayezi.objects.all().last()
        partials = 'partials/momayeziDashboard.html'
        header_title = "ممیزی های سازمان"
       
        #دریافت تمام داده ها
        member = Profile.objects.get(user = request.user)
        
        if(profileSelected.modir ==member or request.user.is_superuser):
            responsible_link = 'ViewMomayeziDashboardResponsible'  
            member_link = 'ViewMomayeziDashboardMember'
            createNewProfile = 'MomayeziCreateViewTypeMomayezi'
        for team in MomayeziTeam.objects.all().filter(typeMomayeziRelated= profileSelected):
            for members in team.memberMomayezi.all():    
              
                if(member == members):
                    member_link = 'ViewMomayeziDashboardMember'
        
        memberCount = MomayeziActivityManager.objects.all().filter(Q(typeMomayeziRelated = profileSelected)& Q(reciver__user = request.user) &Q(status  = 'doing')).count()
        responsibleCount = MomayeziActivityManager.objects.all().filter(Q(typeMomayeziRelated = profileSelected )&Q(status  = 'doing')).count()
        allProfile = TypeMomayezi.objects.all()
        allReport = ReportMomayezi.objects.all().filter(Q(typeMomayeziRelated = profileSelected) )
        allGhovat = ReportMomayezi.objects.all().filter(Q(typeMomayeziRelated = profileSelected) & Q(result ='ghovat'))
        allForsat = ReportMomayezi.objects.all().filter(Q(typeMomayeziRelated = profileSelected) & Q(result ='behbod'))
        allAdam = ReportMomayezi.objects.all().filter(Q(typeMomayeziRelated = profileSelected) & Q(result ='adam') )
      
        allAdamLenght = len(allAdam)
        allGhovatLenght = len(allGhovat)
        allForsatLenght = len(allForsat)
        allAdamPercent = 0.0
        allGhovatPercent = 0.0
        allForsatPercent = 0.0
        listMaxAdam = {}
        listMaxGhovat = {}
        listMaxForsat = {}
        maxAdamValue = []
        maxAdamVahed = []
        maxAdamTitle = []
        maxGhovatValue = []
        maxGhovatVahed = []
        maxGhovatTitle = []
        maxForsatValue = []
        maxForsatVahed = []
        maxForsatTitle = [] 
        allVahed = Vahed.objects.all()
        allGhovatVahed = []
        allForsatVahed = []
        allAdamVahed = []
        #categories = allGhovat.objects.all().filter('vahedRelated').order_by('vahedRelated').values('vahedRelated__title').annotate(count=Count('vahedRelated__title'))
        
        for vahed in allVahed:
            dictData ={'vahed' :vahed.title  ,'count': allGhovat.filter(vahedRelated__id =vahed.id).count()}
            if(dictData['count']==0):
                pass
            else:
                allGhovatVahed.append(dictData)
            dictData ={'vahed' :vahed.title  ,'count': allForsat.filter(vahedRelated__id =vahed.id).count()}
            if(dictData['count']==0):
                pass
            else:
                allForsatVahed.append(dictData)
            dictData ={'vahed' :vahed.title  ,'count': allAdam.filter(vahedRelated__id =vahed.id).count()}
            if(dictData['count']==0):
                pass
            else:
                allAdamVahed.append(dictData)

        sorted_list = sorted(allAdamVahed, key=lambda x: x['count'] , reverse=True)
        allGhovatVahed = sorted (allGhovatVahed , key = lambda x: x['count'] , reverse=True)[:3]
        allForsatVahed = sorted (allForsatVahed , key = lambda x: x['count'] , reverse=True)[:3]
        allAdamVahed = sorted (allAdamVahed , key = lambda x: x['count'] , reverse=True)[:3]

        
        # for forsat in allForsat:
          
        #     listMaxForsat[forsat.activityRelated.calender.vahedMomayezi] =  ReportMomayezi.objects.all().filter(activityRelated__calender__vahedMomayezi =forsat.activityRelated.calender.vahedMomayezi).count()
        # listMaxForsat = sorted(listMaxForsat.items(), key=lambda x:x[1] , reverse=True)
        # listMaxForsat = listMaxForsat[:3]
        # for forsat in listMaxForsat:
        #     maxForsatVahed.append(forsat[0])
        #     maxForsatValue.append(forsat[1])
        #     maxForsatTitle.append(forsat[0].title)
        # for ghovat in allGhovat:
           
        #     listMaxGhovat[ghovat.activityRelated.calender.vahedMomayezi] =  ReportMomayezi.objects.all().filter(activityRelated__calender__vahedMomayezi =ghovat.activityRelated.calender.vahedMomayezi).count()
        
        # listMaxGhovat = sorted(listMaxGhovat.items(), key=lambda x:x[1] , reverse=True)
        # listMaxGhovat = listMaxGhovat[:3]
        # for ghovat in listMaxGhovat:
        #     maxGhovatVahed.append(ghovat[0])
        #     maxGhovatValue.append(ghovat[1])
        #     maxGhovatTitle.append(ghovat[0].title)
        # for adam in allAdam:
            
        #     listMaxAdam[adam.activityRelated.calender.vahedMomayezi] =  ReportMomayezi.objects.all().filter(activityRelated__calender__vahedMomayezi =adam.activityRelated.calender.vahedMomayezi).count()
            
        # listMaxAdam = sorted(listMaxAdam.items(), key=lambda x:x[1] , reverse=True)
        # listMaxAdam = listMaxAdam[:3]
        # for adam in listMaxAdam:
        #     maxAdamVahed.append(adam[0])
        #     maxAdamValue.append(adam[1])
        #     maxAdamTitle.append(adam[0].title)
        

        total =  allAdamLenght+allGhovatLenght +allForsatLenght
        
        
        #عنوان نمایش داده شده در بالای صفحه
        if(total != 0):
            allAdamPercent = ((allAdamLenght)/ total) * 100
            allGhovatPercent = ((allGhovatLenght)/ total) * 100
            allForsatPercent = ((allForsatLenght)/ total) * 100
            
        
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
     
        
        
        context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,'member_link':member_link,
        'discribtion':discribtion,'icon_name':icon_name,'header_title':header_title,'responsible_link':responsible_link ,
        'color':color  ,'partials':partials,'profileSelected':profileSelected,'total':total,'createNewProfile':createNewProfile,
        'allProfile' :allProfile , 'allAdamLenght' :allAdamLenght , 'allGhovatLenght' :allGhovatLenght , 'allForsatLenght' :allForsatLenght,
        'allAdamPercent' :allAdamPercent ,'allGhovatPercent' : allGhovatPercent,'allForsatPercent' :allForsatPercent
        ,'maxAdamValue' :maxAdamValue , 'maxAdamVahed' :maxAdamVahed , 'maxGhovatValue' :maxGhovatValue , 'maxGhovatVahed' :maxGhovatVahed , 'maxForsatValue' :maxForsatValue , 'maxForsatVahed' :maxForsatVahed , 'maxForsatTitle' :maxForsatTitle ,
        'maxGhovatTitle' :maxGhovatTitle , 'maxAdamTitle' :maxAdamTitle,
        'memberCount':memberCount , 'responsibleCount': responsibleCount , 'visio':visio
         ,'allGhovatVahed' : allGhovatVahed , 'allForsatVahed' : allForsatVahed,'allAdamVahed' : allAdamVahed }

        return render(request,self.template_name,context)
    
    
    
    
    
class ViewMomayeziDashboardResponsible( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "dashboardResponsible.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewMomayeziDashboard'
    @staff_only 
    def get(self, request,profileId=None ,*args, **kwargs):


        header_table   = ['ریسک پروفایل','عنوان']
        #اسم داده های جدول
        object_name    = ['title','RiskProcessRelated']
        #دریافت تمام داده ها
        
        
        list_data = []
     
        profileSelected = TypeMomayezi.objects.get(id = profileId)
    #   (('1','برنامه زمانی'),('2','چک لیست'),('3','چک لیست سوال') , ('4' , 'گزارش') , ('5' , 'پایان'))ListViewCheckListMomayeziSelecting
        steps_link = [('CreateViewMomayeziTeam',profileId) , ('ViewCalenderMomayezi',profileId) , ('' ,'ListViewCheckListMomayeziSelecting' ),('ListViewCheckListMomayeziSelecting',profileId) ,('ListViewVahedReportEnteringVahed',profileId) , ('#','')]
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
        linkChange = 'ViewChangeMomayeziProfileStep'
        allActivity = MomayeziActivityManager.objects.all().filter(typeMomayeziRelated = profileSelected).order_by('status')
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
        'discribtion':discribtion,'icon_name':icon_name,'currentStep':currentStep,'lenStep':lenStep,
        'columns':columns , 'color':color , 'header_table': header_table ,'linkChange':linkChange,
         'object_name' : object_name ,  'list_data' : list_data , 'profileSelected' :profileSelected ,'steps':steps , 'allActivity':allActivity}

        return render(request,self.template_name,context)
    
    
class ViewMomayeziDashboardMember( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "dashboardMember.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewMomayeziDashboard'
    @staff_only 
    def get(self, request,profileId=None ,*args, **kwargs):


        header_table   = ['ریسک پروفایل','عنوان']
        #اسم داده های جدول
        object_name    = ['title','RiskProcessRelated']
        #دریافت تمام داده ها
        
        
        list_data = []
       
        profileSelected = TypeMomayezi.objects.get(id = profileId)
      
        steps_link = ['#','CreateViewMomayeziTeam','ListViewRiskIdentification' , 'ListViewCheckListMomayeziSelecting','ListViewRiskMeasurement' ,'#']
        steps = []
        # for idx, step in enumerate(profileSelected.STEP_LIST):
        
        #     dict_temp = {}
        #     dict_temp['step'] = step[0]
        #     dict_temp['title'] = step[1]
        #     dict_temp['link'] = steps_link[idx]

        #     steps.append(dict_temp)
        allActivity = []
        query = MomayeziActivityManager.objects.all().filter(Q(typeMomayeziRelated = profileSelected)& Q(reciver__user = request.user)).order_by('status')
        for item in query:
          
            if(item.activity == 'calender' and item.status =='doing'):
                allActivity.append(('ViewCalenderMomayezi',item , profileSelected.id , -1))  
                  
                
            elif(item.activity == 'team' and item.status =='doing'):
                
                allActivity.append(('CreateViewMomayeziTeam',item ,profileSelected.id , -1))  
                  
               
            elif(item.activity == 'cheakListQuestion' and item.status =='doing'):
                
                allActivity.append(('ListViewCheckListMomayeziSelecting',item , profileId , -1)) 
            elif(item.activity == 'cheakList' and item.status =='doing'):
                calenderSelected = item.calender
                allActivity.append(('ViewCheckListMomayeziList',item , calenderSelected.id , -1)) 
                
            elif(item.activity == 'report' and item.status =='doing'):
                
                allActivity.append(('CreateViewReportEntering',item  ,profileId ,item.id ))    
                
            else:
                allActivity.append(('#' , item))
                
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "داشبورد اعضا ریسک"
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

     
        lenSteps = len(profileSelected.STEP_LIST)
      
        
        
        if(stepId +2 != (lenSteps)):
            x = profileSelected.STEP_LIST[stepId+2]

            
            profileSelected.step = x[0]
            
            profileSelected.save()
          
            
        else:
            
            x = profileSelected.STEP_LIST[-1]
            
            
            profileSelected.step = x[0]
            
            
            profileSelected.save()
            y=  profileSelected.step
            

      
        #دیکشنری داده ها
        context = {}

        return redirect('ViewRiskDashboardResponsible', profileId=profileSelected.id)
    


class ViewChangeMomayeziProfileStep( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
   
    template_name = "dashboardResponsible.html"
    
    @staff_only 
    def get(self, request,profileId=None , stepId=None ,*args, **kwargs):

        profileSelected = TypeMomayezi.objects.get(id = profileId)
        
        lenSteps = len(profileSelected.STEP_LIST)
        allActivity = MomayeziActivityManager.objects.all().filter(Q(typeMomayeziRelated = profileSelected)& Q(status = 'doing'))
        for activity in allActivity:
            x= activity.ACTIVITY_LIST[stepId]
            y= activity.activity 
            
            if(activity.activity == activity.ACTIVITY_LIST[stepId][0]):
                
                activity.status = 'doNot'
                activity.save()
        
        if(stepId +2 != (lenSteps)):
            x = profileSelected.STEP_LIST[stepId+1]

            
            profileSelected.step = x[0]
            
            profileSelected.save()
          
            
        else:
            
            x = profileSelected.STEP_LIST[-1]
            
            
            profileSelected.step = x[0]
            
            
            profileSelected.save()
            y=  profileSelected.step
        
       
      
        #دیکشنری داده ها
        context = {}

        return redirect('ViewMomayeziDashboardResponsible', profileId=profileSelected.id)
    
    
# class ViewRiskDashboardMember( LoginRequiredMixin,View):
#     redirect_field_name = '/profile/login'
#     template_name = "dashboardMember.html"
#     extend = 'baseEmployee.html'
#     menuBack = 'ViewRiskDashboard'
#     @staff_only 
#     def get(self, request,profileId=None ,*args, **kwargs):


#         header_table   = ['ریسک پروفایل','عنوان']
#         #اسم داده های جدول
#         object_name    = ['title','RiskProcessRelated']
#         #دریافت تمام داده ها
        
        
#         list_data = []
       
#         profileSelected = RiskProfile.objects.get(id = profileId)
      
#         steps_link = ['#','ListViewRiskIdentification' , 'ListViewRiskIdentificationSelecting','ListViewRiskMeasurement' ,'#']
#         steps = []
#         for idx, step in enumerate(profileSelected.STEP_LIST):
        
#             dict_temp = {}
#             dict_temp['step'] = step[0]
#             dict_temp['title'] = step[1]
#             dict_temp['link'] = steps_link[idx]

#             steps.append(dict_temp)
#         allActivity = []
#         query = RiskActivityManager.objects.all().filter(Q(riskProfile = profileSelected)& Q(reciver__user = request.user)).order_by('status')
#         for item in query:
#             if(item.activity == 'identification' and item.status =='doing'):
#                 allActivity.append(('ListViewRiskIdentification',item))    
#             elif(item.activity == 'measurement' and item.status =='doing'):
#                 allActivity.append(('ListViewRiskMeasurement',item))    
#             else:
#                 allActivity.append(('#' , item))
#         #عنوان نمایش داده شده در بالای صفحه
#         header_title  = "داشبور اعضا ریسک"
#         #توضحات نمایش داده شده در زیر عنوان
#         discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
#         #آیکون نمایش داده شده در بخش بالای سایت            
#         icon_name     = "person_add"
#         #تعداد ستون ها            
#         color         = "info"
        

       
            
        
#         #رنگ             
#         columns       = 1
#         #دیکشنری داده ها
#         context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
#         'discribtion':discribtion,'icon_name':icon_name,'profileSelected':profileSelected,
#         'columns':columns , 'color':color , 'header_table': header_table ,
#          'object_name' : object_name ,  'list_data' : list_data , 'profileSelected' :profileSelected ,'steps':steps , 'allActivity':allActivity , 'stepsLink':steps_link}

#         return render(request,self.template_name,context)
    
  


# class ViewRiskDashboardResponsible( LoginRequiredMixin,View):
#     redirect_field_name = '/profile/login'
#     template_name = "dashboardResponsible.html"
#     extend = 'baseEmployee.html'
#     menuBack = 'ViewRiskDashboard'
#     @staff_only 
#     def get(self, request,profileId=None ,*args, **kwargs):


#         header_table   = ['ریسک پروفایل','عنوان']
#         #اسم داده های جدول
#         object_name    = ['title','RiskProcessRelated']
#         #دریافت تمام داده ها
        
        
#         list_data = []
       
#         profileSelected = RiskProfile.objects.get(id = profileId)
      
#         steps_link = ['ListViewRiskIdentification' , 'ListViewRiskIdentificationSelecting','ListViewRiskMeasurement' ,'#']
#         steps = []
#         for idx, step in enumerate(profileSelected.STEP_LIST):
        
#             dict_temp = {}
#             dict_temp['step'] = step[0]
#             dict_temp['title'] = step[1]
#             dict_temp['link'] = steps_link[idx]

#             steps.append(dict_temp)
#         allActivity = RiskActivityManager.objects.all().filter(riskProfile = profileSelected).order_by('status')
#         #عنوان نمایش داده شده در بالای صفحه
#         header_title  = "داشبور دیبر ریسک"
#         #توضحات نمایش داده شده در زیر عنوان
#         discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
#         #آیکون نمایش داده شده در بخش بالای سایت            
#         icon_name     = "person_add"
#         #تعداد ستون ها            
#         color         = "info"
        

       
            
        
#         #رنگ             
#         columns       = 1
#         #دیکشنری داده ها
#         context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
#         'discribtion':discribtion,'icon_name':icon_name,
#         'columns':columns , 'color':color , 'header_table': header_table ,
#          'object_name' : object_name ,  'list_data' : list_data , 'profileSelected' :profileSelected ,'steps':steps , 'allActivity':allActivity}

#         return render(request,self.template_name,context)
    
    
# class ViewRiskDashboardMember( LoginRequiredMixin,View):
#     redirect_field_name = '/profile/login'
#     template_name = "dashboardMember.html"
#     extend = 'baseEmployee.html'
#     menuBack = 'ViewRiskDashboard'
#     @staff_only 
#     def get(self, request,profileId=None ,*args, **kwargs):


#         header_table   = ['ریسک پروفایل','عنوان']
#         #اسم داده های جدول
#         object_name    = ['title','RiskProcessRelated']
#         #دریافت تمام داده ها
        
        
#         list_data = []
       
#         profileSelected = RiskProfile.objects.get(id = profileId)
      
#         steps_link = ['#','ListViewRiskIdentification' , 'ListViewRiskIdentificationSelecting','ListViewRiskMeasurement' ,'#']
#         steps = []
#         for idx, step in enumerate(profileSelected.STEP_LIST):
        
#             dict_temp = {}
#             dict_temp['step'] = step[0]
#             dict_temp['title'] = step[1]
#             dict_temp['link'] = steps_link[idx]

#             steps.append(dict_temp)
#         allActivity = []
#         query = RiskActivityManager.objects.all().filter(Q(riskProfile = profileSelected)& Q(reciver__user = request.user)).order_by('status')
#         for item in query:
#             if(item.activity == 'identification' and item.status =='doing'):
#                 allActivity.append(('ListViewRiskIdentification',item))    
#             elif(item.activity == 'measurement' and item.status =='doing'):
#                 allActivity.append(('ListViewRiskMeasurement',item))    
#             else:
#                 allActivity.append(('#' , item))
#         #عنوان نمایش داده شده در بالای صفحه
#         header_title  = "داشبور اعضا ریسک"
#         #توضحات نمایش داده شده در زیر عنوان
#         discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
#         #آیکون نمایش داده شده در بخش بالای سایت            
#         icon_name     = "person_add"
#         #تعداد ستون ها            
#         color         = "info"
        

       
            
        
#         #رنگ             
#         columns       = 1
#         #دیکشنری داده ها
#         context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,
#         'discribtion':discribtion,'icon_name':icon_name,'profileSelected':profileSelected,
#         'columns':columns , 'color':color , 'header_table': header_table ,
#          'object_name' : object_name ,  'list_data' : list_data , 'profileSelected' :profileSelected ,'steps':steps , 'allActivity':allActivity , 'stepsLink':steps_link}

#         return render(request,self.template_name,context)
    
  
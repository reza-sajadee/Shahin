from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CreateFormTypeMadrak , CreateFormMostanadatDakheli , CreateFormMostanadatKhareji , ViewFormMostanadatDakheli , ViewFormMostanadatKhareji ,CreateFormMostanadatDakheliChange ,CreateFormRecordDataBase
from .models import TypeMadrak , MostanadatDakheli , MostanadatKhareji ,TextDataBase , MostanadatDakheliChangeActivityManager ,MostanadatDakheliChange , ConfirmationDataBase ,category_choices ,RecordDataBase , RecordChangeActivityManager
from django.db.models import Q
from django.views.generic import ListView
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import MostanadatDakheliFilter
from jalali_date import datetime2jalali, date2jalali
from risk_app.utils import is_dabir
from Caspian.settings import STATICFILES_DIRS ,MEDIA_ROOT
from django.core.files.storage import default_storage
import os.path
from profile_app.models import Profile
from django.core.files.storage import FileSystemStorage
from organization_app.models import Vahed , TypePostSazmani ,JobBank
from standardTable_app.models import Standard
from Caspian.settings import BASE_DIR
class TypeMadrakHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "TypeMadrak.html"
    def get(self, request,*args, **kwargs):


        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewTypeMadrak( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد
    template_name = "create.html"
    extend = 'base.html'
    def get(self, request, *args, **kwargs):
        form = CreateFormTypeMadrak()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک نوع مدرک  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع مدرک  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ
        color         = "success"
        #دیکشنری داده ها
        contex = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormTypeMadrak(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='نوع مدرک  جدید با موفقیت ساخته شد !!!')
            return redirect('MostanadatListViewTypeMadrak')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='نوع مدرک  مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewTypeMadrak(ListView):


    extend = 'base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست نوع مدرک  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوع مدرک  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ
        color         = "info"
        #عنوان های جدول
        header_table   = ['نوع مدرک' , 'کد نوع مدرک']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = TypeMadrak.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.typeMadrakCode)







            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table
          ,  'list_data' : list_data}
        return context

    model = TypeMadrak
    ordering = '-created_at'
    template_name ='list.html'

class UpdateViewTypeMadrak( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
    def get_obj(self):

        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(TypeMadrak,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormTypeMadrak(instance=obj)

            obj = get_object_or_404(TypeMadrak,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش نوع مدرک  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این نوع مدرک  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت
            icon_name     = "person_add"
            #تعداد ستون ها
            color         = "info"
            #رنگ
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)

    def post(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormTypeMadrak(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='نوع مدرک  جدید با موفقیت ساخته شد !!!')
                return redirect('MostanadatListViewTypeMadrak')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='نوع مدرک  مورد نظر ساخته نشد !')
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewTypeMadrak( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(TypeMadrak,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک نوع مدرک "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که نوع مدرک   " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت
            icon_name     = "delete_forever"
            #تعداد ستون ها
            color         = "danger"
            #رنگ
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend':self.extend,'riskDabir':is_dabir(self),'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}

        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='نوع مدرک  با موفقیت پاک شد !!!')
            context={'extend':self.extend,'riskDabir':is_dabir(self)}
            return redirect('MostanadatListViewTypeMadrak')
        return render(request,self.template_name,context)





class MostanadatDakheliHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "MostanadatDakheli.html"
    def get(self, request,*args, **kwargs):


        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewMostanadatDakheli( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد
    template_name = "create.html"
    extend = 'base.html'
    def get(self, request, *args, **kwargs):
        form = CreateFormMostanadatDakheli()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک مستند داخلی  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک مستند داخلی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ
        color         = "success"
        #دیکشنری داده ها
        contex = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormMostanadatDakheli(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='مستند داخلی  جدید با موفقیت ساخته شد !!!')
            return redirect('MostanadatListViewDakheli')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='مستند داخلی  مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewMostanadatDakheliOutdated(ListView):
    extend = 'baseEmployee.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "مدارک منسوخ"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام مستند داخلی   را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ
        color         = "info"
        #عنوان های جدول
        header_table   = [ 'عنوان سند','طبقه بندی','نوع مدرک']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = MostanadatDakheli.objects.all().filter(outdated = True)
        queryset_filter = MostanadatDakheliFilter(self.request.GET, queryset=queryset)
        list_data = []

        #ایجاد لیست داده ها
        for query in queryset_filter.qs:
            data = []
            dict_temp = {}
            data.append(query.title)

            data.append(query.tabaghbandi)
      
     
            data.append('سایر')

            dict_temp = {query.id : data}
            list_data.append(dict_temp)

            viewLink = "view/" + str(query.id)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table
          ,  'list_data' : list_data , "filter": queryset_filter }
        return context

    model = MostanadatDakheli
    ordering = '-created_at'
    template_name ='madarek_mansokh.html'

class ListViewMostanadatDakheli(ListView):
    extend = 'baseEmployee.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست مستند داخلی  "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام مستند داخلی   را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ
        color         = "info"
        #عنوان های جدول
        header_table   = [ 'نوع مدرک' , 'عنوان سند','طبقه بندی','واحد متولی',]
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = MostanadatDakheli.objects.all().filter(outdated = False)
        queryset_filter = MostanadatDakheliFilter(self.request.GET, queryset=queryset)
        list_data = []

        #ایجاد لیست داده ها
        for query in queryset_filter.qs:
            data = []
            dict_temp = {}
            data.append(query.typeMadrakCode.title)
            data.append(query.title)

            data.append(query.tabaghbandi)
            data.append(query.vahedMotevaliCode)
        
            

            dict_temp = {query.id : data}
            list_data.append(dict_temp)

            viewLink = "view/" + str(query.id)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table
          ,  'list_data' : list_data , "filter": queryset_filter }
        return context

    model = MostanadatDakheli
    ordering = '-created_at'
    template_name ='searchList.html'



class ViewMostanadatDakheliDashboard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "clearDashboard.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
   
    def get(self, request ,*args, **kwargs):
        userProfile = Profile.objects.get(user=self.request.user)
        allActivity = MostanadatDakheliChangeActivityManager.objects.all().filter(~Q(status = 'done'))
        allLenghtDo = len(allActivity.filter(Q(status='doing') ))
        partials = 'partials/dakheliDashboard.html'
        allMostanadat = MostanadatDakheli.objects.all()
        
        
        allCreatedAction = {}
        allComplated = {}
        profileSelected = None
        responsibleCount = 0
        memberCount = 0
        createNewProfile = None
        allProfile=None
        if(request.user.is_superuser):
            activityNotDone = allActivity.filter(status='doing' )
        else:
            activityNotDone = allActivity.filter(Q(reciver = userProfile) & Q(status='doing') )
       
        responsible_link = None
        member_link =  None
        if(len(activityNotDone) >0):
            memberCount = len(activityNotDone)
            member_link = None   

        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "مستندات داخلی"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        queryset = MostanadatDakheli.objects.all().filter(outdated = False)
        list_data = []
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.typeMadrakCode.title)
            data.append(query.title)

            data.append(query.tabaghbandi)
            data.append(query.vahedMotevaliCode)
        
            

            dict_temp = {query.id : data}
            list_data.append(dict_temp)

            viewLink = "view/" + str(query.id)
        
        
            
        
        
        
        visio = 'مدیریت مستندات و سوابق.vsdx'
        
        #رنگ             
        columns       = 1
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack, 'header_title':header_title,'profileSelected':profileSelected,'createNewProfile':createNewProfile,
        'discribtion':discribtion,'icon_name':icon_name,'header_title':header_title,'responsible_link':responsible_link,'member_link':member_link,
        'columns':columns , 'color':color ,'partials':partials, 'allProfile':allProfile , 'allLenghtDo':allLenghtDo, 'responsibleCount':responsibleCount,'memberCount':memberCount ,'list_data':list_data , 'visio':visio
        }

        return render(request,self.template_name,context)
    




class UpdateViewMostanadatDakheli( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
    def get_obj(self):

        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MostanadatDakheli,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormMostanadatDakheli(instance=obj)

            obj = get_object_or_404(MostanadatDakheli,id = id)
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
            context =  {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)

    def post(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormMostanadatDakheli(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='مستند داخلی  جدید با موفقیت ساخته شد !!!')
                return redirect('MostanadatListViewDakheli')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='مستند داخلی  مورد نظر ساخته نشد !')
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)


class ViewMostanadatDakheli( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "viewmostanadatdakheli.html"
    extend = 'baseEmployee.html'
    def get_obj(self):

        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MostanadatDakheli,id = id)
        return obj

    def get_link(self , obj):
        mostanadPath =  MEDIA_ROOT + "/mostanad/"

        if(os.path.exists(mostanadPath + str(obj.dakheliSanadCode) + '.pdf')):
            return('mostanad/' + str(obj.dakheliSanadCode) + '.pdf')
        if(os.path.exists(mostanadPath + str(obj.dakheliSanadCode) + '.docx')):
            return('mostanad/' + str(obj.dakheliSanadCode) + '.docx')
        if(os.path.exists(mostanadPath + str(obj.dakheliSanadCode) + '.doc')):
            return('mostanad/' + str(obj.dakheliSanadCode) + '.doc')
        if(os.path.exists(mostanadPath + str(obj.dakheliSanadCode) + '.xls')):
            return('mostanad/' + str(obj.dakheliSanadCode) + '.xls')
        if(os.path.exists(mostanadPath + str(obj.dakheliSanadCode) + '.xlsx')):
            return('mostanad/' + str(obj.dakheliSanadCode) + '.xlsx')
        return('در دسترس نیست')


    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = ViewFormMostanadatDakheli(instance=obj)
            #print(default_storage.exists('caspian'))

            linkAdress = self.get_link(obj)
            obj = get_object_or_404(MostanadatDakheli,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش مستند داخلی  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت
            icon_name     = "person_add"
            #تعداد ستون ها
            color         = "info"


            dateLastUpdate     = datetime2jalali(obj.updated_at).strftime('14%y/%m/%d')
            typeMadrakTitle    = linkAdress
            vahedMotevali      = obj.vahedMotevaliCode.title
            vahedTaeid         = obj.vahedTaeidCode.title
            vahedTasvib        = obj.vahedTasvibCode.title
            vahedMortabet =''
            for vahed in obj.vahedMortabetCode.all():
                vahedMortabet +=vahed.title

            listData = []
            historyChange = MostanadatDakheliChange.objects.all().filter(documentRelated = obj)
            for change in historyChange:
                firstStepHistory = MostanadatDakheliChangeActivityManager.objects.all().filter(activity = 'register').filter(MostanadatDakheliChangeRelated = change)
                lastStepHistory  = firstStepHistory[0].lastStep
                data = (change , firstStepHistory[0] , lastStepHistory)
                
                listData.append(data)

            #رنگ
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name, 'obj':obj,
            'color':color , 'columns':columns , 'dateLastUpdate' : dateLastUpdate , 'vahedMotevali':vahedMotevali , 'vahedMortabet':vahedMortabet  ,'typeMadrakTitle':typeMadrakTitle, 'vahedTaeid':vahedTaeid , 'vahedTasvib':vahedTasvib , 'linkAdress' : linkAdress , 'listData':listData}


        return render(request,self.template_name,context)


class ViewMostanadatDakheliOutdated( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "viewmostanadatdakheliOutdated.html"
    extend = 'baseEmployee.html'
    def get_obj(self):

        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MostanadatDakheli,id = id)
        return obj

    def get_link(self , obj):
        mostanadPath =  MEDIA_ROOT + "/mostanad/"
        if(os.path.exists(mostanadPath + str(obj.dakheliSanadCode) + '.pdf')):
            return('mostanad/' + str(obj.dakheliSanadCode) + '.pdf')
        if(os.path.exists(mostanadPath + str(obj.dakheliSanadCode) + '.docx')):
            return('mostanad/' + str(obj.dakheliSanadCode) + '.docx')
        if(os.path.exists(mostanadPath + str(obj.dakheliSanadCode) + '.doc')):
            return('mostanad/' + str(obj.dakheliSanadCode) + '.doc')
        if(os.path.exists(mostanadPath + str(obj.dakheliSanadCode) + '.xls')):
            return('mostanad/' + str(obj.dakheliSanadCode) + '.xls')
        if(os.path.exists(mostanadPath + str(obj.dakheliSanadCode) + '.xlsx')):
            return('mostanad/' + str(obj.dakheliSanadCode) + '.xlsx')
        return('disabled')


    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = ViewFormMostanadatDakheli(instance=obj)
            #print(default_storage.exists('caspian'))

            linkAdress = self.get_link(obj)
            obj = get_object_or_404(MostanadatDakheli,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش مستند داخلی  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت
            icon_name     = "person_add"
            #تعداد ستون ها
            color         = "info"


            dateLastUpdate     = datetime2jalali(obj.updated_at).strftime('14%y/%m/%d')
            typeMadrakTitle    = linkAdress
            if(obj.vahedMotevaliCode != None):
                vahedMotevali = obj.vahedMotevaliCode.title
            else:
                vahedMotevali = 'نامعلوم'
            if(obj.vahedTaeidCode != None):
                vahedTaeid = obj.vahedTaeidCode.title
            else:
                vahedTaeid = 'نامعلوم'
            if(obj.vahedTasvibCode != None):
                vahedTasvib = obj.vahedTasvibCode.title
            else:
                vahedTasvib = 'نامعلوم'

            
            vahedMortabet =''
            for vahed in obj.vahedMortabetCode.all():
                vahedMortabet +=vahed.title
            listData = []
            historyChange = MostanadatDakheliChange.objects.all().filter(documentRelated = obj)
            for change in historyChange:
                firstStepHistory = MostanadatDakheliChangeActivityManager.objects.all().filter(activity = 'register').filter(MostanadatDakheliChangeRelated = change)
                lastStepHistory  = MostanadatDakheliChangeActivityManager.objects.all().filter(activity = 'isDelete').filter(MostanadatDakheliChangeRelated = change)
                data = (change , firstStepHistory[0] , lastStepHistory[0])
                
                listData.append(data)

            #رنگ
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns , 'dateLastUpdate' : dateLastUpdate , 'vahedMotevali':vahedMotevali , 'vahedMortabet':vahedMortabet  ,'typeMadrakTitle':typeMadrakTitle, 'vahedTaeid':vahedTaeid , 'vahedTasvib':vahedTasvib , 'linkAdress' : linkAdress , 'listData' : listData}


        return render(request,self.template_name,context)




class CreateViewMostanadatDakheliChange( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "MostanadatDakheliChangeCreate.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    def getMafogh(self ,profileSender):
        psotMafoghSelected = JobBank.objects.all().filter(profile=profileSender)[0].jobBankPost.postMafogh
        jobBankMafoghSelected = JobBank.objects.all().filter(jobBankPost = psotMafoghSelected)[0]

        profileReciver = jobBankMafoghSelected.profile
        return profileReciver
    def get(self, request, *args, **kwargs):
        selectedId=  request.GET.get('id') 
        if(selectedId!=None):
            obj = get_object_or_404(MostanadatDakheli,id = selectedId)
            form = CreateFormMostanadatDakheliChange(initial = {'documentRelated' : obj })
        else:
            obj=None
            form = CreateFormMostanadatDakheliChange()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ثبت درخواست حذف تغییر و یا تغییر سند"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک درخواست تغییر ، حذف یا تدوین  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        
        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menu_link':self.menu_link,'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name , 'selectedId':selectedId ,
        'columns' : columns , 'color' : color , 'obj':obj}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        profileSender  = Profile.objects.filter(user=self.request.user)[0]
      
        form = CreateFormMostanadatDakheliChange(request.POST,request.FILES)
        
        profileReciver = self.getMafogh(profileSender)
        profileSender  = Profile.objects.filter(user=self.request.user)[0]
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            f = form.save()
            f.save()

            textBox = TextDataBase.objects.create(title = 'توضیح درخواست کننده' , text = request.POST.get('description'))
            if(request.FILES.get('document', False)):
                document = request.FILES.get('document', False)
                instanceMostanadatDakheliChangeActivityManagerRegister = MostanadatDakheliChangeActivityManager.objects.create(reciver = profileReciver , sender  = profileSender ,status='done', activity = 'register' , MostanadatDakheliChangeRelated  =f , file = document)
            else:
                instanceMostanadatDakheliChangeActivityManagerRegister = MostanadatDakheliChangeActivityManager.objects.create(reciver = profileReciver , sender  = profileSender ,status='done', activity = 'register' , MostanadatDakheliChangeRelated  =f )
            instanceMostanadatDakheliChangeActivityManagerRegister.texts.add(textBox)
            instanceMostanadatDakheliChangeActivityManagerRegister.save()

            instanceMostanadatDakheliChangeActivityManager = MostanadatDakheliChangeActivityManager.objects.create(reciver = profileReciver , sender  = profileSender , activity = 'barresiMafogh',previousActivity = instanceMostanadatDakheliChangeActivityManagerRegister , MostanadatDakheliChangeRelated  =f)
            
            instanceMostanadatDakheliChangeActivityManager.save()
            instanceMostanadatDakheliChangeActivityManagerRegister.nextActivity = instanceMostanadatDakheliChangeActivityManager
            instanceMostanadatDakheliChangeActivityManagerRegister.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title =' درخواست تغییر ، حذف یا تدوین مدرک  جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewMostanadatDakheliChangeDoing')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title =' درخواست تغییر ، حذف یا تدوین مدرک  مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'form': form }
        return render(request,self.template_name,context)




class ListViewMostanadatDakheliChangeDoing(ListView):
  

    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست    تغییر ، حذف یا تدوین سند"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام درخواست تغییر ، حذف یا تدوین  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = [  'واحد درخواست کننده' , 'مرحله اقدام' , ]
        #اسم داده های جدول
        status =  self.request.GET.get('status') 
        
        #دریافت تمام داده ها
        
        list_data = []
        userProfile = Profile.objects.filter(user=self.request.user)[0]
        if(status == 'done'):
            queryset = MostanadatDakheliChangeActivityManager.objects.all().filter(status='done')
        else:
            queryset = MostanadatDakheliChangeActivityManager.objects.all().filter(status='doing')
        if(self.request.user.is_superuser):
            pass
        else:
            queryset = queryset.filter(reciver = userProfile)
        
        
        
        
        
        #ایجاد لیست داده ها
        for query in queryset:
            
            
            data = []
            dict_temp = {}
            
            data.append(query.MostanadatDakheliChangeRelated.vahedRelated)
            data.append(query.get_activity_display)
            data.append(query.reciver)


            


        
            
        
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = { 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data ,'extend':self.extend , 'menu_link':self.menu_link}
        return context

    model = MostanadatDakheliChange
    ordering = '-created_at' 
    template_name ='MostanadatDakheliChangeListStep.html'



class CreateViewMostanadatDakheliChangeStep( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "mostanadatDakheliChangeCreateStep.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    
    #karshenasProfile = Profile.objects.all().filter(profile = )

    #modirToseProfile = Profile.objects.get(id =id1 )
    #modirToseProfile = Profile.objects.get(id =id1 )
    karshenasProfile = 1
    karshenasProfile = 2
    def getMafogh(self ,profileSender):
        psotMafoghSelected = JobBank.objects.all().filter(profile=profileSender)[0].jobBankPost.postMafogh
        jobBankMafoghSelected = JobBank.objects.all().filter(jobBankPost = psotMafoghSelected)[0]

        profileReciver = jobBankMafoghSelected.profile
        return profileReciver
    def get_obj(self , activitySelected):
                id = activitySelected.MostanadatDakheliChangeRelated.documentRelated.id
                #id = self.kwargs.get('id')
                obj=None
                if id is not None:
                    obj = get_object_or_404(MostanadatDakheli,id = id)
                return obj
    def saveing(self ,activitySelected , text  , profileSender , profileReciver  ,confirm , titleText  ,nextStep ,file=None ,nextFailStep=None ,profileReciverField=None ):
        if(confirm =='yes'):
            
                
            MostanadatDakheliChangeSelected = activitySelected.MostanadatDakheliChangeRelated
            cdb = ConfirmationDataBase.objects.create( title =titleText ,profile =profileReciver  ,confirm =confirm ,text = text ) 
            activitySelected.confirmations=cdb
            activitySelected.status = 'done'
            instanceMostanadatDakheliChangeActivityManager = MostanadatDakheliChangeActivityManager.objects.create(reciver = profileReciver , sender  = profileSender , activity = nextStep,previousActivity = activitySelected , MostanadatDakheliChangeRelated  =activitySelected.MostanadatDakheliChangeRelated)
            activitySelected.nextActivity = instanceMostanadatDakheliChangeActivityManager
            if(file != None):
                activitySelected.file = file
            activitySelected.save()
            instanceMostanadatDakheliChangeActivityManager.save()
            return True
        elif(confirm =='completed'):
            activitySelected.status = 'completed'
            if  text != None:
                activitySelected.texts.add(text)
            activitySelected.save()
            return False
        else:
            cdb = ConfirmationDataBase.objects.create( title =titleText ,profile =profileReciver  ,confirm ='no' ,text = text ) 
            activitySelected.confirmations=cdb
            activitySelected.status = 'done'
            instanceMostanadatDakheliChangeActivityManager = MostanadatDakheliChangeActivityManager.objects.create(reciver = profileReciverField , sender  = profileSender , activity = nextFailStep,previousActivity = activitySelected , MostanadatDakheliChangeRelated  =activitySelected.MostanadatDakheliChangeRelated)
            activitySelected.nextActivity = instanceMostanadatDakheliChangeActivityManager
            activitySelected.save()
            instanceMostanadatDakheliChangeActivityManager.save()
            
    def get(self, request, activityId,*args, **kwargs):
        form = CreateFormMostanadatDakheliChange()
        formMostanadatDakheli = CreateFormMostanadatDakheli()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = " درخواست تغییر ، حذف یا تدوین"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک درخواست تغییر ، حذف یا تدوین  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        texts = []
        boolians = []
        confirmation = ''
        fields = ''
        cause = ''
        profiles = ''
        definitionCorrectiveaAtion = ''
        profilesPosts = ''
        filedSelected = ''
        queryset = MostanadatDakheli.objects.all()
        
        activitySelected = MostanadatDakheliChangeActivityManager.objects.all().filter(id = activityId)[0]
        firstActivity = activitySelected.firstStep()
        all = activitySelected.allActivityList()
        allVahed = Vahed.objects.all()
        allPostType  =  TypePostSazmani.objects.all()
        allSystem    = Standard.objects.all()
        allType   = TypeMadrak.objects.all()
        if(activitySelected.lastStep().activity == 'editDoc'):
            
            obj = self.get_obj(activitySelected)
            
            if obj is not None:
                formMostanadatDakheli = CreateFormMostanadatDakheli(instance=obj)
                
                formMostanadatDakheli.versionNumber = int(obj.versionNumber) + 1
                
                contex = {'extend':self.extend , 'menu_link':self.menu_link,'form': form, 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name ,
                'columns' : columns , 'color' : color , 'activitySelected':activitySelected , 'texts' : texts,'boolians' : boolians,
                'confirmation' : confirmation ,  'fields' : fields ,'cause' :cause , 'profilesPosts':profilesPosts , 'definitionCorrectiveaAtion' : definitionCorrectiveaAtion , 'filedSelected' : filedSelected , 'all' : all , 'formMostanadatDakheli' : formMostanadatDakheli , 'obj':obj ,'allVahed':allVahed ,'allPostType':allPostType ,'allSystem':allSystem ,'allType':allType , 'category_choices' : category_choices} 
                return render(request,self.template_name,contex)

        if(activitySelected.lastStep().activity == 'reform'):
            obj = get_object_or_404(MostanadatDakheliChange,id = activitySelected.MostanadatDakheliChangeRelated.id)
            form = CreateFormMostanadatDakheliChange(instance = obj)
        

        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menu_link':self.menu_link,'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'activitySelected':activitySelected , 'texts' : texts,'boolians' : boolians,
        'confirmation' : confirmation ,  'fields' : fields ,'cause' :cause , 'profilesPosts':profilesPosts , 'definitionCorrectiveaAtion' : definitionCorrectiveaAtion , 'filedSelected' : filedSelected , 'all' : all , 'formMostanadatDakheli' : formMostanadatDakheli , 'allVahed' :allVahed , 'allPostType' : allPostType , 'allSystem' : allSystem , 'allType' : allType , 'category_choices' : category_choices} 
        return render(request,self.template_name,contex)


    def post(self, request,activityId , *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormMostanadatDakheliChange(request.POST,request.FILES)
        profileReciver = Profile.objects.filter(id=321)[0]
        profileSender  = Profile.objects.filter(user=self.request.user)[0]
        activitySelected = MostanadatDakheliChangeActivityManager.objects.all().filter(id = activityId)[0]
        MostanadatDakheliChangeSelected = activitySelected.MostanadatDakheliChangeRelated
        if(activitySelected.activity == 'reform'):    
        #بررسی صحت اطلاعات ورودی
            obj = get_object_or_404(MostanadatDakheliChange,id = activitySelected.MostanadatDakheliChangeRelated.id)
            form = CreateFormMostanadatDakheliChange(request.POST or request.FILES , instance = obj)

            if form.is_valid():
                form.save()
                if(request.FILES.get('document', False)):
                    result = self.saveing(activitySelected , text = request.POST.get('description') ,  profileSender = profileSender , profileReciver = self.getMafogh(profileSender) , confirm = 'yes'  , titleText = 'تکمیل مدارک' , nextStep = 'barresiMafogh',nextFailStep = 'register' , file = request.FILES['document'] )
                else:
                    result = self.saveing(activitySelected , text = request.POST.get('description') ,  profileSender = profileSender , profileReciver = self.getMafogh(profileSender) , confirm = 'yes'  , titleText = 'تکمیل مدارک' , nextStep = 'barresiMafogh',nextFailStep = 'register'  )
                
                
                #تابع نمایش پیغام
                if(result):
                    sweetify.toast(self.request,timer=30000 , icon="success",title ='درخواست تغییر ، حذف یا تدوین توسط کارشناس دفتر توسعه مدیریت و تحقیقات مورد تایید قرار گرفت!!!')
                else:
                    sweetify.toast(self.request,timer=30000 , icon="warning",title ='درخواست تغییر ، حذف یا تدوین به اتمام رسید!!!')
                return redirect('ListViewMostanadatDakheliChangeDoing')
            else :
                sweetify.toast(self.request,timer=30000 , icon="error",title ='درخواست تغییر ، حذف یا تدوین  مورد نظر ساخته نشد !')
        if(activitySelected.activity == 'barresiMafogh'):
                
                
                result = self.saveing(activitySelected , text = request.POST.get('description') ,  profileSender = profileSender , profileReciver = self.karshenasProfile , confirm = request.POST.get('submit')  , titleText = 'بررسی درخواست توسط کارشناس دفتر توسعه مدیریت و تحقیقات' , nextStep = 'barresiKarshenas',nextFailStep = 'reform' ,profileReciverField=profileSender )
                if(result):
                    sweetify.toast(self.request,timer=30000 , icon="success",title ='درخواست تغییر ، حذف یا تدوین توسط کارشناس دفتر توسعه مدیریت و تحقیقات مورد تایید قرار گرفت!!!')
                else:
                    sweetify.toast(self.request,timer=30000 , icon="warning",title ='درخواست تغییر ، حذف یا تدوین به اتمام رسید!!!')
                return redirect('ListViewMostanadatDakheliChangeDoing')
        if(activitySelected.activity == 'barresiKarshenas'):
            result = self.saveing(activitySelected , text = request.POST.get('description') ,  profileSender = profileSender , profileReciver = self.modirToseProfile , confirm = request.POST.get('submit') , titleText = 'بررسی درخواست توسط کارشناس دفتر توسعه مدیریت و تحقیقات' , nextStep = 'barresiModir' ,nextFailStep = 'reform',profileReciverField=profileSender )
            if(result):
                sweetify.toast(self.request,timer=30000 , icon="success",title ='درخواست تغییر ، حذف یا تدوین توسط کارشناس دفتر توسعه مدیریت و تحقیقات مورد تایید قرار گرفت!!!')
            else:
                sweetify.toast(self.request,timer=30000 , icon="warning",title ='درخواست تغییر ، حذف یا تدوین به اتمام رسید!!!')
            return redirect('ListViewMostanadatDakheliChangeDoing')
        if(activitySelected.activity == 'barresiModir'):
            result = self.saveing(activitySelected , text = request.POST.get('description') or None ,  profileSender = profileSender , profileReciver = self.modirToseProfile , confirm = request.POST.get('submit') or None , titleText = activitySelected.get_activity_display , nextStep = 'tadvinSanad' ,  )
            
            if(result):
                sweetify.toast(self.request,timer=30000 , icon="success",title ='درخواست تغییر ، حذف یا تدوین توسط بررسی مدیر دفتر توسعه مدیریت و تحقیقات مورد تایید قرار گرفت!!!')
            else:
                sweetify.toast(self.request,timer=30000 , icon="warning",title ='درخواست تغییر ، حذف یا تدوین به اتمام رسید!!!')
            return redirect('ListViewMostanadatDakheliChangeDoing')
        if(activitySelected.activity == 'tadvinSanad'):
            if(request.FILES.get('document', False)):
                result = self.saveing(activitySelected , text = request.POST.get('description') or None ,  profileSender = profileSender , profileReciver = self.karshenasProfile , confirm = request.POST.get('submit') or None , titleText = activitySelected.get_activity_display , nextStep = 'isDelete' , file = request.FILES['document'] )
            else:
                result = self.saveing(activitySelected , text = request.POST.get('description') or None ,  profileSender = profileSender , profileReciver = self.karshenasProfile , confirm = request.POST.get('submit') or None , titleText = activitySelected.get_activity_display , nextStep = 'isDelete' , )
            
            
            if(result):
                sweetify.toast(self.request,timer=30000 , icon="success",title ='سند جدید تدوین شد !!!')
            else:
                sweetify.toast(self.request,timer=30000 , icon="warning",title ='درخواست تغییر ، حذف یا تدوین به اتمام رسید!!!')
            return redirect('ListViewMostanadatDakheliChangeDoing')
       
            
        if(activitySelected.activity == 'isDelete'):
            if request.POST.get('submit') == 'completed':
                activitySelected.status = 'completed'
                document = activitySelected.MostanadatDakheliChangeRelated.documentRelated
                document.outdated = True
                document.save()
                textBox = TextDataBase.objects.create(title = 'علت منسوخ شدن' , text = request.POST.get('description'))
                activitySelected.texts.add(textBox)
                activitySelected.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='سند  مورد نظر منسوخ شد !!!')
                result = False
            else:
                if(activitySelected.MostanadatDakheliChangeRelated.problem == 'create'):
                    result = self.saveing(activitySelected , text = request.POST.get('description') or None ,  profileSender = profileSender , profileReciver = self.karshenasProfile , confirm = 'yes' , titleText = activitySelected.get_activity_display , nextStep = 'newDoc'  )
                else:
                    result = self.saveing(activitySelected , text = request.POST.get('description') or None ,  profileSender = profileSender , profileReciver = self.karshenasProfile , confirm = 'yes' , titleText = activitySelected.get_activity_display , nextStep = 'editDoc'  )
            if(result):
                sweetify.toast(self.request,timer=30000 , icon="success",title ='سند جدید جهت تدوین و ویرایش آماده شده است !!!')
            if(result == False):
                sweetify.toast(self.request,timer=30000 , icon="warning",title ='درخواست تغییر ، حذف یا تدوین به اتمام رسید!!!')
            return redirect('ListViewMostanadatDakheliChangeDoing')
        
        if(activitySelected.activity == 'newDoc'):
            form = CreateFormMostanadatDakheli(request.POST,request.FILES)
            #بررسی صحت اطلاعات ورودی
            upload = request.FILES['document']
            typeFile = '.' + upload.name.split('.')[-1]
            fss = FileSystemStorage()
            file = fss.save( MEDIA_ROOT + '/mostanad/' +request.POST['dakheliSanadCode'] +typeFile  , upload, )
            activitySelected.status = 'completed'
            activitySelected.save()
            if form.is_valid():
                
                
                form.save()
                #تابع نمایش پیغام
                sweetify.toast(self.request,timer=30000 , icon="success",title ='مستند داخلی  جدید با موفقیت ساخته شد !!!')
                return redirect('MostanadatListViewDakheli')
            else :
                sweetify.toast(self.request,timer=30000 , icon="error",title ='مستند داخلی  مورد نظر ساخته نشد !')
            return redirect('ListViewMostanadatDakheliChangeDoing')
        if(activitySelected.activity == 'editDoc'):
            obj = self.get_obj(activitySelected)
            
            form = CreateFormMostanadatDakheli(request.POST,request.FILES ,instance=obj)
            #بررسی صحت اطلاعات ورودی
            if(request.FILES.get('document', False)):
                upload = request.FILES['document']
                typeFile = '.' + upload.name.split('.')[-1]
                fss = FileSystemStorage()
                file = fss.save( MEDIA_ROOT + '/mostanad/' +request.POST['dakheliSanadCode'] +typeFile  , upload, )
            activitySelected.status = 'completed'
            activitySelected.save()
            if form.is_valid():
                
                
                form.save()
                #تابع نمایش پیغام
                sweetify.toast(self.request,timer=30000 , icon="success",title ='مستند داخلی  جدید با موفقیت ساخته شد !!!')
                return redirect('MostanadatListViewDakheli')
            else :
                sweetify.toast(self.request,timer=30000 , icon="error",title ='مستند داخلی  مورد نظر ساخته نشد !')
            return redirect('ListViewMostanadatDakheliChangeDoing')
        context = {'extend':self.extend,'form': form }
        return render(request,self.template_name,context)





class CreateViewRecordChange( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "MostanadatDakheliChangeCreate.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    def get(self, request,recordId, *args, **kwargs):
        profileReciver = Profile.objects.filter(id=321)[0]
        profileSender  = Profile.objects.filter(user=self.request.user)[0]
        recordSelectedId = recordId
        recordSelected = RecordDataBase.objects.all().filter(id = recordSelectedId)[0]
        RecordChangeActivityManager.objects.create(sender =profileReciver ,reciver = profileSender ,status ='doing'  ,activity ='register'  ,RecordChangeRelated =recordSelected  )
        
        contex = {}
        return redirect('ListViewRecordChangeDoing')




class ListViewRecordChangeDoing(ListView):
  

    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست    تغییر ، حذف یا تدوین سند"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام درخواست تغییر ، حذف یا تدوین  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = [  'عنوان سابقه' , 'مرحله اقدام' , ]
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = MostanadatDakheliChange.objects.all()
        list_data = []
        userProfile = Profile.objects.filter(user=self.request.user)[0]
        
        queryset = RecordChangeActivityManager.objects.all().filter(status='doing').filter(reciver = userProfile)
        
        
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            
            data.append(query.RecordChangeRelated.title)
            data.append(query.get_activity_display)
         

   
            
 

         
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = { 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data ,'extend':self.extend , 'menu_link':self.menu_link}
        return context

    model = MostanadatDakheliChange
    ordering = '-created_at' 
    template_name ='recordChangeListStep.html'





class CreateViewRecordChangeStep( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "recordChangeCreateStep.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    def get_obj(self , activitySelected):
                id = activitySelected.RecordChangeRelated.id
                #id = self.kwargs.get('id')
                obj=None
                if id is not None:
                    obj = get_object_or_404(RecordDataBase,id = id)
                return obj
    def saveing(self ,activitySelected , text  , profileSender , profileReciver ,confirm , titleText  ,nextStep ,file=None ,nextFailStep=None  ):
        if(confirm =='yes'):
            
                
            recordSelected = activitySelected.RecordChangeRelated
            cdb = ConfirmationDataBase.objects.create( title =titleText ,profile =profileReciver  ,confirm =confirm ,text = text ) 
            activitySelected.confirmations=cdb
            activitySelected.status = 'done'
            instanceRecordActivityManager = RecordChangeActivityManager.objects.create(reciver = profileReciver , sender  = profileSender , activity = nextStep,previousActivity = activitySelected , RecordChangeRelated  =activitySelected.RecordChangeRelated)
            activitySelected.nextActivity = instanceRecordActivityManager
            activitySelected.save()
            instanceRecordActivityManager.save()
            return True
        elif(confirm =='completed'):
            activitySelected.status = 'completed'
            if  text != None:
                activitySelected.texts.add(text)
            activitySelected.save()
            return False
        elif(confirm =='delete'):
            activitySelected.status = 'delete'
            if  text != None:
                activitySelected.texts.add(text)
            activitySelected.save()
            return False
        else:
            cdb = ConfirmationDataBase.objects.create( title =titleText ,profile =profileReciver  ,confirm ='no' ,text = text ) 
            activitySelected.confirmations=cdb
            activitySelected.status = 'done'
            instanceRecordChangeActivityManager = RecordChangeActivityManager.objects.create(reciver = profileReciver , sender  = profileSender , activity = nextFailStep,previousActivity = activitySelected , RecordChangeRelated  =activitySelected.RecordChangeRelated)
            activitySelected.nextActivity = instanceRecordChangeActivityManager
            activitySelected.save()
            instanceRecordChangeActivityManager.save()
            
    def get(self, request, activityId,*args, **kwargs):
        form = CreateFormMostanadatDakheliChange()
        formMostanadatDakheli = CreateFormMostanadatDakheli()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = " درخواست تغییر در سابقه"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک درخواست تغییر ، حذف یا تدوین  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        texts = []
        boolians = []
        confirmation = ''
        fields = ''
        cause = ''
        profiles = ''
        definitionCorrectiveaAtion = ''
        profilesPosts = ''
        filedSelected = ''
        queryset = MostanadatDakheli.objects.all()
        
        activitySelected = RecordChangeActivityManager.objects.all().filter(id = activityId)[0]
        recordSelected = activitySelected.RecordChangeRelated
        firstActivity = activitySelected.firstStep()
        all = activitySelected.allActivityList()
        allVahed = Vahed.objects.all()
        allPostType  =  TypePostSazmani.objects.all()


        if(activitySelected.lastStep().activity == 'editRecord'):
            
            obj = self.get_obj(activitySelected)
            
            if obj is not None:
                formRecordDataBase = CreateFormRecordDataBase(instance=obj)
                
               
                
                contex = {'extend':self.extend , 'menu_link':self.menu_link,'form': form, 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name ,
                'columns' : columns , 'color' : color , 'activitySelected':activitySelected , 'texts' : texts,'boolians' : boolians,
                'confirmation' : confirmation ,  'fields' : fields ,'cause' :cause , 'profilesPosts':profilesPosts , 'definitionCorrectiveaAtion' : definitionCorrectiveaAtion , 'filedSelected' : filedSelected , 'all' : all , 'formMostanadatDakheli' : formMostanadatDakheli , 'obj':obj ,'allVahed':allVahed ,'allPostType':allPostType ,} 
                return render(request,self.template_name,contex)

        

        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menu_link':self.menu_link,'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'activitySelected':activitySelected , 'texts' : texts,'boolians' : boolians,
        'confirmation' : confirmation ,  'fields' : fields ,'cause' :cause , 'profilesPosts':profilesPosts , 'definitionCorrectiveaAtion' : definitionCorrectiveaAtion , 'filedSelected' : filedSelected , 'all' : all , 'formMostanadatDakheli' : formMostanadatDakheli , 'allVahed' :allVahed , 'allPostType' : allPostType  , 'recordSelected' : recordSelected } 
        return render(request,self.template_name,contex)


    def post(self, request,activityId , *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormRecordDataBase(request.POST,request.FILES)
        profileReciver = Profile.objects.filter(id=321)[0]
        profileSender  = Profile.objects.filter(user=self.request.user)[0]
        activitySelected = RecordChangeActivityManager.objects.all().filter(id = activityId)[0]
        
        if(activitySelected.activity == 'register'):
                result = self.saveing(activitySelected , text = request.POST.get('description') ,  profileSender = profileSender , profileReciver = profileReciver , confirm = request.POST.get('submit')  , titleText = 'دلایل تغییر در سابقه' , nextStep = 'barresiMafogh',nextFailStep = 'delete'  )
                if(result):
                    sweetify.toast(self.request,timer=30000 , icon="success",title ='درخواست تغییر در سابقه ثبت شد !!!')
                else:
                    sweetify.toast(self.request,timer=30000 , icon="warning",title ='درخواست تغییر تغییر در سابقه به اتمام رسید!!!')
                return redirect('ListViewRecordChangeDoing')
        if(activitySelected.activity == 'barresiMafogh'):
                result = self.saveing(activitySelected , text = request.POST.get('description') ,  profileSender = profileSender , profileReciver = profileReciver , confirm = request.POST.get('submit')  , titleText = 'توضیحات مافوق' , nextStep = 'barresiKarshenas',nextFailStep = 'delete'  )
                if(result):
                    sweetify.toast(self.request,timer=30000 , icon="success",title ='درخواست تغییر در سابقه ثبت شد !!!')
                else:
                    sweetify.toast(self.request,timer=30000 , icon="warning",title ='درخواست تغییر تغییر در سابقه به اتمام رسید!!!')
                return redirect('ListViewRecordChangeDoing')
        if(activitySelected.activity == 'barresiKarshenas'):
                result = self.saveing(activitySelected , text = request.POST.get('description') ,  profileSender = profileSender , profileReciver = profileReciver , confirm = request.POST.get('submit')  , titleText = 'توضیحات کارشناس' , nextStep = 'barresiModir',nextFailStep = 'barresiMafogh'  )
                if(result):
                    sweetify.toast(self.request,timer=30000 , icon="success",title ='درخواست تغییر در سابقه ثبت شد !!!')
                else:
                    sweetify.toast(self.request,timer=30000 , icon="warning",title ='درخواست تغییر تغییر در سابقه به اتمام رسید!!!')
                return redirect('ListViewRecordChangeDoing')
        
        if(activitySelected.activity == 'barresiModir'):
                result = self.saveing(activitySelected , text = request.POST.get('description') ,  profileSender = profileSender , profileReciver = profileReciver , confirm = request.POST.get('submit')  , titleText = 'توضیحات مدیر' , nextStep = 'editKarshenas',nextFailStep = 'delete'  )
                if(result):
                    sweetify.toast(self.request,timer=30000 , icon="success",title ='درخواست تغییر در سابقه ثبت شد !!!')
                else:
                    sweetify.toast(self.request,timer=30000 , icon="warning",title ='درخواست تغییر تغییر در سابقه به اتمام رسید!!!')
                return redirect('ListViewRecordChangeDoing')
        
        if(activitySelected.activity == 'editKarshenas'):
            obj = self.get_obj(activitySelected)
            
            form = CreateFormRecordDataBase(request.POST,request.FILES ,instance=obj)
            #بررسی صحت اطلاعات ورودی
            activitySelected.status = 'completed'
            activitySelected.save()
            if form.is_valid():
                
                
                form.save()
                #تابع نمایش پیغام
                sweetify.toast(self.request,timer=30000 , icon="success",title ='سابقه مورد نظر با موفقیت به روز شد !!!')
                return redirect('ViewRecordDataBase')
            else :
                sweetify.toast(self.request,timer=30000 , icon="error",title ='سابقه مورد نظر به روز نشد !')
            return redirect('ViewRecordChange')
        context = {'extend':self.extend,'form': form }
        return render(request,self.template_name,context)



class UpdateViewRecord( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
    def get_obj(self):

        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(RecordDataBase,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRecordDataBase(instance=obj)

            obj = get_object_or_404(RecordDataBase,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش مستند خارجی  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این مستند خارجی  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت
            icon_name     = "person_add"
            #تعداد ستون ها
            color         = "info"
            #رنگ
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)

    def post(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormMostanadatKhareji(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='مستند خارجی  جدید با موفقیت ساخته شد !!!')
                return redirect('MostanadatListViewKhareji')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='مستند خارجی  مورد نظر ساخته نشد !')
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewMostanadatDakheli( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MostanadatDakheli,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک مستند داخلی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که مستند داخلی   " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت
            icon_name     = "delete_forever"
            #تعداد ستون ها
            color         = "danger"
            #رنگ
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend':self.extend,'riskDabir':is_dabir(self) ,'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}

        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='مستند داخلی  با موفقیت پاک شد !!!')
            context={'extend':self.extend,'riskDabir':is_dabir(self)}
            return redirect('MostanadatListViewDakheli')
        return render(request,self.template_name,context)




class ViewRecordDashboard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "clearDashboard.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
   
    def get(self, request ,*args, **kwargs):
        userProfile = Profile.objects.get(user=self.request.user)
        allActivity = RecordChangeActivityManager.objects.all().filter(~Q(status = 'done'))
        allLenghtDo = len(allActivity.filter(Q(status='doing') ))
        partials = 'partials/recordDashboard.html'
        allRecord = RecordDataBase.objects.all()
        visio = 'مدیریت مستندات و سوابق.vsdx'
       
        allCreatedAction = {}
        allComplated = {}
        profileSelected = None
        responsibleCount = 0
        memberCount = 0
        createNewProfile = None
        allProfile=None
        if(request.user.is_superuser):
            activityNotDone = allActivity.filter(status='doing' )
        else:
            activityNotDone = allActivity.filter(Q(reciver = userProfile) & Q(status='doing') )
        
        responsible_link = None

        if(len(activityNotDone) >0):
            responsible_link = 'ListViewRecordChangeDoing'

        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست کنترل سوابق سیستم مدیریت یکپارچه"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        queryset = RecordDataBase.objects.all()

        
        #رنگ             
        columns       = 1
 
        
        #رنگ             
        columns       = 1
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack, 'header_title':header_title,'profileSelected':profileSelected,'createNewProfile':createNewProfile,
        'discribtion':discribtion,'icon_name':icon_name,'header_title':header_title,'responsible_link':responsible_link,
        'columns':columns , 'color':color ,'partials':partials, 'allProfile':allProfile , 'allLenghtDo':allLenghtDo, 'responsibleCount':responsibleCount,'memberCount':memberCount ,'allRecord':allRecord , 'visio':visio
        }

        return render(request,self.template_name,context)
    

    def post(self, request, *args, **kwargs):
        profileReciver = Profile.objects.filter(id=321)[0]
        profileSender  = Profile.objects.filter(user=self.request.user)[0]
        recordSelected = RecordDataBase.objects.get(id = request.POST.get('recordId'))
        
        activitySelected = RecordChangeActivityManager.objects.create(sender =profileReciver ,reciver = profileSender ,status ='doing'  ,activity ='register'  ,RecordChangeRelated =recordSelected  )
        
        cdb = ConfirmationDataBase.objects.create( title ='ثبت درخواست' ,profile =profileReciver  ,confirm =True ,text = request.POST.get('description')  ) 
        activitySelected.confirmations=cdb
        activitySelected.status = 'done'
        instanceRecordActivityManager = RecordChangeActivityManager.objects.create(reciver = profileReciver , sender  = profileSender , activity = 'barresiMafogh',previousActivity = activitySelected , RecordChangeRelated  =activitySelected.RecordChangeRelated)
        activitySelected.nextActivity = instanceRecordActivityManager
        activitySelected.save()
        instanceRecordActivityManager.save()

        return redirect('ListViewRecordChangeDoing')


class MostanadatKharejiHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "MostanadatKhareji.html"
    def get(self, request,*args, **kwargs):


        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewMostanadatKhareji( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد
    template_name = "create.html"
    extend = 'base.html'
    def get(self, request, *args, **kwargs):
        form = CreateFormMostanadatKhareji()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک مستند خارجی  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک مستند خارجی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ
        color         = "success"
        #دیکشنری داده ها
        contex = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormMostanadatKhareji(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='مستند خارجی  جدید با موفقیت ساخته شد !!!')
            return redirect('MostanadatListViewKhareji')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='مستند خارجی  مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewMostanadatKhareji(ListView):


    extend = 'baseEmployee.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست مستند خارجی  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام مستند خارجی  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = MostanadatKhareji.objects.all()
        queryset_filter = MostanadatDakheliFilter(self.request.GET, queryset=queryset)
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}

            data.append(query.title[:70])
            









            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table
          ,  'list_data' : list_data , "filter": queryset_filter ,}
        return context

    model = MostanadatKhareji
    ordering = '-created_at'
    template_name ='mostanadat_khareji_list.html'


class ViewMostanadatKhareji( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "viewmostanadatkhareji.html"
    extend = 'baseEmployee.html'
    def get_obj(self):

        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MostanadatKhareji,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = ViewFormMostanadatKhareji(instance=obj)

            obj = get_object_or_404(MostanadatKhareji,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش مستند داخلی  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت
            icon_name     = "person_add"
            #تعداد ستون ها
            color         = "info"

            try:
                sanadTitle         = obj.title
            except:
                sanadTitle = 'نامعلوم'
            try:
                sanadCode          = obj.kharejiSanadCode
            except:
                sanadCode = 'نامعلوم'
            try:
                ProcessMortabet    = obj.processCode.title
            except:
                ProcessMortabet = 'نامعلوم'
            try:
                versionNumber      = obj.versionNumber
            except:
                versionNumber = 'نامعلوم'
            try:
                refrenceName       = obj.refrenceName
            except:
                refrenceName = 'نامعلوم'
            
            try:
                expiredDate        = obj.expiredDate
            except:
                expiredDate = 'نامعلوم'
            try:
                postmasolUpdate    = obj.postmasolUpdate.title
            except:
                postmasolUpdate = 'نامعلوم'
            try:
                updatePeriod       = obj.updatePeriod
            except:
                updatePeriod = 'نامعلوم'
            try:
                tozihat            = obj.tozihat
            except:
                tozihat = 'نامعلوم'
            try:
                etebarDate         = obj.etebarDate
            except:
                etebarDate = 'نامعلوم'
            try:
                expireDate         = obj.expiredDate
            except:
                expireDate = 'نامعلوم'
            try:
                entesharDate = obj.entesharDate
            except:
                entesharDate = 'نامعلوم'
            try:
                govermentUpdate = obj.govermentUpdate
            except :
                govermentUpdate = 'نامعلوم'


            #رنگ
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns , 'sanadTitle' : sanadTitle, 'sanadCode' : sanadCode,'ProcessMortabet' : ProcessMortabet , 'versionNumber' : versionNumber, 'refrenceName' : refrenceName,'expiredDate' : expiredDate ,'postmasolUpdate' : postmasolUpdate ,'updatePeriod' : updatePeriod , 'tozihat' : tozihat,'etebarDate' : etebarDate ,'expireDate' : expireDate  , 'entesharDate':entesharDate , 'govermentUpdate':govermentUpdate }


        return render(request,self.template_name,context)


class UpdateViewMostanadatKhareji( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
    def get_obj(self):

        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MostanadatKhareji,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormMostanadatKhareji(instance=obj)

            obj = get_object_or_404(MostanadatKhareji,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش مستند خارجی  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این مستند خارجی  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت
            icon_name     = "person_add"
            #تعداد ستون ها
            color         = "info"
            #رنگ
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)

    def post(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormMostanadatKhareji(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='مستند خارجی  جدید با موفقیت ساخته شد !!!')
                return redirect('MostanadatListViewKhareji')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='مستند خارجی  مورد نظر ساخته نشد !')
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewMostanadatKhareji( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(MostanadatKhareji,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک مستند خارجی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که مستند خارجی   " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت
            icon_name     = "delete_forever"
            #تعداد ستون ها
            color         = "danger"
            #رنگ
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend':self.extend,'riskDabir':is_dabir(self),'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}

        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='مستند خارجی  با موفقیت پاک شد !!!')
            context={'extend':self.extend,'riskDabir':is_dabir(self)}
            return redirect('MostanadatListViewKhareji')
        return render(request,self.template_name,context)





class ViewRecordDataBase(ListView):
  

    extend = 'baseEmployee.html'
    menu_link = 'ViewMomayezi'
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "listRecordDataBase.html"
    

     
    def get(self, request, *args, **kwargs):
        
        
        
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
        header_table   = ['زمان ممیزی' , 'واحد' , 'ساعت' ,'ساعت پایان', 'تیم' ,'سیستم' , 'بند', ' ']
        #اسم داده های جدول
        
     
        #دریافت تمام داده ها
        queryset = RecordDataBase.objects.all()
       
        
       
       
        
            
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menu_link':self.menu_link, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          , 'queryset':queryset}
        
        return render(request,self.template_name,context)

 

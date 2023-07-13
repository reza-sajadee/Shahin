from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CreateFormRade ,   CreateFormIndexMahaleKhedmat 
from .models import Rade,Hoze,Bakhsh,Daste,SatheVahed,TypePostSazmani,Vahed , SathPost  ,IndexMahaleKhedmat , JobBank , Post , PostDescription
from .forms import CreateFormRade , CreateFormDaste, CreateFormHoze, CreateFormSatheVahed,CreateFormTypePostSazmani , CreateFormBakhsh, CreateFormVahed , CreateFormSathPost , CreateFormJobBank, CreateFormPost
from django.views.generic import ListView
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from risk_app.utils import is_dabir
from django.http import JsonResponse
from .serializers import OrgSerializer ,JobSerializer
###############
def load_Job(request):
    qs_val = list(JobBank.objects.all())
    
    serializer = JobSerializer(qs_val , many=True)
    return JsonResponse( serializer.data,safe=False)
class ChartMapH( LoginRequiredMixin,View):
    template_name = "chartH.html"
    redirect_field_name = '/profile/login'
    def get(self, request,*args, **kwargs):
        allJob = JobBank.objects.all()
        x = []
        for job in allJob:
            try:
                x.append({'name':job.jobBankPost.title , 'id':job.jobBankPost.id , 'parentId':job.jobBankPost.postMafogh.id , })
            except:
                continue
        y = json.dumps(x[:10])
       
        return render(request,self.template_name , {'y' : y})

class ChartMap( LoginRequiredMixin,View):
    template_name = "chartMap.html"
    redirect_field_name = '/profile/login'
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


class ChartSelectedMap( LoginRequiredMixin,View):
    template_name = "chartSelectedMap.html"
    redirect_field_name = '/profile/login'
    def get(self, request,*args, **kwargs):
        selected =  request.GET.get('id') + '.jpg'
        contex= {'selected':selected , 'title' : selected[:-4]}
        return render(request,self.template_name , contex)


class HozeHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "Hoze.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewHoze( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormHoze()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک حوزه سازمانی جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک حوزه سازمانی جدید ، موارد خواسته شده را تکمیل نمایید"
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
        form = CreateFormHoze(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='حوزه سازمانی جدید با موفقیت ساخته شد !!!')
            return redirect('OrganizationListViewHoze')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='حوزه سازمانی مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewHoze(ListView):
  


    extend='base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست حوزه سازمانی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام حوزه سازمانی ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
    
        
        header_table   = ['عنوان','کد حوزه سازمانی']
        #اسم داده های جدول
        object_name    = ['title','hoze']
        #دریافت تمام داده ها
        queryset = Hoze.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.hozeCode)
            
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data }
        return context

    model = Hoze
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewHoze( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend='base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Hoze,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormHoze(instance=obj)
            
            obj = get_object_or_404(Hoze,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش حوزه سازمانی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این حوزه سازمانی ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self) ,'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormHoze(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='حوزه سازمانی جدید با موفقیت ساخته شد !!!')
                return redirect('OrganizationListViewHoze')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='حوزه سازمانی مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewHoze( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend = 'base.html'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Hoze,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک حوزه سازمانی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که حوزه سازمانی  " + obj.title + " "  + " را پاک کنید   ؟"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='حوزه سازمانی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('OrganizationListViewHoze')
        return render(request,self.template_name,context)
    
    




###############



class RadeHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "Rade.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewRade( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormRade()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک رده سازمانی جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک رده سازمانی جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #دیکشنری داده ها
        contex = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormRade(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='رده سازمانی جدید با موفقیت ساخته شد !!!')
            return redirect('OrganizationListViewRade')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='رده سازمانی مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewRade(ListView):
  


    extend='base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست رده سازمانی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام رده سازمانی ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
        
        
        header_table   = ['عنوان','کد رده سازمانی']
        #اسم داده های جدول
        object_name    = ['title','radeCode']
        #دریافت تمام داده ها
        queryset = Rade.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.radeCode)
          
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data }
        return context

    model = Rade
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewRade( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend='base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Rade,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRade(instance=obj)
            
            obj = get_object_or_404(Rade,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش رده سازمانی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این رده سازمانی ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self) ,'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormRade(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='رده سازمانی جدید با موفقیت ساخته شد !!!')
                return redirect('OrganizationListViewRade')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='رده سازمانی مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewRade( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend = 'base.html'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Rade,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک رده سازمانی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که رده سازمانی  " + obj.title + " "  + " را پاک کنید   ؟"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='رده سازمانی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('OrganizationListViewRade')
        return render(request,self.template_name,context)
    
    




###############

class DasteHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "Daste.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewDaste( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormDaste()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک دسته سازمانی جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک دسته سازمانی جدید ، موارد خواسته شده را تکمیل نمایید"
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
        form = CreateFormDaste(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='دسته سازمانی جدید با موفقیت ساخته شد !!!')
            return redirect('OrganizationListViewDaste')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='دسته سازمانی مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewDaste(ListView):
  


    extend='base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست دسته سازمانی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این گروه لیست تمام دسته سازمانی ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        
       
        
        #عنوان های جدول
        header_table   = ['عنوان','کد دسته سازمانی','کد بخش سازمانی','عنوان بخش سازمانی']
        #اسم داده های جدول
        #object_name    = ['title','processCode','processAreaCode.processAreaCode','processAreaCode.title','created_at','updated_at']
        #دریافت تمام داده ها
        queryset = Daste.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.dasteCode)
            data.append(query.bakhsh.bakhshCode)
            
            data.append(query.bakhsh.title)

            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
        'list_data' : list_data }
        return context

    model = Daste
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewDaste( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend='base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Daste,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormDaste(instance=obj)
            
            obj = get_object_or_404(Daste,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش دسته سازمانی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این دسته سازمانی ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self) ,'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormDaste(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='دسته سازمانی جدید با موفقیت ساخته شد !!!')
                return redirect('OrganizationListViewDaste')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='دسته سازمانی مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewDaste( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend = 'base.html'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Daste,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک دسته سازمانی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که دسته سازمانی  " + obj.title + " "  + " را پاک کنید   ؟"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='دسته سازمانی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('OrganizationListViewDaste')
        return render(request,self.template_name,context)
    
    
###############################



class BakhshHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "Bakhsh.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewBakhsh( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormBakhsh()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک بخش سازمانی جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک بخش سازمانی جدید ، موارد خواسته شده را تکمیل نمایید"
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
        form = CreateFormBakhsh(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='بخش سازمانی جدید با موفقیت ساخته شد !!!')
            return redirect('OrganizationListViewBakhsh')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='بخش سازمانی مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewBakhsh(ListView):
  


    extend='base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست بخش سازمانی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این گروه لیست تمام بخش سازمانی ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
      
        
        header_table   = ['عنوان','کد بخش سازمانی','کد حوزه سازمانی','عنوان حوزه سازمانی']
        #اسم داده های جدول
        #object_name    = ['title','processCode','processAreaCode.processAreaCode','processAreaCode.title','created_at','updated_at']
        #دریافت تمام داده ها
        queryset = Bakhsh.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.bakhshCode)
            data.append(query.hoze.hozeCode)
            data.append(query.hoze.title)

            
    
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
        'list_data' : list_data }
        return context

    model = Bakhsh
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewBakhsh( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend='base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Bakhsh,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormBakhsh(instance=obj)
            
            obj = get_object_or_404(Bakhsh,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش بخش سازمانی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این بخش سازمانی ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self) ,'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormBakhsh(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='بخش سازمانی جدید با موفقیت ساخته شد !!!')
                return redirect('OrganizationListViewBakhsh')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='بخش سازمانی مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewBakhsh( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend = 'base.html'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Bakhsh,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک بخش سازمانی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که بخش سازمانی  " + obj.title + " "  + " را پاک کنید   ؟"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='بخش سازمانی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('OrganizationListViewBakhsh')
        return render(request,self.template_name,context)
    
    




###################


class VahedHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "Vahed.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewVahed( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormVahed()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک واحد سازمان  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک واحد سازمان  جدید ، موارد خواسته شده را تکمیل نمایید"
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
        form = CreateFormVahed(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='واحد سازمان  جدید با موفقیت ساخته شد !!!')
            return redirect('OrganizationListViewVahed')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='واحد سازمان  مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewVahed(ListView):
  


    extend='base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست واحد سازمان  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام واحد سازمان  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
       
        
        header_table   = ['عنوان','کد واحد سازمانی','سطح واحد','پست سازمانی مسئول واحد','کد پست سازمانی (مسئول واحد)','واحد سازمانی مافوق',
                          'کد واحد سازمانی مافوق','دسته سازمانی ', 'کد دسته  سازمانی' , 'بخش سازمانی' , 'کد بخش سازمانی' , 'حوزه سازمانی' , 'کد حوزه سازمانی']
        #اسم داده های جدول
        
        #دریافت تمام داده ها
        queryset = Vahed.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.vahedCode())
            data.append(query.satheVahed)
            data.append(query.typePostSazmani.title)
            data.append(query.typePostSazmani.typePostSazmaniCode)
            data.append(query.vahedMafogh.title or None)
            data.append(query.vahedMafogh.vahedCode())
            if(query.daste !=None):
                data.append(query.daste.title)
                data.append(query.daste.dasteCode)
            else:
                data.append("")
                data.append("")
            if(query.bakhsh !=None):
                data.append(query.bakhsh.title)
                data.append(query.bakhsh.bakhshCode)
            else:
                data.append("")
                data.append("")
            
            
            
            data.append(query.hoze.title)
            data.append(query.hoze.hozeCode)
         
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data }
        return context

    model = Vahed
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewVahed( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend='base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Vahed,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormVahed(instance=obj)
            
            obj = get_object_or_404(Vahed,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش واحد سازمان  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این واحد سازمان  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self) ,'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormVahed(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='واحد سازمان  جدید با موفقیت ساخته شد !!!')
                return redirect('OrganizationListViewVahed')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='واحد سازمان  مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewVahed( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend = 'base.html'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Vahed,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک واحد سازمان "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که واحد سازمان   " + obj.title + " "  + " را پاک کنید   ؟"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='واحد سازمان  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('OrganizationListViewVahed')
        return render(request,self.template_name,context)
    
    



###################


class SatheVahedHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "SatheVahed.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewSatheVahed( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormSatheVahed()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک سطح واحد سازمانی جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک سطح واحد سازمانی جدید ، موارد خواسته شده را تکمیل نمایید"
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
        form = CreateFormSatheVahed(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='سطح واحد سازمانی جدید با موفقیت ساخته شد !!!')
            return redirect('OrganizationListViewSatheVahed')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='سطح واحد سازمانی مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewSatheVahed(ListView):
  


    extend='base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست سطح واحد سازمانی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام سطح واحد سازمانی ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
      
        
        header_table   = ['عنوان','کد سطح واحد سازمانی']
        #اسم داده های جدول
        object_name    = ['title','satheVahedCode']
        #دریافت تمام داده ها
        queryset = SatheVahed.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.satheVahedCode)
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data }
        return context

    model = SatheVahed
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewSatheVahed( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend='base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(SatheVahed,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormSatheVahed(instance=obj)
            
            obj = get_object_or_404(SatheVahed,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش سطح واحد سازمانی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این سطح واحد سازمانی ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self) ,'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormSatheVahed(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='سطح واحد سازمانی جدید با موفقیت ساخته شد !!!')
                return redirect('OrganizationListViewSatheVahed')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='سطح واحد سازمانی مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewSatheVahed( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend = 'base.html'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(SatheVahed,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک سطح واحد سازمانی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که سطح واحد سازمانی  " + obj.title + " "  + " را پاک کنید   ؟"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='سطح واحد سازمانی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('OrganizationListViewSatheVahed')
        return render(request,self.template_name,context)
    
    




####################



class TypePostSazmaniHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "TypePostSazmani.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewTypePostSazmani( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormTypePostSazmani()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک نوع پست سازمانی جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع پست سازمانی جدید ، موارد خواسته شده را تکمیل نمایید"
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
        form = CreateFormTypePostSazmani(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='نوع پست سازمانی جدید با موفقیت ساخته شد !!!')
            return redirect('OrganizationListViewTypePostSazmani')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='نوع پست سازمانی مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewTypePostSazmaniClient(ListView):
  


    extend='baseEmployee.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست نوع پست سازمانی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوع پست سازمانی ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
       
        
        header_table   = ['عنوان','کد نوع پست سازمانی']
        #اسم داده های جدول
        object_name    = ['title','sathPostCode']
        allPostDescription = PostDescription.objects.all()
        #دریافت تمام داده ها
        queryset = TypePostSazmani.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.typePostSazmaniCode)
            data.append(allPostDescription.filter(typePostRelated = query).first())
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        list_data=list_data[1:]
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data}
        return context

    model = TypePostSazmani
    ordering = '-created_at' 
    template_name ='listPost.html'

class ListViewTypePostSazmani(ListView):
  


    extend='base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست نوع پست سازمانی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوع پست سازمانی ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
       
        
        header_table   = ['عنوان','کد نوع پست سازمانی']
        #اسم داده های جدول
        object_name    = ['title','sathPostCode']
        #دریافت تمام داده ها
        queryset = TypePostSazmani.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.typePostSazmaniCode)
            
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data}
        return context

    model = TypePostSazmani
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewTypePostSazmani( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend='base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(TypePostSazmani,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormTypePostSazmani(instance=obj)
            
            obj = get_object_or_404(TypePostSazmani,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش نوع پست سازمانی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این نوع پست سازمانی ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self) ,'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormTypePostSazmani(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='نوع پست سازمانی جدید با موفقیت ساخته شد !!!')
                return redirect('OrganizationListViewTypePostSazmani')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='نوع پست سازمانی مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)


class ViewTypePostSazmani( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "viewPostDescription.html"
    extend='baseEmployee.html'
   
    def get(self, request,postId=None ,*args, **kwargs):
        typePostSelected = TypePostSazmani.objects.get(id = postId)
        PostDescriptionSelected = PostDescription.objects.filter(typePostRelated  = postId).first()
        allPost = Post.objects.all().filter(PostTypePostSazmani = typePostSelected)
        #allPersonels = JobBank.objects.all().filter(jobBankPost = postRelated)
        
        
    
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ویرایش نوع پست سازمانی "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این نوع پست سازمانی ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        #رنگ             
        columns       = 1
        #دیکشنری داده ها
        context =  {'extend':self.extend  , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns , 'PostDescriptionSelected' :PostDescriptionSelected  , 'allPost' :allPost}


        return render(request,self.template_name,context)
    
        sweetify.toast(self.request,timer=30000 , icon="warning",title ='      شرح شغل موجود نیست !!!')
        #context['object']=None
        return redirect(self.request.META.get('HTTP_REFERER'))
            
            
            


class DeleteViewTypePostSazmani( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend = 'base.html'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(TypePostSazmani,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک نوع پست سازمانی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که نوع پست سازمانی  " + obj.title + " "  + " را پاک کنید   ؟"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='نوع پست سازمانی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('OrganizationListViewTypePostSazmani')
        return render(request,self.template_name,context)
    
    

#####################


class SathPostHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "SathPost.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewSathPost( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormSathPost()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک نوع پست سازمانی جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نوع پست سازمانی جدید ، موارد خواسته شده را تکمیل نمایید"
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
        form = CreateFormSathPost(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='نوع پست سازمانی جدید با موفقیت ساخته شد !!!')
            return redirect('OrganizationListViewSathPost')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='نوع پست سازمانی مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewSathPost(ListView):
  


    extend='base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست نوع پست سازمانی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نوع پست سازمانی ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
      
        
        header_table   = ['عنوان','کد نوع پست سازمانی']
        #اسم داده های جدول
        object_name    = ['title','sathPostCode']
        #دریافت تمام داده ها
        queryset = SathPost.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.sathPostCode)
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data }
        return context

    model = SathPost
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewSathPost( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend='base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(SathPost,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormSathPost(instance=obj)
            
            obj = get_object_or_404(SathPost,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش نوع پست سازمانی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این نوع پست سازمانی ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self) ,'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormSathPost(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='نوع پست سازمانی جدید با موفقیت ساخته شد !!!')
                return redirect('OrganizationListViewSathPost')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='نوع پست سازمانی مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewSathPost( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend = 'base.html'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(SathPost,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک نوع پست سازمانی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که نوع پست سازمانی  " + obj.title + " "  + " را پاک کنید   ؟"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='نوع پست سازمانی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('OrganizationListViewSathPost')
        return render(request,self.template_name,context)
    
    


######################






class IndexMahaleKhedmatHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "IndexMahaleKhedmat.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewIndexMahaleKhedmat( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormIndexMahaleKhedmat()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک   ایندکس محل خدمت "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک ایندکس محل خدمت ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #دیکشنری داده ها
        contex = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormIndexMahaleKhedmat(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='ایندکس محل خدمت با موفقیت ساخته شد !!!')
            return redirect('OrganizationListViewIndexMahaleKhedmat')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title =' ایندکس محل خدمت مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewIndexMahaleKhedmat(ListView):
  


    extend='base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست   ایندکس محل خدمت"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام   ایندکس محل خدمت را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
        
        
        header_table   = ['عنوان','کد ایندکس محل خدمت']
        #اسم داده های جدول
        object_name    = ['title','indexCode']
        #دریافت تمام داده ها
        queryset = IndexMahaleKhedmat.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.indexCode)
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data }
        return context

    model = IndexMahaleKhedmat
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewIndexMahaleKhedmat( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend='base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(IndexMahaleKhedmat,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormIndexMahaleKhedmat(instance=obj)
            
            obj = get_object_or_404(IndexMahaleKhedmat,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش  ایندکس محل خدمت "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این  ایندکس محل خدمت ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self) ,'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormIndexMahaleKhedmat(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='ایندکس محل خدمت با موفقیت ساخته شد !!!')
                return redirect('OrganizationListViewIndexMahaleKhedmat')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='ایندکس محل خدمت  مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewIndexMahaleKhedmat( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend = 'base.html'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(IndexMahaleKhedmat,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک ایندکس محل خدمت"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که  ایندکس محل حدمت  " + obj.title + " "  + " را پاک کنید   ؟"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('OrganizationListViewIndexMahaleKhedmat')
        return render(request,self.template_name,context)
    
    


################# بانک مشاغل


class JobBankHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "JobBank.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewJobBank( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormJobBank()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "افزودن یک شغل به بانک مشاغل "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت افزودن  یک شغل به بانک مشاغل ، موارد خواسته شده را تکمیل نمایید"
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
        form = CreateFormJobBank(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='یک شغل به بانک مشاغل افزوده شد !!!')
            return redirect('OrganizationListViewJobBank')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='شغل به بانک مشاغل افزوده نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewJobBank(ListView):
  


    extend='base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "بانک مشاغل"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام شغل ها را در بانک مشاغل  مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
       
        
        header_table   = ['کد پرسنلی' , 'نام' ,'نام خانوادگی',' کد واحد','نام واحد','کد واحد مافوق'  , 'نام واحد مافوق','کد نوع پست سازمانی' , 'نام نوع پست سازمانی ' , ' کد نوع پست سازمانی مافوق ' , 'نام نوع پست سازمانی مافوق']
        #اسم داده های جدول
        object_name    = ['vahed','profile', 'counter']
        #دریافت تمام داده ها
        queryset = JobBank.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            
            if(query.profile != None):
                try:
                    data.append(query.jobBankPost.codePostSazmani())
                except:
                    data.append('None')
                
                data.append(query.profile.firstName)
                data.append(query.profile.lastName)
            else:
                data.append('None')
                data.append('None')
                data.append('None')
            try:
                data.append(query.jobBankPost.vahed.vahedCode())
                data.append(query.jobBankPost.vahed.title)
            except:
                data.append('None')
                data.append('None')
            
            try:
                data.append(query.jobBankPost.vahed.vahedMafogh.vahedCode())
                data.append(query.jobBankPost.vahed.vahedMafogh.title)
                
            except:
                data.append('None')
                data.append('None')
            try:
                data.append(query.jobBankPost.PostTypePostSazmani.typePostSazmaniCode)
                data.append(query.jobBankPost.PostTypePostSazmani.title)
            except:
                data.append('None')
                data.append('None')
            try:
                data.append(query.jobBankPost.typePostSazmaniMafogh.typePostSazmaniCode)
            except:
                data.append('')
            try:
                data.append(query.jobBankPost.typePostSazmaniMafogh.title)
            except:
                data.append('')
            
            
            

 
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data}
        return context

    model = JobBank
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewJobBank( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend='base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(JobBank,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormJobBank(instance=obj)
            
            obj = get_object_or_404(JobBank,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش نوع پست سازمانی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این نوع پست سازمانی ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self) ,'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormJobBank(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='نوع پست سازمانی جدید با موفقیت ساخته شد !!!')
                return redirect('OrganizationListViewJobBank')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='نوع پست سازمانی مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewJobBank( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend = 'base.html'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(JobBank,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک نوع پست سازمانی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که نوع پست سازمانی  " + str(obj.profile) + " "  + " را پاک کنید   ؟"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='نوع پست سازمانی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('OrganizationListViewJobBank')
        return render(request,self.template_name,context)
    
    
##################### چارت پست سازمانی

class PostHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "Post.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewPost( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormPost()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک پست سازمان  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک پست سازمان  جدید ، موارد خواسته شده را تکمیل نمایید"
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
        form = CreateFormPost(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='پست سازمان  جدید با موفقیت ساخته شد !!!')
            return redirect('OrganizationListViewPost')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='پست سازمان  مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewPost(ListView):
  


    extend='base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست پست سازمان  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام پست سازمان  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
       
        
        header_table   = ['عنوان','کد پست سازمانی', 'کد واحد سازمانی ','id' ]
        #اسم داده های جدول
        
        #دریافت تمام داده ها
        queryset = Post.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.vahed.vahedCode() + str(query.PostTypePostSazmani))
            

            data.append(query.vahed.vahedCode())
            
            data.append(query.id)
         
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data }
        return context

    model = Post
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewPost( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend='base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Post,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormPost(instance=obj)
            
            obj = get_object_or_404(Post,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش پست سازمان  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این پست سازمان  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':is_dabir(self) ,'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormPost(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='پست سازمان  جدید با موفقیت ساخته شد !!!')
                return redirect('OrganizationListViewPost')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='پست سازمان  مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)

class DeleteViewPost( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend = 'base.html'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Post,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک پست سازمان "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که پست سازمان   " + obj.title + " "  + " را پاک کنید   ؟"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='پست سازمان  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('OrganizationListViewPost')
        return render(request,self.template_name,context)
    
    

from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CreateFormPositionNameList
from .models import PositionNameList 

from django.views.generic import ListView
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.mixins import LoginRequiredMixin


class PositionNameListHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "PositionNameList.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewPositionNameList( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    
    def get(self, request, *args, **kwargs):
        form = CreateFormPositionNameList()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک نام پست سازمانی جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک نام پست سازمانی جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex = {'extend':'base.html','form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormPositionNameList(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='نام پست سازمانی جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewPositionNameList')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='نام پست سازمانی مورد نظر ساخته نشد !')
        context = {'extend':'base.html','form': form}
        return render(request,self.template_name,context)


class ListViewPositionNameList(ListView):
  


    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست نام پست سازمانی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام نام پست سازمانی ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #عنوان های جدول
        header_table   = ['عنوان','کد نام پست سازمانی']
        #اسم داده های جدول
        object_name    = ['title','positionNameCode']
        #دریافت تمام داده ها
        queryset = PositionNameList.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.positionNameCode)
            
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':'base.html', 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data}
        return context

    model = PositionNameList
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewPositionNameList( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(PositionNameList,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormPositionNameList(instance=obj)
            
            obj = get_object_or_404(PositionNameList,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش نام پست سازمانی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این نام پست سازمانی ، موارد جدید را وارد کنید"
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
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':'base.html',}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormPositionNameList(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='نام پست سازمانی جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewPositionNameList')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='نام پست سازمانی مورد نظر ساخته نشد !')           
            context = {'extend':'base.html','form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewPositionNameList( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(PositionNameList,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک نام پست سازمانی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که نام پست سازمانی  " + obj.title + " "  + " را پاک کنید   ؟"
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
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':'base.html',}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='نام پست سازمانی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ListViewPositionNameList')
        return render(request,self.template_name,context)
    
    


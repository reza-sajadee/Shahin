from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CreateFormNahiye ,CreateFormGroup , CreateFormProcess,CreateFormHoze , CreateFormProcessDocument ,CreateFormProcessDescription
from .models import Nahiye , Hoze , Group  ,Process , ProcessDocument , ProcessDescription , ProcessFrom,ProcessTo

from django.views.generic import ListView
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from risk_app.utils import is_dabir

from profile_app.decorators import  staff_only




class ProcessMap( LoginRequiredMixin,View):
    template_name = "processmap.html"
    redirect_field_name = '/profile/login'
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#############



class NahiyeHome( LoginRequiredMixin,View):
    template_name = "Nahiye.html"
    redirect_field_name = '/profile/login'
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)





#کلاس ایجاد رکورد جدید
class CreateViewNahiye( LoginRequiredMixin,View):
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    redirect_field_name = '/profile/login'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormNahiye()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک ناحیه فرآیندی جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک ناحیه فرآیندی جدید ، موارد خواسته شده را تکمیل نمایید"
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
        form = CreateFormNahiye(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='ناحیه فرآیندی جدید با موفقیت ساخته شد !!!')
            return redirect('ProcessListViewNahiye')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='ناحیه فرآیندی مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewNahiye(ListView):
  
    redirect_field_name = '/profile/login'

    extend = 'base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست ناحیه فرآیندی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام ناحیه فرآیندی ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان','کد ناحیه فرآیندی']
        #اسم داده های جدول
        object_name    = ['title','nahiyeCode']
        #دریافت تمام داده ها
        queryset = Nahiye.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.nahiyeCode)
            
        
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data}
        return context

    model = Nahiye
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewNahiye( LoginRequiredMixin,View):
    template_name = "create.html"
    extend='base.html'
    redirect_field_name = '/profile/login'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Nahiye,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormNahiye(instance=obj)
            
            obj = get_object_or_404(Nahiye,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش ناحیه فرآیندی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این ناحیه فرآیندی ، موارد جدید را وارد کنید"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormNahiye(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='ناحیه فرآیندی جدید با موفقیت ساخته شد !!!')
                return redirect('ProcessListViewNahiye')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='ناحیه فرآیندی مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewNahiye( LoginRequiredMixin,View):
    
    extend = 'base.html'
    template_name = "delete.html"
    redirect_field_name = '/profile/login'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Nahiye,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک ناحیه فرآیندی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که ناحیه فرآیندی  " + obj.title + " "  + " را پاک کنید   ؟"
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
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='ناحیه فرآیندی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ProcessListViewNahiye')
        return render(request,self.template_name,context)
    
    




#############

class GroupHome( LoginRequiredMixin,View):
    template_name = "Group.html"
    redirect_field_name = '/profile/login'
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewGroup( LoginRequiredMixin,View):
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    redirect_field_name = '/profile/login'
    def get(self, request, *args, **kwargs):
        form = CreateFormGroup()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک فرآیند جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک فرآیند جدید ، موارد خواسته شده را تکمیل نمایید"
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
        form = CreateFormGroup(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='فرآیند جدید با موفقیت ساخته شد !!!')
            return redirect('ProcessListViewGroup')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='فرآیند مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewGroup(ListView):
  


    extend = 'base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست فرآیند ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این گروه لیست تمام فرآیند ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان','کد حوزه فرآیندی','کد ناحیه فرآیندی','عنوان ناحیه فرآیندی']
        #اسم داده های جدول
        #object_name    = ['title','processCode','nahiyeCodeCode.nahiyeCodeCode','nahiyeCodeCode.title','created_at','updated_at']
        #دریافت تمام داده ها
        queryset = Group.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.groupCode)
            data.append(query.hozeCode.hozeCode)
            data.append(query.hozeCode.title)

            
       
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
        'list_data' : list_data}
        return context

    model = Group
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewGroup( LoginRequiredMixin,View):
    template_name = "create.html"
    extend='base.html'
    redirect_field_name = '/profile/login'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Group,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormGroup(instance=obj)
            
            obj = get_object_or_404(Group,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش فرآیند "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این فرآیند ، موارد جدید را وارد کنید"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormGroup(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='فرآیند جدید با موفقیت ساخته شد !!!')
                return redirect('ProcessListViewGroup')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='فرآیند مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewGroup( LoginRequiredMixin,View):
    
    extend = 'base.html'
    template_name = "delete.html"
    redirect_field_name = '/profile/login'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Group,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک فرآیند"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که فرآیند  " + obj.title + " "  + " را پاک کنید   ؟"
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
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='فرآیند با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ProcessListViewGroup')
        return render(request,self.template_name,context)
    
    



#############


class ProcessHome( LoginRequiredMixin,View):
    template_name = "Process.html"
    redirect_field_name = '/profile/login'
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewProcess( LoginRequiredMixin,View):
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    redirect_field_name = '/profile/login'
    def get(self, request, *args, **kwargs):
        form = CreateFormProcess()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک گروه فرآیندی جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک گروه فرآیندی جدید ، موارد خواسته شده را تکمیل نمایید"
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
        form = CreateFormProcess(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='گروه فرآیندی جدید با موفقیت ساخته شد !!!')
            return redirect('ProcessListViewProcess')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='گروه فرآیندی مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewProcess(ListView):
  


    extend = 'baseEmployee.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست  فرآیندی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این گروه لیست تمام گروه فرآیندی ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان','کد فرآیند',' گروه فرآیندی' , 'مالک فرآیند']
        #اسم داده های جدول
        #object_name    = ['title','processCode','nahiyeCodeCode.nahiyeCodeCode','nahiyeCodeCode.title','created_at','updated_at']
        #دریافت تمام داده ها
        queryset = Process.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
        'list_data' : queryset}
        return context

    model = Process
    ordering = '-created_at' 
    template_name ='listViewProcess.html'

class UpdateViewProcess( LoginRequiredMixin,View):
    template_name = "create.html"
    extend='base.html'
    redirect_field_name = '/profile/login'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Process,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormProcess(instance=obj)
            
            obj = get_object_or_404(Process,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش گروه فرآیندی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این گروه فرآیندی ، موارد جدید را وارد کنید"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormProcess(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='گروه فرآیندی جدید با موفقیت ساخته شد !!!')
                return redirect('ProcessListViewProcess')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='گروه فرآیندی مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewProcess( LoginRequiredMixin,View):
    
    extend = 'base.html'
    template_name = "delete.html"
    redirect_field_name = '/profile/login'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Process,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک گروه فرآیندی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که گروه فرآیندی  " + obj.title + " "  + " را پاک کنید   ؟"
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
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='گروه فرآیندی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ProcessListViewProcess')
        return render(request,self.template_name,context)
    
    



#############



class HozeHome( LoginRequiredMixin,View):
    template_name = "Hoze.html"
    redirect_field_name = '/profile/login'
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewHoze( LoginRequiredMixin,View):
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    redirect_field_name = '/profile/login'
    def get(self, request, *args, **kwargs):
        form = CreateFormHoze()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک بخش فرآیندی جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک بخش فرآیندی جدید ، موارد خواسته شده را تکمیل نمایید"
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
            sweetify.toast(self.request,timer=30000 , icon="success",title ='بخش فرآیندی جدید با موفقیت ساخته شد !!!')
            return redirect('ProcessListViewHoze')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='بخش فرآیندی مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewHoze(ListView):
  


    extend = 'base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست بخش فرآیندی ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام بخش فرآیندی ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان','کد حوزه فرآیندی','کد ناحیه فرآیندی','عنوان ناحیه فرآیندی']
        #اسم داده های جدول
        #object_name    = ['title','hozeCode','nahiyeCodeCode.nahiyeCodeCode','nahiyeCodeCode.title','created_at','updated_at']
        #دریافت تمام داده ها
        queryset = Hoze.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.hozeCode)
            data.append(query.nahiyeCode)
            data.append(query.nahiyeCode.title)

            

            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
        'list_data' : list_data}
        return context

    model = Hoze
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewHoze( LoginRequiredMixin,View):
    template_name = "create.html"
    extend='base.html'
    redirect_field_name = '/profile/login'
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
            header_title  = "ویرایش بخش فرآیندی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این بخش فرآیندی ، موارد جدید را وارد کنید"
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
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormHoze(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='بخش فرآیندی جدید با موفقیت ساخته شد !!!')
                return redirect('ProcessListViewHoze')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='بخش فرآیندی مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewHoze( LoginRequiredMixin,View):
    
    extend = 'base.html'
    template_name = "delete.html"
    redirect_field_name = '/profile/login'
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
            header_title  = "پاک کردن یک بخش فرآیندی"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که بخش فرآیندی  " + obj.title + " "  + " را پاک کنید   ؟"
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
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='بخش فرآیندی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ProcessListViewHoze')
        return render(request,self.template_name,context)
    
    






#کلاس ایجاد رکورد جدید
class CreateViewProcessDocument( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'base.html'
    @staff_only 
    def get(self, request, *args, **kwargs):
        form = CreateFormProcessDocument()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک سند فرآیند  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک سند فرآیند  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex= {'extend':self.extend,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    @staff_only
    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormProcessDocument(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='سند فرآیند  جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewProcessDocument')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='سند فرآیند  مورد نظر ساخته نشد !')
        context= {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewProcessDocument(ListView):
  
    extend = 'base.html'
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست سند فرآیند  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام سند فرآیند  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['فرآیند' ,]
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = ProcessDocument.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
         
            data.append(query.process.title)

           
   
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = ProcessDocument
    ordering = '-created_at' 
    template_name ='list.html'



class ViewProcessDocument( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "proccesdocument.html"
    extend = 'baseEmployee.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(ProcessDocument,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = ProcessDocument.objects.all().filter(id=id)[0]
           
            pd = get_object_or_404(ProcessDocument,id = id)
            ProcessDescriptionSelected = ProcessDescription.objects.all().filter(ProcessDocumentRelated = pd)
            processFromSelected = ProcessFrom.objects.all().filter(ProcessDocumentRealated = pd).exclude(inputProcess = None)
            processToSelected = ProcessTo.objects.all().filter(ProcessDocumentRealated = pd).exclude(outputProcess = None)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "اطلاعات سند فرآیند   "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "چزییات سند فرآیند را در این صفحه می توانید مشاهده کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها

            #جدول لیست پرداختی ها
          
    
            #ایجاد لیست داده ها
            header_table   = ['ردیف' ,'شرح فعالیت','مسئول/مسئولان' ,'مستندات مورد استفاده در اجرای فعالیت','توضیحات']
            
            #list_data = {'ردیف' : 1 , 'شرح فعالیت' : ProcessDescriptionSelected.activityDescription , 'مسئول' : ProcessDescriptionSelected.ownerActivity , 'مستندات' : '' , 'توضیحات' : ProcessDescriptionSelected.description}
            #ایجاد لیست داده ها
           
            #جدول لیست کلاس ها
            # عنوان های جدول
        
       
            context =  {'extend':self.extend , 'object':obj , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,
                'color':color , 'columns':columns,'ProcessDescriptionSelected':ProcessDescriptionSelected,
                'header_table':header_table , 'form':form ,'pd':pd , 'processFromSelected':processFromSelected , 'processToSelected':processToSelected    }


        return render(request,self.template_name,context)
 

class UpdateViewProcessDocument( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(ProcessDocument,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormProcessDocument(instance=obj)
            
            obj = get_object_or_404(ProcessDocument,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش سند فرآیند  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این سند فرآیند  ، موارد جدید را وارد کنید"
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
        context= {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormProcessDocument(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='سند فرآیند  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewProcessDocument')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='سند فرآیند  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewProcessDocument( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    extend ='base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(ProcessDocument,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک سند فرآیند "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که سند فرآیند   " + obj.process.title + " "  + " را پاک کنید   ؟"
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
        context= {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='سند فرآیند  با موفقیت پاک شد !!!')
            
            return redirect('ListViewProcessDocument')
        return render(request,self.template_name,context)
    
 
 



class ProcessDescriptionHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "ProcessDescription.html"
    @staff_only 
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewProcessDescription( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'base.html'
    @staff_only 
    def get(self, request, *args, **kwargs):
        form = CreateFormProcessDescription()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک توضیحات فرآیند  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک توضیحات فرآیند  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex= {'extend':self.extend,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    @staff_only
    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormProcessDescription(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='توضیحات فرآیند  جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewProcessDescription')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='توضیحات فرآیند  مورد نظر ساخته نشد !')
        context= {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewProcessDescription(ListView):
  
    extend = 'base.html'
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست توضیحات فرآیند  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام توضیحات فرآیند  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['شناسنامه فرآیند مرتبط' , 'توضیحات فعالیت','صاحب فعالیت']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = ProcessDescription.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
         
            data.append(query.ProcessDocumentRelated)
            data.append(query.activityDescription)
            data.append(query.ownerActivity)
           
   
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = ProcessDescription
    ordering = '-created_at' 
    template_name ='list.html'



class ViewProcessDescription( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detail.html"
    extend = 'base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(ProcessDescription,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = ProcessDescription.objects.all().filter(id=id)[0]
           
            obj = get_object_or_404(ProcessDescription,id = id)
            
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "اطلاعات توضیحات فرآیند   "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "چزییات توضیحات فرآیند را در این صفحه می توانید مشاهده کنید"
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
            
            list_data = {'فرآیند مرتبط' : obj.ProcessDocumentRelated , 'توضیحات فعالیت' : obj.activityDescription , 'صاحب فرآیند' : obj.ownerActivity , 'توضیحات' : obj.description}
            #ایجاد لیست داده ها
           
            #جدول لیست کلاس ها
            # عنوان های جدول
            
                
            context =  {'extend':self.extend , 'object':obj , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,
                'color':color , 'columns':columns,'list_data':list_data,
                'header_table':header_table , 'form':form , }


        return render(request,self.template_name,context)
 

class UpdateViewProcessDescription( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(ProcessDescription,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormProcessDescription(instance=obj)
            
            obj = get_object_or_404(ProcessDescription,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش توضیحات فرآیند  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این توضیحات فرآیند  ، موارد جدید را وارد کنید"
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
        context= {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormProcessDescription(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='توضیحات فرآیند  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewProcessDescription')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='توضیحات فرآیند  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewProcessDescription( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    extend ='base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(ProcessDescription,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک توضیحات فرآیند "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که توضیحات فرآیند   " + obj.ProcessDocumentRelated.process.title + " "  + " را پاک کنید   ؟"
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
        context= {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='توضیحات فرآیند  با موفقیت پاک شد !!!')
            
            return redirect('ListViewProcessDescription')
        return render(request,self.template_name,context)
     
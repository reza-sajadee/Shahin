from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CreateFormCategoriy ,CreateFormNews
from .models import Categoriy ,News
from django.urls import reverse
from django.views.generic import ListView
import json
from django.contrib.auth.mixins import LoginRequiredMixin


from django.http.response import HttpResponseRedirect

from profile_app.models import Profile

from django.http import JsonResponse
from django.db.models import Model


from profile_app.decorators import  staff_only

from risk_app.utils import is_dabir



class CategoriyHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "Categoriy.html"
    @staff_only 
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewCategoriy( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'base.html'
    @staff_only 
    def get(self, request, *args, **kwargs):
        form = CreateFormCategoriy()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک دسته بندی خبر  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک دسته بندی خبر  جدید ، موارد خواسته شده را تکمیل نمایید"
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
        form = CreateFormCategoriy(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='دسته بندی خبر  جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewCategoriy')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='دسته بندی خبر  مورد نظر ساخته نشد !')
        context= {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewCategoriy(ListView):
  
    extend = 'base.html'
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست دسته بندی خبر  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام دسته بندی خبر  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
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
        queryset = Categoriy.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
         
            data.append(query.title)
           
   
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = Categoriy
    ordering = '-created_at' 
    template_name ='list.html'



class ViewCategoriy( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "detail.html"
    extend = 'base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Categoriy,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = Categoriy.objects.all().filter(id=id)[0]
           
            obj = get_object_or_404(Categoriy,id = id)
            
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "اطلاعات دسته بندی خبر   "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "چزییات دسته بندی خبر را در این صفحه میتوانید مشاهده کنید"
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
            
                
            context =  {'object':obj,'extend':self.extend , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,
                'color':color , 'columns':columns,'list_data':list_data,
                'header_table':header_table , 'form':form , }


        return render(request,self.template_name,context)
 

class UpdateViewCategoriy( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Categoriy,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormCategoriy(instance=obj)
            
            obj = get_object_or_404(Categoriy,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش دسته بندی خبر  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این دسته بندی خبر  ، موارد جدید را وارد کنید"
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
        context= {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormCategoriy(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='دسته بندی خبر  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewCategoriy')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='دسته بندی خبر  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewCategoriy( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'base.html'
    
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Categoriy,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        
        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک دسته بندی خبر "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که دسته بندی خبر   " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'object': obj,'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='دسته بندی خبر  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ListViewCategoriy')
        return render(request,self.template_name,context)
    
 
 
 



class NewsHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "News.html"
    @staff_only 
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewNews( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    @staff_only 
    def get(self, request, *args, **kwargs):
        form = CreateFormNews()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک خبر  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک خبر  جدید ، موارد خواسته شده را تکمیل نمایید"
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
        form = CreateFormNews(request.POST,request.FILES)
        
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='خبر  جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewNews')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='خبر  مورد نظر ساخته نشد !')
        context= {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewNews(ListView):
  
    extend='base.html'
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست خبر  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام خبر  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['شناسه' ,'عنوان' ,'دسته بندی']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = News.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.id)
            data.append(query.title)
            data.append(query.NewsCategoriy)
          
   
            



           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = News
    ordering = '-created_at' 
    template_name ='list.html'


class ArchiveViewNews(ListView):
  
    extend='baseEmployee.html'
    @staff_only
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست خبر  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام خبر  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['عنوان' ,'دسته بندی']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = News.objects.all().exclude(NewsCategoriy__title = 'اسلایدر')
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
         
            data.append(query.title)
            data.append(query.NewsCategoriy)
          
   
            



           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data , 'queryset':queryset}
        return context

    model = News
    ordering = '-created_at' 
    template_name ='newsList.html'



class ViewNews( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "newsSingle.html"
    extend = 'baseEmployee.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(News,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = News.objects.all().filter(id=id)[0]
            
            obj = get_object_or_404(News,id = id)
            allNews = News.objects.all().filter(NewsCategoriy__title = 'عمومی')
            if(len(allNews) > 3 ):
                allNews = allNews[:3]
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "اطلاعات خبر   "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "چزییات خبر را در این صفحه میتوانید مشاهده کنید"
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
            
                
            context =  {'object':obj,'extend':self.extend , 'header_title':header_title,
                'discribtion':discribtion,'icon_name':icon_name,
                'color':color , 'columns':columns,'list_data':list_data,
                'header_table':header_table , 'form':form , 'allNews':allNews}


        return render(request,self.template_name,context)
 

class UpdateViewNews( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend= 'base.html'
    @staff_only
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(News,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormNews(instance=obj)
            
            obj = get_object_or_404(News,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش خبر  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این خبر  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'form': form,'extend':self.extend,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormNews(request.POST , request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='خبر  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewNews')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='خبر  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewNews( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    extend ='base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(News,id = id)
        return obj
    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک خبر "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا میخواهید که خبر   " + obj.title + " "  + " را پاک کنید   ؟"
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
    @staff_only
    def post( self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='خبر  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ListViewNews')
        return render(request,self.template_name,context)
    
 
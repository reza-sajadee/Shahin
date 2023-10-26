from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CreateFormStandard , CreateFormStandardReferenceRelease
from .models import Standard , StandardReferenceRelease , RequirementStandards

from django.views.generic import ListView
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from risk_app.utils import is_dabir



class StandardHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend='base.html'
    template_name = "Standard.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewStandard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend='base.html'
    #قالب کلی ایجاد 
    template_name = "create.html"
    
    def get(self, request, *args, **kwargs):
        form = CreateFormStandard()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک استاندارد  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک استاندارد  جدید ، موارد خواسته شده را تکمیل نمایید"
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


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormStandard(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='استاندارد  جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewStandard')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='استاندارد  مورد نظر ساخته نشد !')
        context= {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewStandard(ListView):
  

    extend = 'baseEmployee.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست استاندارد  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام استاندارد  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['شماره استاندارد','موضوع استاندارد (فارسی)','موضوع استاندارد (انگلیسی)','نماد',
                          'وضعیت در شرکت','تاریخ انتشار (شمسی)','تاریخ انتشار (میلادی)','شماره تجدید نظر',
                          'مرجع صدور (اصلی)','زبان‌های متن ','نوع‌استاندارد','دامنه کاربرد جغرافیایی استاندارد',
                          'شماره استاندارد ملی/بین‌المللی متناظر','مرجع استاندارد ملی/بین‌المللی متناظر','کد واحد متولی سازمانی','واحدهای سازمانی مرتبط']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = Standard.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.standardNumber)
            data.append(query.standardTitlePersian)
            data.append(query.standardTitleEnglish)
            data.append(query.namad)
            data.append(query.vaziyatEjra)
            data.append(query.shamsiReleaseDate)
            data.append(query.miladiReleaseDate)
            data.append(query.tajdidNazarNumber)
            data.append(query.refrerence)
            data.append(query.language)
            data.append(query.typeStandard)
            data.append(query.geoDomainStandard)
            data.append(query.internationalStandardReference)
            data.append(query.internationalStandardReferenceNumber)
            data.append(query.vahedMotevaliCode)
            data.append(query.vahedMortabetCode)
            
 

         
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = Standard
    ordering = '-created_at' 
    template_name ='listStandard.html'


class ListViewStandardBand(ListView):
  

    extend = 'baseEmployee.html'
    def get(self, request,band=None, *args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست استاندارد  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام استاندارد  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['شماره استاندارد','موضوع استاندارد (فارسی)','موضوع استاندارد (انگلیسی)','نماد',
                          'وضعیت در شرکت','تاریخ انتشار (شمسی)','تاریخ انتشار (میلادی)','شماره تجدید نظر',
                          'مرجع صدور (اصلی)','زبان‌های متن ','نوع‌استاندارد','دامنه کاربرد جغرافیایی استاندارد',
                          'شماره استاندارد ملی/بین‌المللی متناظر','مرجع استاندارد ملی/بین‌المللی متناظر','کد واحد متولی سازمانی','واحدهای سازمانی مرتبط']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = RequirementStandards.objects.all().filter(standard__id =band )
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            try:
                if('-' in query.clauseNumber):
                    continue
                data = []
                dict_temp = {}
                data.append(query.clauseNumber)
                data.append(query.title)
                data.append(query.text)
                data.append(query.description)
                data.append(query.parentClause)
                data.append(query.childClause)
                data.append(query.standard)
      
            
            

         
            
           
                dict_temp = {query.id : data}
                list_data.append(dict_temp)
            except:
                pass
        #دیکشنری داده ها
        context= {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'queryset' : queryset}
        return render(request,self.template_name,context)


    model = Standard
    ordering = '-created_at' 
    template_name ='listStandardBand.html'



class UpdateViewStandard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend='base.html'
    template_name = "create.html"
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Standard,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormStandard(instance=obj)
            
            obj = get_object_or_404(Standard,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش استاندارد  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این استاندارد  ، موارد جدید را وارد کنید"
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
        context= {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormStandard(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='استاندارد  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewStandard')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='استاندارد  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewStandard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend='base.html'
    
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Standard,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک استاندارد "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که استاندارد   " + obj.standardTitlePersian + " "  + " را پاک کنید   ؟"
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
        context= {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='استاندارد  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ListViewStandard')
        return render(request,self.template_name,context)
    
    




class StandardReferenceReleaseHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend='base.html'
    template_name = "StandardReferenceRelease.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewStandardReferenceRelease( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend='base.html'
    #قالب کلی ایجاد 
    template_name = "create.html"
    
    def get(self, request, *args, **kwargs):
        form = CreateFormStandardReferenceRelease()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک استاندارد  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک استاندارد  جدید ، موارد خواسته شده را تکمیل نمایید"
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


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormStandardReferenceRelease(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='استاندارد  جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewStandardReferenceRelease')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='استاندارد  مورد نظر ساخته نشد !')
        context= {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewStandardReferenceRelease(ListView):
  

    extend = 'base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست مراجع صدور استاندارد ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام استاندارد  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['نام فارسی استاندارد مرجع','نام انگلیسی استاندارد مرجع','نماد','وب سایت','شماره تماس']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = StandardReferenceRelease.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.persianReferenceName)
            data.append(query.englishReferenceName)
            data.append(query.namad)
            
            data.append(query.website)
            data.append(query.phoneNumber)
         
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = StandardReferenceRelease
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewStandardReferenceRelease( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend='base.html'
    template_name = "create.html"
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(StandardReferenceRelease,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormStandardReferenceRelease(instance=obj)
            
            obj = get_object_or_404(StandardReferenceRelease,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش استاندارد  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این استاندارد  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend' :self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormStandardReferenceRelease(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='استاندارد  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewStandardReferenceRelease')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='استاندارد  مورد نظر ساخته نشد !')           
            context= {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewStandardReferenceRelease( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend='base.html'
    
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(StandardReferenceRelease,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک استاندارد "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که استاندارد   " + obj.persianReferenceName + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend' : self.extend,'riskDabir':is_dabir(self) ,'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):
        context= {'extend':self.extend,'riskDabir':is_dabir(self),}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='استاندارد  با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ListViewStandardReferenceRelease')
        return render(request,self.template_name,context)
    
    





from django.shortcuts import render
from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CreateFormEvent
from .models import Event 
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
from django.http import JsonResponse
from django.db.models import Model
from profile_app.decorators import  staff_only
from profile_app.models import Profile
# Create your views here.
from .serializers import EventSerializer
from django.db.models import Q
def load_events(request):
    #qs_val = list(Event.objects.all().filter(user = Profile.objects.get(user = request.user)))
    qs_val = list(Event.objects.all().filter(Q(allUser = True) | Q(user = Profile.objects.get(user = request.user))))
    serializer = EventSerializer(qs_val , many=True)
    return JsonResponse( serializer.data,safe=False)


class EventHome( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "Event.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewEvent( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend='base.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormEvent()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک رویداد جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک رویداد جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex = {'extend':self.extend,'riskDabir':'','form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormEvent(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='رویداد جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewEvent')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='رویداد مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':'','form': form}
        return render(request,self.template_name,context)


class ListViewEvent(ListView):
  


    extend='base.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست رویداد ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام رویداد ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
    
        
        header_table   = ['فعال','پاک شده','ایجاد کننده','عنوان','توضیحات','زمان شروع','زمان پایان']
        #اسم داده های جدول
        object_name    = ['title','Event']
        #دریافت تمام داده ها
        queryset = Event.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            if(query.is_active):    
                data.append('بلی')
            else:
                data.append('خیر')
            if(query.is_deleted):    
                data.append('بلی')
            else:
                data.append('خیر')
            data.append(query.user)
            data.append(query.title)
            data.append(query.description)
            data.append(query.start)
            data.append(query.end)
            
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':'', 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data }
        return context

    model = Event
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewEvent( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend='base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Event,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormEvent(instance=obj)
            
            obj = get_object_or_404(Event,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش رویداد "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این رویداد ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'extend':self.extend,'riskDabir':'' ,'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend,'riskDabir':'',}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormEvent(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='رویداد جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewEvent')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='رویداد مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':'','form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewEvent( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    
    template_name = "delete.html"
    extend = 'base.html'
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Event,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک رویداد"
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که رویداد  " + obj.title + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'extend':self.extend,'riskDabir':'','object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):
        context = {'extend':self.extend,'riskDabir':'',}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='رویداد با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ListViewEvent')
        return render(request,self.template_name,context)
    
    

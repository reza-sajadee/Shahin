from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from profile_app.models import Profile
from .forms import CreateFormMessages
from .models import Messages

from django.views.generic import ListView
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from risk_app.utils import is_dabir

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions , status
from .serializers import MessagesSerializer


class MessagesHome( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    template_name = "Messages.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)


#کلاس ایجاد رکورد جدید
class CreateViewMessages( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "create.html"
    extend = 'base.html'
    def get(self, request, *args, **kwargs):
        form = CreateFormMessages()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک اطلاعیه  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک اطلاعیه  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        #دیکشنری داده ها
        contex = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormMessages(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='اطلاعیه  جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewAdminMessages')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='اطلاعیه  مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form}
        return render(request,self.template_name,context)


class ListViewMessages(ListView):
  

    extend = 'baseEmployee.html'
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
        header_table   = ['ارسال کننده' , 'توضیحات', 'وضعیت' ,'آیکون', '']
        #اسم داده های جدول

        #دریافت تمام داده ها
        profileReciver = Profile.objects.all().filter(user =self.request.user )[0]
        queryset = Messages.objects.all().filter( reciver= profileReciver  )
        list_data = []
        unread = 0
        allnotif = len(queryset)
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.sender)
            data.append(query.title)
            data.append(query.description[:75] + ' ...')
            data.append(query.status)
            data.append(query.icon)
           
            if(query.personalStatus =='notRead'):
                data.append('خوانده نشده')
                unread +=1
            else:
                data.append('خوانده شده')
   
            
 
        

         
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : queryset , 'unread':unread , 'allnotif':allnotif}
        return context

    model = Messages
    ordering = '-created_at' 
    template_name ='inbox.html'

class ListViewAdminMessages(ListView):
  

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
        header_table   = ['عنوان' , 'توضیحات', 'وضعیت' ,'آیکون' , 'گیرندگان' ,'وضعیت دیده شدن']
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = Messages.objects.all()
        list_data = []
        
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.title)
            data.append(query.description[:75] + ' ...')
            data.append(query.status)
            data.append(query.icon)
          
            data.append(query.reciver)
            if(query.personalStatus =='notRead'):
                data.append('خوانده نشده')
            else:
                data.append('خوانده شده')
   
            
 


         
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = {'extend':self.extend,'riskDabir':is_dabir(self), 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = Messages
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewMessages( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Messages,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormMessages(instance=obj)
            
            obj = get_object_or_404(Messages,id = id)
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
            context =  {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
       
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormMessages(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='نوبت ممیزی  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewAdminMessages')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='نوبت ممیزی  مورد نظر ساخته نشد !')           
            context = {'extend':self.extend,'riskDabir':is_dabir(self),'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewMessages( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'base.html'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Messages,id = id)
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
            context       = {'extend':self.extend,'riskDabir':is_dabir(self),'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):
        
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='نوبت ممیزی  با موفقیت پاک شد !!!')
            context={'extend':self.extend,'riskDabir':is_dabir(self),}
            return redirect('ListViewAdminMessages')
        return render(request,self.template_name,context)
    


@permission_classes([IsAuthenticated])    
class ListMessagesAPI(APIView):
    def get(self, request,id=None ,*args, **kwargs):
        profileSelected = Profile.objects.get(user = request.user)
      
        query = Messages.objects.all().filter(reciver = profileSelected).filter(personalStatus='pending')
        serializers = MessagesSerializer(query , many=True)
        return Response(serializers.data , status = status.HTTP_200_OK)
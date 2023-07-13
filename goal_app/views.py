from django.shortcuts import render
from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CreateFormObjective
from .models import Objective 
from django.urls import reverse
from django.views.generic import ListView
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated

from django.http.response import HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Model
from profile_app.decorators import  staff_only
# Create your views here.


#کلاس ایجاد رکورد جدید
class CreateViewObjective( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createObjectiveView.html"
    extend='baseEmployee.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateFormObjective()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک هدف جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک رویداد جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "primary"
        #دیکشنری داده ها
        contex = {'extend':self.extend,'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormObjective(request.POST,request.FILES)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            form.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='رویداد جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewObjective')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='رویداد مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'riskDabir':'','form': form}
        return render(request,self.template_name,context)


from django.shortcuts import render
from django.shortcuts import render
from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .models import Faq 
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

# Create your views here.

# Create your views here.

class ViewFaqDashboard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "clearDashboard.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
    
    def get(self, request ,*args, **kwargs):
        
        
        partials = 'partials/faqDashboard.html'
        
        
        
       
        
        
        
        
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "سوالات متداول "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        
        
      
        
        allFaq = Faq.objects.all()
            
    
        #رنگ             
        columns       = 1
        
        
        
        #رنگ             
        columns       = 1
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,'header_title':header_title,
        'columns':columns , 'color':color ,'partials':partials,'allFaq':allFaq }

        return render(request,self.template_name,context)
    

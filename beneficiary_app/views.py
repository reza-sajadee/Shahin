from django.shortcuts import render
from .models import BeneficiaryList , Beneficiary , GroupBeneficiary
from django.views.generic import ListView
# Create your views here.

class ListViewBeneficiaryList(ListView):
  
    extend = 'baseEmployee.html'
  
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست ذینفعان سازمان"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام ارزیابی ریسک سوال  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
    
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = BeneficiaryList.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        
        #دیکشنری داده ها
        context= {'extend':self.extend, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color ,
            'queryset' : queryset}
        return context

    model = BeneficiaryList
    ordering = '-created_at' 
    template_name ='listBeneficiaryList.html'


class ListViewBeneficiary(ListView):
  
    extend = 'baseEmployee.html'
  
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست ذینفعان سازمان"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام ارزیابی ریسک سوال  ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
    
        #اسم داده های جدول

        #دریافت تمام داده ها
        beneficiary = Beneficiary.objects.all()
        group = GroupBeneficiary.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        
        #دیکشنری داده ها
        context= {'extend':self.extend, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color ,
            'beneficiary' : beneficiary , 'group' : group}
        return context

    model = BeneficiaryList
    ordering = '-created_at' 
    template_name ='listBeneficiary.html'


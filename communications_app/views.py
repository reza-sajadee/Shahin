from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView
from organization_app.models import JobBank
from .models import External
class ListInternalCommunications(ListView):
  


    extend='baseEmployee.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست ارتباطات درون سازمانی"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام شغل ها را در بانک مشاغل  مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
       
        
        header_table   = ['پست سازمانی','نام و نام خانوادگی','همراه','داخلی','تلفن مستقیم']
        #اسم داده های جدول
        object_name    = ['vahed','profile', 'counter']
        #دریافت تمام داده ها
        queryset = JobBank.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            try:
                data = []
                dict_temp = {}
                
                data.append(query.jobBankPost.title)
                data.append(query.profile.firstName + '-' + query.profile.lastName)
                data.append('-')
                data.append('-')
                data.append('-')
                
                

    
                dict_temp = {query.id : data}
                list_data.append(dict_temp)
            except:
                pass
        #دیکشنری داده ها
        context = {'extend':self.extend, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data}
        return context

    model = JobBank
    ordering = '-created_at' 
    template_name ='listCommunications.html'




class ListViewExternal(ListView):
  

    extend = 'baseEmployee.html'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست ارتباطات برون سازمانی"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام کمیته  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['سازمان' , 'موضوع ارتباط' ,'زمان ارتباط' , 'نحوه ارتباط' ,'اقدام کننده'   ,'ارتباط گیرنده' , ]
        #اسم داده های جدول

        #دریافت تمام داده ها
        queryset = External.objects.all()
        list_data = []
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.organization)
            data.append(query.title)
            data.append(query.time)
            data.append(query.how)
            data.append(query.actor)
            data.append(query.reciver)
            
            
 

         
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = { 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data, 'extend' : self.extend,}
        return context

    model = External

    template_name ='externalList.html'
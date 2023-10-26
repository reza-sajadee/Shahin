from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from standardTable_app.models import Standard
from .models import InputManagementReview,ProfileManagementReview , InviteManagementReview ,approveManagementReview
from organization_app.models import JobBank
from django.shortcuts import  redirect
from django.views.generic import ListView
from jalali_date import datetime2jalali, date2jalali
# Create your views here.
class CreateViewManagementReview( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "createManagementReview.html"
    
    extend ='baseEmployee.html'

    def get(self, request, *args, **kwargs):
      
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ساخت یک پروفایل ریسک  جدید "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک پروفایل ریسک  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "success"
        allSystem = Standard.objects.all()
        allInput = InputManagementReview.objects.all()
        allInvited = ProfileManagementReview.objects.all()[0].members
        allJob    = JobBank.objects.all()
        
        #دیکشنری داده ها
        contex= {'extend':self.extend, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'allSystem':allSystem ,'allInput':allInput ,'allInvited':allInvited  , 'allJob':allJob}
        return render(request,self.template_name,contex)


    def post(self, request , *args, **kwargs):
        return redirect('ViewManagmentReview')




class ListViewManagementReview(ListView):

  
    extend = 'baseEmployee.html'
    menu_link = 'ViewMomayezi'
    
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "سوابق بازنگری و مدیریت"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام سوال ممیزی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = [ 'ردیف' , 'عنوان' , 'تاریخ' ,   ]
        #اسم داده های جدول






        #دریافت تمام داده ها
        queryset = InviteManagementReview.objects.all()
        list_data = []
        counter = 0
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            counter += 1
            data.append(counter)
            data.append(query.ProfileManagementReviewRelated.title)
            data.append(datetime2jalali(query.dateManagementReview).strftime('14%y/%m/%d'))
           
  
           
   
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context= {'extend':self.extend , 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table 
          ,  'list_data' : list_data}
        return context

    model = InviteManagementReview
    ordering = '-created_at' 
    template_name ='listManagementReview.html'




class ViewManagementReview( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "viewManagementReview.html"
    extend = 'baseEmployee.html'
    

    def get(self, request,inviteId=None ,*args, **kwargs):

          
       
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ویرایش گزارش ممیزی  "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این گزارش ممیزی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        #رنگ             
        columns       = 1
        #دیکشنری داده ها
        peresents =['محمدعلیرحیمی','مجید خنجری','غلامرضا محتسبی','محسن زرگر','کیوان مظفری','علی مظفری','مجید بیاتی','علیرضا احمدی','روح‌اله خداکرم','محمد مهدی مظلوم‌زاده','لیلی نجاتی','سونیا کاوه','مینا حسنی',]
        absents = ['مهرداد فیضی','احمد محمودی سوره','کاظم فهیمی','فرهاد یادگاری','رضا خودسیانی','علی رضایانیی','احمد محمودی سوره','کاظم فهیمی','فرهاد یادگاری','رضا خودسیانی','علی رضایانی']
        InviteManagementReviewSelected = InviteManagementReview.objects.all().filter(id =inviteId )[0]
        ProfileManagementReviewSelected = InviteManagementReviewSelected.ProfileManagementReviewRelated
        allApproved = approveManagementReview.objects.all().filter(ProfileManagementReviewApprovedRelated =ProfileManagementReviewSelected )
        context =  {'header_title':header_title,'discribtion':discribtion,'icon_name':icon_name,
        'color':color , 'columns':columns ,'extend':self.extend ,'allApproved':allApproved ,'InviteManagementReviewSelected':InviteManagementReviewSelected ,'ProfileManagementReviewSelected':ProfileManagementReviewSelected , 'peresents':peresents , 'absents':absents}


        return render(request,self.template_name,context)
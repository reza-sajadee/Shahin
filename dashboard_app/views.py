
from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CreateFormDashboard
from .models import Dashboard
from news_app.models import News
from event_app.models import Event
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from profile_app.decorators import  staff_only 
from profile_app.models import Profile
from notifications_app.models import Notifications
from messages_app.models import Messages


class DashboardHome( LoginRequiredMixin,View):
    template_name = "dashboard.html"
    redirect_field_name = '/profile/login'
    
    def get(self, request,*args, **kwargs):
        
        context={ 'extend' : 'base.html'}
        return render(request,self.template_name ,context)


class DashboardEmployeeHome( LoginRequiredMixin,View):
    template_name = "dashboardEmployee.html"
    redirect_field_name = '/profile/login'
    def get(self, request,*args, **kwargs):
       
       
       
        
        news = News.objects.filter(NewsCategoriy__title = 'عمومی' )
        if(len(news) > 3):
            news = news[:2]
        sliders= News.objects.filter(NewsCategoriy__title = 'اسلایدر')
        events = Event.objects.get_all_events()
        profileNot =Profile.objects.all().filter(user=request.user)[0]
        notifications = Notifications.objects.all().filter(recivers = profileNot).order_by('-created_at').filter(personalStatus ='pending')
        messages = Messages.objects.all().filter(reciver = profileNot).order_by('-created_at').filter(personalStatus ='pending')
        
        countNotif = len(notifications)
        countmsg = len(messages)
        if(len(sliders) == 0):
            firstSlide = sliders
        else:
            if(len(sliders) == 1):
                firstSlide = sliders[0]
                sliders = []
            else:
                sliders.reverse()
                firstSlide = sliders[0]
                if(len(sliders) > 5):
                    sliders=sliders[1:6]
                else:
                    sliders=sliders[1:]
       
        context={ 'extend' : 'base.html' , 'news':news , 'sliders':sliders ,'firstSlide':firstSlide , 'events' : events , 'notifications' :notifications , 'countNotif':countNotif , 'countmsg' : countmsg , 'messages':messages}
        return render(request,self.template_name,context)



class Login( LoginRequiredMixin,View):
    template_name = "login.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)



class CreateViewDasboard( LoginRequiredMixin,View):

    template_name = "create.html"
    redirect_field_name = '/profile/login'
    def get(self, request, *args, **kwargs):
        
        form = CreateFormDashboard()
        header_title  = "ساخت یک بخش بندی "
        discribtion   = "جهت ایجاد یک بخش بندی جدید ، موارد خواسته شده را تکمیل نمایید"
        icon_name     = "person_add"
        columns       = 1
        color         = "success"
        contex = {'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        form = CreateFormDashboard(request.POST,request.FILES)
         #sweetify.toast(self.request,timer=30000 , icon="success",title = 'Some error happened here - reload the site')
        sweetify.toast(self.request,timer=30000 , icon="error",title = 'متاسفانه درخواست شما انجام نشد!!!')
        if form.is_valid():
            form.save()
            sweetify.toast(self.request,timer=30000 , icon="success",title ='بخش بندی جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewDashboard')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='بخش بندی مورد نظر ساخته نشد !')
        context = {'form': form}
        return render(request,self.template_name,context)


class ListViewDashboard(ListView):
  


    def get_context_data(self, **kwargs):
        header_title  = "لیست بخش بندی ها"
        discribtion   = "در این بخش لیست تمام بخش بندی ها را میتوانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر میتوانید داستفاده کنید "
        icon_name     = "table_chart"
        columns       = 1
        color         = "success"
        header_table   = ['نام' ,'تاریخ ایجاد' , 'تاریخ آپدیت']
        object_name    = ['name' , 'created_at' , 'updated_at']
        
        context = super().get_context_data(**kwargs)
        queryset = Dashboard.objects.all()
        list_data = []
        
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.name)
            data.append(query.created_at)
            data.append(query.updated_at)
            dict_temp = {query.id : data}
            list_data.append(dict_temp)

        context = { 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
         'object_name' : object_name ,  'list_data' : list_data}
        return context

    model = Dashboard
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewDashboard( LoginRequiredMixin,View):
    template_name = "create.html"
    redirect_field_name = '/profile/login'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Dashboard,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormDashboard(instance=obj)
            obj = get_object_or_404(Dashboard,id = id)
            header_title  = "ویرایش بخش بندی "
            discribtion   = "جهت ویرایش این بخش بندی ، موارد جدید را وارد کنید"
            icon_name     = "person_add"
            color         = "info"
            columns       = 1
            context =  {'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormDashboard(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='بخش بندی جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewDashboard')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='بخش بندی مورد نظر ساخته نشد !')           
            context = {'form': form,'object':obj}
        return render(request,self.template_name,context)



class DeleteViewDashboard( LoginRequiredMixin,View):
    
    template_name = "delete.html"
    redirect_field_name = '/profile/login'
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(Dashboard,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            header_title  = "پاک کردن یک بخش بندی"
            discribtion   = "آیا میخواهید که بخش بندی  " + obj.name + " "  + " را پاک کنید   ؟"
            icon_name     = "delete_forever"
            color         = "danger"
            context       = {'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='بخش بندی با موفقیت پاک شد !!!')
            context['object']=None
            return redirect('ListViewDashboard')
        return render(request,self.template_name,context)
    
    
    
# اطلاعات پایه --- > مدل فرآیندی 
class ViewModelProccess( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "مدل فرآیندی"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر بخش های محتلف مدل فرآیندی را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : '','title' : 'زنجیره ارزش' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'نقشه فرایندی' , 'link' : 'ProcessMap' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : 'url','title' : 'ماتریس فرایندی' , 'link' : 'media/other/ماتریس فرآیند ها.xlsx' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'لیست فرآیندی' , 'link' : 'ListViewProcess' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'جدول ارتباطات فرایندی' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            #{ 'staticLink' : '','title' : 'شناسنامه‌های فرایندی (جستجو)' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : 'url','title' : 'شاخص های ارزیابی فرآیند' , 'link' : 'media/other/شاخص های ارزیابی فرآیند.xlsx' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : 'url','title' : 'شاخص های مقایسه ای عملکرد 99 و 1400' , 'link' : 'media/other/شاخص های مقایسه ای عملکرد 99 و 1400.xlsx' ,'icon':'control-panel' , 'color' : '1' , } ,
            
            
                ]
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)
 
 # اطلاعات پایه --- > برنامه راهبردی     
class ViewStrategyPlan( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "برنامه راهبردی "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر بخش های محتلف برنامه راهبردی  را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : 'url','title' : 'سند استراتژی' , 'link' : 'media/other/سند استراتژی.pdf' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : 'url','title' : ' اهداف استراتژیک' , 'link' : 'media/other/اهداف.xlsx' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : 'url','title' : 'تحلیل شرایط سازمان' , 'link' : 'media/other/تحلیل شرایط سازمان.xlsx' ,'icon':'control-panel' , 'color' : '1' , } ,

            
            
                ]
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)
   
# اطلاعات پایه --- >  ذینفعان سازمان  
class ViewStockHoldersOrganization( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ذینفعان سازمان "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر بخش های محتلف ذینفعان سازمان  را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : '','title' : ' ذینفعان' , 'link' : 'ListViewBeneficiaryList' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'نیازها و انتظارات ذینفعان' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
                ]
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)
    
#  مدیریت کیفیت --- >  اهداف و برنامه ها 
class ViewGoalAndPlan( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "اهداف و برنامه ها "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر هدف و برنامه های  را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : '','title' : 'تعریف هدف' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'لیست اهداف ' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,


            
            
                ]
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)
 
    
#  مدیریت کیفیت --- >   کمیته ها   
class ViewCommittee( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = " کمیته "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر هدف و برنامه های  را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : '','title' : 'تعریف کمیته ' , 'link' : 'CreateViewCommittee' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'لیست کمیته ' , 'link' : 'ListViewCommittee' ,'icon':'control-panel' , 'color' : '1' , } ,


            
            
                ]
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)
 
#  مدیریت کیفیت --- > مدیریت فرآیند ها 
class ViewProccessManagment( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "مدیریت فرآیند ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر مدیریت و فرآیند ها  را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : '','title' : 'مدل فرایندی' , 'link' : 'ViewModelProccess' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'ثبت شاخص‌های فرایندی' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'شاخص‌های فرایندی' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'پایش و اندازه‌گیری فرایندها' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,


            
            
                ]
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)

#  risk_app/views.app 33 مدیریت کیفیت --- >   مدیریت ریسک در بخش      
 
#  مدیریت کیفیت --- > کنترل عدم انطباق و اقدامات اصلاحی 
class ViewAdamEntebagh( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "کنترل عدم انطباق و اقدام اصلاحی"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر مدیریت و فرآیند ها  را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : '','title' : 'ثبت عدم انطباق / اقدام اصلاحی' , 'link' : 'MomayeziCreateViewCorrectiveAction' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'لیست اقدامات اصلاحی در حال انجام' , 'link' : 'ListViewCorrectiveActionDoing' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'لیست اقدامات اصلاحی به اتمام رسیده' , 'link' : 'ListViewCorrectiveActionDone' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'داشبورد اقدامات اصلاحی' , 'link' : 'ViewCorrectiveActionDashboard' ,'icon':'control-panel' , 'color' : '1' , } ,
            
            



            
            
                ]
        if  Profile.objects.filter(user =self.request.user)[0].user.is_superuser :
            list_menu.append({ 'staticLink' : '','title' : 'برنامه اجرایی' , 'link' : '' ,'icon':'control-panel' , 'color' : '2' , } ,)
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)

#  مدیریت کیفیت --- > مدیریت  تغییر 
class ViewParadigmManagment( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "مدیریت تغییر"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیربخش های مختلف مدیریت تغییر را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : '','title' : 'ثبت شناسنامه تغییر' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'شناسنامه تغییرات' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,


            
            
                ]
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)
    
    
#  مدیریت کیفیت --- > ممیزی   
class ViewMomayezi( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ممیزی داخلی"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر بخش های مختبف ممیزی  را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            
            { 'staticLink' : '','title' : 'لیست ممیزان داخلی شرکت' , 'link' : 'ListViewMomayeziTeam' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'درخواست عضویت در تیم ممیزان داخلی' , 'link' : 'RegisterViewMomayeziTeamRequest' ,'icon':'control-panel' , 'color' : '1' , } ,
            
            { 'staticLink' : '','title' : 'برنامه ممیزی داخلی' , 'link' : 'ListViewCalenderMomayeziType' ,'icon':'control-panel' , 'color' : '1' , } ,
            
            
            
            
            { 'staticLink' : '','title' : 'گزارش ممیزی داخلی' , 'link' : 'ListViewReportType' ,'icon':'control-panel' , 'color' : '1' , } ,
            
   


            
            
                ]

        if  Profile.objects.filter(user =self.request.user)[0].user.is_superuser :
            
            list_menu.append({ 'staticLink' : '','title' : 'ایجاد ممیزی داخلی' , 'link' : 'MomayeziTypeMomayezi' ,'icon':'control-panel' , 'color' : '2' , } )
            list_menu.append({ 'staticLink' : '','title' : 'تدوین برنامه ممیزی-دبیر دفتر بهبود' , 'link' : 'CreateViewCalenderMomayeziListType' ,'icon':'control-panel' , 'color' : '2' , } )
            list_menu.append({ 'staticLink' : '','title' : 'تدوین سوالات ممیزی' , 'link' : 'CreateViewQuestionMomayeziList' ,'icon':'control-panel' , 'color' : '2' , } )
            list_menu.append({ 'staticLink' : '','title' : 'چک‌لیست‌های ممیزی داخلی' , 'link' : '' ,'icon':'control-panel' , 'color' : '2' , } )
            list_menu.append({ 'staticLink' : '','title' : 'تدوین / به‌روزرسانی چک‌لیست‌های ممیزی' , 'link' : '' ,'icon':'control-panel' , 'color' : '2' , } ,)
            list_menu.append({ 'staticLink' : '','title' : 'ثبت یافته‌های ممیزی (چک‌لیست) ' , 'link' : 'ListViewCheckListMomayeziEntering' ,'icon':'control-panel' , 'color' : '2' , } )
            list_menu.append({ 'staticLink' : '','title' : 'تدوین گزارش ممیزی داخلی ' , 'link' : 'ListViewReportEntering' ,'icon':'control-panel' , 'color' : '2' , } )

        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)
  
#  مدیریت کیفیت --- > ارزیابی عملکرد   
class ViewPerformanceIndex( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ارزیابی عملکرد"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر بخش های مختبف ممیزی  را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            
            { 'staticLink' : '','title' : 'داشبورد شاخص عملکردی' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'نتایج شاخص عملکردی' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'ثبت داده ها  ' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            

                ]

        if  Profile.objects.filter(user =self.request.user)[0].user.is_superuser :
            list_menu.append({ 'staticLink' : '','title' : 'ثبت شاخص عملکردی' , 'link' : 'CreateViewPerformanceIndex' ,'icon':'control-panel' , 'color' : '2' , } )
            list_menu.append({ 'staticLink' : '','title' : 'لیست شاخص های عملکردی' , 'link' : 'ListViewPerformanceFormula' ,'icon':'control-panel' , 'color' : '2' , } )
            list_menu.append({ 'staticLink' : '','title' : 'گزارش داده های ثبت شده' , 'link' : '' ,'icon':'control-panel' , 'color' : '2' , } )
            

        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)
  
#  مدیریت کیفیت --- > بازنگری مدیریت   
class ViewManagmentReview( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "مدیریت بازنگری"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر بخش های مختلف مدیریت تغییر   را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : '','title' : 'تعیین دستور جلسه بازنگری مدیریت' , 'link' : 'CreateViewManagementReview' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'دعوتنامه بازنگری مدیریت' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'صورتجلسه بازنگری مدیریت' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'سوابق بازنگری مدیریت' , 'link' : 'ListViewManagementReview' ,'icon':'control-panel' , 'color' : '1' , } ,

   


            
            
                ]
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)
#  میتندات و سوابق  --- > درخواست تهیه تغییر در مدرک   
class ViewMostanadatChange( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "درخواست تهیه / تغییر در مدرک"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر بخش های مختلف مدیریت تغییر   را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : '','title' : 'درخواست تغییر ، حذف و یا تدوین سند' , 'link' : 'CreateViewMostanadatDakheliChange' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'لیست درخواست ها' , 'link' : 'ListViewMostanadatDakheliChangeDoing' ,'icon':'control-panel' , 'color' : '1' , } ,
            

   


            
            
                ]
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)

#  مدیریت جلسات  --- >  پروفایل جلسات  
class ViewProfileMeeting( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "پروفایل جلسات"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر بخش های مختلف پروفایل جلسات  را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            
                ]
        if  Profile.objects.filter(user =self.request.user)[0].user.is_superuser :
            list_menu.append({ 'staticLink' : '','title' : 'تعریف پروفایل جلسه' , 'link' : 'CreateViewMeetingProfile' ,'icon':'control-panel' , 'color' : '2'  } )
            list_menu.append({ 'staticLink' : '','title' : 'لیست پروفایل جلسات ' , 'link' : 'ListViewMeetingProfile' ,'icon':'control-panel' , 'color' : '2' , } )
            list_menu.append({ 'staticLink' : '','title' : '(درحال برگزاری) لیست جلسات  ' , 'link' : 'ListViewMeeting' ,'icon':'control-panel' , 'color' : '2' , } )
            list_menu.append({ 'staticLink' : '','title' : 'گزارش جلسات ' , 'link' : 'ListViewMeetingReview' ,'icon':'control-panel' , 'color' : '2' , } )
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)
#  مدیریت جلسات  --- >  'گزارش'   
class ViewReport( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = " گزارش"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر بخش های مختلف پروفایل جلسات  را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : '','title' : 'درخواست گزارش' , 'link' : 'CreateViewReport' ,'icon':'control-panel' , 'color' : '1'  } ,
            { 'staticLink' : '','title' : 'لیست گزارشات  درخواست شده' , 'link' : 'ListViewReportRequest' ,'icon':'control-panel' , 'color' : '1'  } ,
            { 'staticLink' : '','title' : 'لیست گزارشات   دریافت شده' , 'link' : 'ListViewReportDone' ,'icon':'control-panel' , 'color' : '1'  } ,
                ]
        
            
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)

#  مدیریت جلسات --- >  برگذاری جلسات    
class VieweMeeting( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "برگزاری جلسه"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر  بخش های مختلف بیرگزاری جلسه  را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : '','title' : 'برنامه‌ریزی تشکیل جلسه (ثبت در تقویم)' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'ارسال دعوتنامه' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'ثبت صورتجلسه' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,


            
            
                ]
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)
#  مدیریت جلسات --- >  برگذاری جلسات    
class ViewProject( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "مدیریت پروژه"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر  بخش های مختلف بیرگزاری جلسه  را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : '','title' : 'تعریف پروفایل پروژه' , 'link' : 'CreateViewProjectProfile' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'لیست پروفایل پروژه' , 'link' : 'ListViewProjectProfile' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'پروژه های من' , 'link' : 'ListViewProject' ,'icon':'control-panel' , 'color' : '1' , } ,
            


            
            
                ]
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)


#  ارتباطات  --- >  لیست ارتباطات درون سازمانی  
class VieweInternalComunication( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ارتباطات درون سازمانی"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر بخش های مختلف ارتباطات درون سازمانی   را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : '','title' : 'تماس‌های اضطراری ' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'داخلی واحدهای سازمانی' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'ارتباط با مدیران' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,


            
            
                ]
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)

#  ارتباطات  --- >  لیست ارتباطات برون سازمانی  
class VieweExternalComunication( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "listMenu.html"
    extend = 'baseEmployee.html'    
    @staff_only 
    def get(self, request,id=None ,*args, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ارتباطات برون سازمانی"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در زیر بخش های مختلف ارتباطات برون سازمانی را میتوانید مشاهده نمایید "
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        

        #لینک های دکمه های بزرگ درون صفحه
        list_menu = [
            { 'staticLink' : '','title' : 'تماس‌های اضطراری' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,
            { 'staticLink' : '','title' : 'لیست تماس‌های برون سازمانی' , 'link' : '' ,'icon':'control-panel' , 'color' : '1' , } ,



            
            
                ]
        context =  {'extend':self.extend, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color ,'list_menu':list_menu,
            }
        return render(request,self.template_name,context)
    

from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic , View
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
import sweetify
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from profile_app.models import Profile
from notifications_app.models import Notifications
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
from news_app.models import News
import math
from risk_app.utils import is_dabir

class UserRegisterView(generic.CreateView):
    form_class = UserCreationForm   
    template_name = 'login.html'
    success_url = reverse_lazy('login')
    
class ProfileHome( LoginRequiredMixin,View):
    template_name = "profile.html"
    redirect_field_name = '/profile/login'
    

    def get(self, request,*args, **kwargs):
        
        profile = Profile.objects.get(user=request.user)
        profileNot =Profile.objects.all().filter(user=request.user)
        notifications = Notifications.objects.all().filter(recivers = profile).order_by('-created_at')
        userAllNotification = []
        if(len(notifications)>7):
            notifications = notifications[:7]
        # for noti in notifications:
        #     recivers = noti.recivers.all().filter()
            
        #     if(len(recivers)==1):
        #         if (profile.user == noti.recivers.get().user):
        #             userAllNotification.append((noti))
            
        #     if(len(recivers)>1 ):
                
        #         for ricvie in recivers:
                   
        #             if (profile == ricvie):
                       
                       
        #                 userAllNotification.append(noti)
        
        # if (len(userAllNotification)  > 7):
        #     userAllNotification = userAllNotification[:7]
       
        context ={'profile' : profile , 'notifications':notifications ,'riskDabir':is_dabir(self), }
        return render(request,self.template_name , context)
    
    def post(self, request ,*args, **kwargs):
        context= {'extend':'base.html', 'riskDabir':is_dabir(self),}
        loginedUser = request.user
        currentPassword  = request.POST.get("currentPassword", "")
        newPassword      = request.POST.get("newPassword", "")
        ConfirmPassword  = request.POST.get("ConfirmPassword", "")
        if(check_password(currentPassword,loginedUser.password)):
            if(len(newPassword)!=0):
                if(len(ConfirmPassword)!=0):
                    if(ConfirmPassword == newPassword):
                        u = User.objects.get(username__exact=loginedUser.username)
                        u.set_password(newPassword)
                        u.save()
                        sweetify.toast(self.request,timer=30000 , icon="success",title ='رمز عبور با موفقیت تغییر کرد !!!')
                        auth.logout(request)
                        return render(request,'login')
                    else:
                        sweetify.toast(self.request,timer=30000 , icon="error",title ='رمز عبور تطابق ندارد !!!')
                        return redirect('ProfileHome')
                else:
                    sweetify.toast(self.request,timer=30000 , icon="error",title ='رمز عبور را باید دوبار وارد نمایید !!!')
                    return redirect('ProfileHome') 
                 
        #     
        return render(request,self.template_name,context)


class UpdateViewNotifStatusPersonal( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    def get_obj(self):
        
        id = self.kwargs.get('notifId')
        obj=None
        if id is not None:
            obj = get_object_or_404(Notifications,id = id)
        return obj
    
    def get(self, request,notifId=None ,*args, **kwargs):
        context= {'extend':'base.html',}
        obj = self.get_obj()
        if obj is not None:
            try:
                obj.personalStatus = "read"
                obj.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='نوبت ممیزی  جدید با موفقیت ساخته شد !!!')
                return redirect('ProfileHome') 
            except:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='نوبت ممیزی  مورد نظر ساخته نشد !')           
            
        return redirect('ProfileHome') 

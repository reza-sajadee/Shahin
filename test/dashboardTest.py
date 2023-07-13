
class ViewCommitteeDashboard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "clearDashboard.html"
    extend = 'baseEmployee.html'
    menuBack ="ViewMomayeziDashboard"
    
 
    def get(self, request ,*args, **kwargs):
        
       
        selectedType =  request.GET.get('type') 
        createNewProfile = None
        allProfile = None
        responsible_link = None
        member_link =  None
     
        partials = 'partials/committeeDashboard.html'
        header_title = "کمیته ها و کارگروه های سازمان"
       
        #دریافت تمام داده ها
        member = Profile.objects.get(user = request.user)
        
        if(request.user.is_superuser):
            responsible_link = None
            member_link = None
            createNewProfile = None
     
      
        
        
       
       
       
       
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
     
     
        
        context = {'extend':self.extend , 'menuBack':self.menuBack,'riskDabir':is_dabir(self), 'header_title':header_title,'member_link':member_link,
        'discribtion':discribtion,'icon_name':icon_name,'header_title':header_title,'responsible_link':responsible_link ,
        'color':color  ,'partials':partials,'createNewProfile':createNewProfile,'allProfile':allProfile
        }

        return render(request,self.template_name,context)
    
    
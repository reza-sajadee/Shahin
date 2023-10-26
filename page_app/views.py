
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View



from django.contrib.auth.mixins import LoginRequiredMixin




from profile_app.decorators import  staff_only



class aboutUs( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "about.html"
    @staff_only 
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)

class strategyPlan( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "strategyPlan.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
    @staff_only 
    def get(self, request,*args, **kwargs):
        
        color         = "info"
        header_title  = "برنامه راهبردی"
        context = {'extend':self.extend , 'menuBack':self.menuBack, 'header_title':header_title,
        'header_title':header_title,'color':color }
        return render(request,self.template_name , context)
    

class stockHolders( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "stockHolders.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
    @staff_only 
    def get(self, request,*args, **kwargs):
        
       
        color         = "info"
        header_title  = "ذی نفعان سازمان "
        context = {'extend':self.extend , 'menuBack':self.menuBack, 'header_title':header_title,
        'header_title':header_title,'color':color }
        return render(request,self.template_name , context)
    

class modelProccess( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "modelProccess.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
    @staff_only 
    def get(self, request,*args, **kwargs):
        
       
        color         = "info"
        header_title  = "مدل فرآیندی"
        context = {'extend':self.extend , 'menuBack':self.menuBack, 'header_title':header_title,
        'header_title':header_title,'color':color }
        return render(request,self.template_name , context)
    

class mostanadChange( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "mostanadChange.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
    @staff_only 
    def get(self, request,*args, **kwargs):
        
       
        color         = "info"
        header_title  = "درخواست تهیه / تغییر در مدرک "
        context = {'extend':self.extend , 'menuBack':self.menuBack, 'header_title':header_title,
        'header_title':header_title,'color':color }
        return render(request,self.template_name , context)
    
    

class performanceIndex( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "performanceIndex.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
    @staff_only 
    def get(self, request,*args, **kwargs):
        
       
        color         = "info"
        header_title  = "شاخص عملکردی"
        context = {'extend':self.extend , 'menuBack':self.menuBack, 'header_title':header_title,
        'header_title':header_title,'color':color }
        return render(request,self.template_name , context)
    
    

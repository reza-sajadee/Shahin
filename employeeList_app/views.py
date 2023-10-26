from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CreateFormEmployeeList
from .models import EmployeeList

from django.views.generic import ListView
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from risk_app.utils import is_dabir

class EmployeeListHome( LoginRequiredMixin,View):
    template_name = "EmployeeList.html"
    redirect_field_name = '/profile/login'
    extend='base.html'
    def get(self, request,*args, **kwargs):
        
        context = {'extend':self.extend,'riskDabir':is_dabir(self),}
        return render(request,self.template_name , context)


class treeEmployeeList( LoginRequiredMixin,View):
    extend='base.html'
    template_name = "treechart.html"
    redirect_field_name = '/profile/login'
    def get(self, request, *args, **kwargs):
        
        queryset = EmployeeList.objects.all()
    
        employees = []
        
        data = []
        for query in queryset:
            
            data.append(query.firstName)
            data.append(query.lastName)
            data.append(query.employeeNumber)
            data.append(query.superiorNumber)
            
            employees.append({'firstName' :  query.firstName , 'lastName' : query.lastName  , 'employeeNumber' : query.employeeNumber ,  })
        tree = []
     

        employees = data
        header_title  = "ساخت یک کارمند جدید "
        discribtion   = "جهت ایجاد یک کارمند جدید ، موارد خواسته شده را تکمیل نمایید"
        icon_name     = "person_add"
        columns       = 1
        color         = "success"
        contex = { 'header_title':header_title,'extend':self.extend,'riskDabir':is_dabir(self),
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'employees' : employees  ,'object_list':json.dumps(tree) ,"tree":tree}
        return render(request,self.template_name,contex )



class CreateViewEmployeeList( LoginRequiredMixin,View):
    extend='base.html'
    template_name = "create.html"
    redirect_field_name = '/profile/login'
    def get(self, request, *args, **kwargs):
        
        form = CreateFormEmployeeList()
        header_title  = "ساخت یک کارمند جدید "
        discribtion   = "جهت ایجاد یک کارمند جدید ، موارد خواسته شده را تکمیل نمایید"
        icon_name     = "person_add"
        columns       = 1
        color         = "success"
        contex = {'form': form, 'header_title':header_title,'extend':self.extend,'riskDabir':is_dabir(self),
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        form = CreateFormEmployeeList(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            sweetify.toast(self.request,timer=30000 , icon="success",title ='کارمند جدید با موفقیت ساخته شد !!!')
            return redirect('ListViewEmployeeList')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='کارمند مورد نظر ساخته نشد !')
        context = {'form': form,'extend':self.extend,'riskDabir':is_dabir(self),}
        return render(request,self.template_name,context)


class ListViewEmployeeList(ListView):
  

    extend='base.html'
    def get_context_data(self, **kwargs):
        header_title  = "لیست کارمند ها"
        discribtion   = "در این بخش لیست تمام کارمند ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        icon_name     = "table_chart"
        columns       = 1
        color         = "info"
        header_table   = ['نام','نام خانوادگی','کد ملی' , 'کد پرسنلی' ]
        #object_name    = ['firstName','lastName','idNumber','employeeList' , 'created_at' , 'updated_at' , 'superiorNumber']
        
        context = super().get_context_data(**kwargs)
        queryset = EmployeeList.objects.all()
        list_data = []
        
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.firstName)
            data.append(query.lastName)
            data.append(query.idNumber)
            data.append(query.employeeNumber)

            
            dict_temp = {query.id : data}
            list_data.append(dict_temp)

        context = { 'header_title':header_title,'extend':self.extend,'riskDabir':is_dabir(self),
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,
        'list_data' : list_data}
        return context

    model = EmployeeList
    ordering = '-created_at' 
    template_name ='list.html'

class UpdateViewEmployeeList( LoginRequiredMixin,View):
    template_name = "create.html"
    redirect_field_name = '/profile/login'
    extend='base.html'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(EmployeeList,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormEmployeeList(instance=obj)
            obj = get_object_or_404(EmployeeList,id = id)
            header_title  = "ویرایش کارمند "
            discribtion   = "جهت ویرایش این کارمند ، موارد جدید را وارد کنید"
            icon_name     = "person_add"
            color         = "info"
            columns       = 1
            context =  {'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns,'extend':self.extend,'riskDabir':is_dabir(self),}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormEmployeeList(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='کارمند جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewEmployeeList')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='کارمند مورد نظر ساخته نشد !')           
            context = {'form': form,'object':obj,'extend':self.extend,'riskDabir':is_dabir(self),}
        return render(request,self.template_name,context)



class DeleteViewEmployeeList( LoginRequiredMixin,View):
    extend='base.html'
    template_name = "delete.html"
    redirect_field_name = '/profile/login'
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(EmployeeList,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            header_title  = "پاک کردن یک کارمند"
            discribtion   = "آیا می خواهید که کارمند  " + obj.firstName + " "  + " را پاک کنید   ؟"
            icon_name     = "delete_forever"
            color         = "danger"
            context       = {'object': obj, 'header_title':header_title,'extend':self.extend,'riskDabir':is_dabir(self),
            'discribtion':discribtion,'icon_name':icon_name , 'color':color}
            
        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='کارمند با موفقیت پاک شد !!!')
            context = {'extend':self.extend,'riskDabir':is_dabir(self),}
            return redirect('ListViewEmployeeList')
        return render(request,self.template_name,context)
    
    

@permission_classes((permissions.AllowAny,))    
class ChartData(APIView):

    
    def get(self, request, format=None):
       
       
        queryset = EmployeeList.objects.all()
        firstName =[]
        lastName =[]
        employeeNumber =[]
        parentNumber = []

        for employee in queryset:
            firstName.append(employee.firstName)
            lastName.append(employee.firstName)
            employeeNumber.append(employee.firstName)
            parentNumber.append(employee.firstName)
 



        data = {
        "firstName" : firstName,
        "lastName" : lastName,
        "employeeNumber" : employeeNumber,
        "parentNumber" : parentNumber,
       
        }
        return Response(data)
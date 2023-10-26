from django.shortcuts import render
from .models import BeneficiaryList , Beneficiary , GroupBeneficiary ,CurrentNeed ,FutureExpectations
from django.views.generic import ListView
# Create your views here.

class ListViewBeneficiaryList(ListView):
  
    extend = 'baseEmployee.html'
  
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست ذی نفعان سازمان"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام ارزیابی ریسک سوال  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
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
        header_title  = "لیست ذی نفعان سازمان"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام ارزیابی ریسک سوال  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
    
        #اسم داده های جدول

        #دریافت تمام داده ها
        listData = []
        allBeneficiary = Beneficiary.objects.all()
        allGroup = GroupBeneficiary.objects.all()
        allCurrentNeed = CurrentNeed.objects.all()
        allFutureExpectations = FutureExpectations.objects.all()
        for group in allGroup:
            selectedBeneficiary = allBeneficiary.filter(groupRelated = group)
            listData.append((group.title , group.classificationRelated.title  ,selectedBeneficiary , allCurrentNeed.filter(beneficiaryRelated = selectedBeneficiary[0]) , allFutureExpectations.filter(beneficiaryRelated = selectedBeneficiary[0])  ))
            
     
        #ایجاد لیست داده ها
        
        #دیکشنری داده ها
        context= {'extend':self.extend, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color ,
            'listData' : listData }
        return context

    model = BeneficiaryList
    ordering = '-created_at' 
    template_name ='listBeneficiary.html'


from django.contrib import messages
import sweetify
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse

from organization_app.models import TypePostSazmani , Vahed , JobBank , Post , Hoze

from standardTable_app.models import RequirementStandards , Standard

from .forms import CreateFormCorrectiveAction ,CreateFormCorrectiveAction2
from .models import CorrectiveAction ,CorrectiveActionActivityManager ,TextDataBase , ConfirmationDataBase
from profile_app.decorators import  staff_only
from profile_app.models import Profile

from django.views.generic import ListView
import json
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from jalali_date import datetime2jalali, date2jalali
from datetime import timedelta
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from project_app.models import PlanProfile
from performanceIndex_app.utils import jalali_to_gregorian
import datetime
from notifications_app.models import Notifications
#تایپ


class test( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    template_name = "CorrectiveAction.html"
    def get(self, request,*args, **kwargs):
        #CorrectiveActionActivityManager.objects.create( sender =  , reciver =  , status =  , activity =  , CorrectiveActionRelated =  , texts =  , previousActivity =  , nextActivity =  , confirmations =  )
        import pandas as pd
        newData = pd.read_excel("c:/666.xlsx")
        counter = 0
        for index, row in newData.iterrows():
            counter = (counter +2)
            demdVahed = Vahed.objects.get(id=21)
            standardSelected = Standard.objects.get(id = 1)
            profile246 = Profile.objects.get(id = 246)
            profile298 = Profile.objects.get(id = 298)
            profile105 = Profile.objects.get(id = 105)
            vahEu = Vahed.objects.get(id = row['c'])
            proEuM = Profile.objects.get(id =row['d'] )
            proEu = Profile.objects.get(id =row['e'] )
            firstCA = CorrectiveAction.objects.create(problem = 'correctiveAction',demandantVahed =demdVahed ,demandantId ='Ca-00' +str(index)  ,standardRelated =standardSelected ,source ='MomayeziDakheli' ,vahed =vahEu  )
            secondCA = CorrectiveAction.objects.create(problem = 'Correction',demandantVahed =demdVahed ,demandantId ='Ca-00' +str(index + 1) ,standardRelated =standardSelected ,source ='MomayeziDakheli' , vahed =vahEu, owner = proEu , deadLine = '1401-12-29' , effective = True )
            acRegister = CorrectiveActionActivityManager.objects.create( sender =profile246  , reciver =profile246  , status ='done'  , activity ='register'  , CorrectiveActionRelated =firstCA  ,     )
            texts = TextDataBase.objects.create(title = 'شرح مسئله / درخواست' ,text = row['a'] ) 
            acRegister.texts.set([texts,])
            acRegister.save()
           
            acBf = CorrectiveActionActivityManager.objects.create( sender =profile246  , reciver =profile298  , status ='done'  , activity ='barresiMafogh'  , CorrectiveActionRelated =firstCA  , confirmations = ConfirmationDataBase.objects.create(title =  'بررسی درخواست توسط مافوق',profile =profile298  ,confirm ='yes' )     , previousActivity =acRegister )
            acRegister.nextActivity = acBf
            acRegister.save()

            acBm = CorrectiveActionActivityManager.objects.create( sender =profile246  , reciver =profile298  , status ='done'  , activity ='barresiModir'  , CorrectiveActionRelated =firstCA  , confirmations = ConfirmationDataBase.objects.create(title =  'بررسی درخواست توسط مدیر',profile =profile298  ,confirm ='yes' )     , previousActivity =acBf )
            acBf.nextActivity = acBm
            acBf.save()

            acEu = CorrectiveActionActivityManager.objects.create( sender =profile246  , reciver =profile298  , status ='done'  , activity ='executiveUnit'  , CorrectiveActionRelated =firstCA     , previousActivity =acBm )
            acBm.nextActivity = acEu
            acBm.save()

            acBMoa = CorrectiveActionActivityManager.objects.create( sender =profile246  , reciver =profile105  , status ='done'  , activity ='barresiMoaven'  , CorrectiveActionRelated =firstCA     , previousActivity =acEu )
            acEu.nextActivity = acBMoa
            acEu.save()

            acCa = CorrectiveActionActivityManager.objects.create( sender =profile246  , reciver =proEuM  , status ='doing'  , activity ='cause'  , CorrectiveActionRelated =firstCA     , previousActivity =acBMoa )
            acBMoa.nextActivity = acCa
            acBMoa.save()


            # acDca = CorrectiveActionActivityManager.objects.create( sender =proEuM  , reciver =proEuM  , status ='done'  , activity ='definitionCorrectiveaAtion'  , CorrectiveActionRelated =firstCA     , previousActivity =acCa  )
            # texts = TextDataBase.objects.create(title = 'علت یابی اقدام اصلاحی' ,text = row['g'] ) 
            # acDca.texts.set([texts,])
            # acDca.save()
            # acCa.nextActivity = acDca
            # acCa.save()


            # acEjr = CorrectiveActionActivityManager.objects.create( sender =profile246  , reciver =proEu  , status ='done'  , activity ='ejraNatije'  , CorrectiveActionRelated =secondCA     , previousActivity =acDca  )
            # texts = TextDataBase.objects.create(title = 'نتیجه نهایی ',text = row["h"] ) 
            # acEjr.texts.set([texts,])
            # acEjr.save()

            # acCrmot = CorrectiveActionActivityManager.objects.create( sender =profile246  , reciver =proEu  , status ='done'  , activity ='confirmRiportMotevali'  , CorrectiveActionRelated =secondCA     , previousActivity =acEjr ,confirmations =  ConfirmationDataBase.objects.create(title = 'مدیر دفتر توسعه و تحقیقات' ,profile = profile298 ,confirm ="yes" )  )
            # acDca.nextActivity = acCrmot
            # acDca.save()


            # acCrmodir = CorrectiveActionActivityManager.objects.create( sender =profile246  , reciver =proEu  , status ='completed'  , activity ='confirmRiportModir'  , CorrectiveActionRelated =secondCA     , previousActivity =acCrmot  )
            # acCrmot.nextActivity = acCrmodir
            # acCrmot.save()
        return redirect('ViewCorrectiveActionDashboard')
      
class CorrectiveActionHome( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    template_name = "CorrectiveAction.html"
    def get(self, request,*args, **kwargs):
        

        return render(request,self.template_name)

    
 
class ViewCorrectiveActionDashboard( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    template_name = "clearDashboard.html"
    extend = 'baseEmployee.html'
    menuBack = 'ViewRiskDashboard'
    
    @staff_only 
    def get(self, request ,*args, **kwargs):
        userProfile = Profile.objects.get(user=self.request.user)
        visio = 'مدیریت بهبود.vsdx'
        allActivity = CorrectiveActionActivityManager.objects.all().filter(~Q(status = 'done'))
        allLenghtDo = len(allActivity.filter(Q(status='doing') ))
        partials = 'partials/correctiveDashboard.html'
        allCorrective = CorrectiveAction.objects.all()
        allCorrectiveAction = allCorrective.filter(problem ='correctiveAction' )
        allCorrection = allCorrective.filter(problem = 'Correction')
        
        allCreatedAction = {}
        allComplated = {}
        profileSelected = None
        responsibleCount = 0
        memberCount = 0
        createNewProfile = 'createViewCorrectiveAction'
        allProfile=['1402',]
        if(request.user.is_superuser):
            activityNotDone = allActivity.filter(status='doing' )
        else:
            activityNotDone = allActivity.filter(Q(reciver = userProfile) & Q(status='doing') )
       
        responsible_link = None
        member_link =  'ListViewCorrectiveActionDoing'
        if(len(activityNotDone) >0):
            memberCount = len(activityNotDone)
            member_link = 'ListViewCorrectiveActionDoing'    
        # if(jobBankSelected in profileRiskSelected.committeeRisk.members.all()):
        #     member_link = 'ViewRiskDashboardMember'
        summary = dict.fromkeys(('all' , 'ca' , 'c' , 'e' , 'ie' , 'comp'))
        summary['all'] = 0
        summary['ca'] = 0
        summary['c'] = 0
        summary['e'] = 0
        summary['ie'] = 0
        summary['comp'] = 0
        allSource = {'data':[] , 'labels':[]}
        
        allHozeData ={'data':[] , 'labels':[] , 'all' :[]}
        for source in CorrectiveAction.SOURCE_TYPE :
            if(len(allCorrective.filter(source = str(source[0]))) == 0):
                continue
            allSource['data'].append(len(allCorrective.filter(source = str(source[0]))))
            allSource['labels'].append(source[1])
         
            
        for activity in allActivity:
            allCreatedAction[activity.firstStep().CorrectiveActionRelated.id] = activity.lastStep().CorrectiveActionRelated
            
            if(activity.lastStep().status == 'completed'):
                
                allComplated[activity.lastStep().id] = activity.lastStep()
        for key , value in allComplated.items():
          
            if(value.CorrectiveActionRelated.effective == True):
                
                summary['e'] = summary['e'] + 1
            if(value.CorrectiveActionRelated.effective == False):
                summary['ie'] = summary['ie'] + 1
            if(value.CorrectiveActionRelated.problem == 'correctiveAction'):
                summary['ca'] = summary['ca'] + 1
            if(value.CorrectiveActionRelated.problem == 'Correction'):
                summary['c'] = summary['c'] + 1
            
            if(value.CorrectiveActionRelated.source == 'MomayeziDakheli'):
                #allHoze['MomayeziDakheli'] += 1
                pass
        allHoze = Hoze.objects.all()      
        tempValue = []
        for hoze in allHoze:
            allHozeData['labels'].append(hoze.title)
            allHozeData['data'].append( len(allCorrective.filter(vahed__hoze=hoze)))
            tempValue.append( (len(allCorrective.filter(vahed__hoze=hoze).filter(effective = True))
                                        , len(allCorrective.filter(vahed__hoze=hoze).filter(effective = False))
                                        , len(allCorrective.filter(vahed__hoze=hoze)) - len(allCorrective.filter(vahed__hoze=hoze).filter(effective = False)) -(len(allCorrective.filter(vahed__hoze=hoze).filter(effective = True)) )))
        jariList = []
        efList = []
        nEfList = []
        for temp in tempValue:
            jariList.append(temp[2])
            efList.append(temp[0])
            nEfList.append(temp[1])
 
        allHozeData['all'] = ( jariList,efList ,nEfList)
        summary['all'] = len(allCreatedAction)
        summary['comp'] = len(allComplated)
        summary['incomp'] = summary['all'] - summary['comp']
        
        
        dictData = {'summary' : summary , 'allSource' :allSource  }
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "اقدامات اصلاحی در یک نگاه "
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ویرایش این مستند داخلی  ، موارد جدید را وارد کنید"
        #آیکون نمایش داده شده در بخش بالای سایت            
        icon_name     = "person_add"
        #تعداد ستون ها            
        color         = "info"
        
        
        
        
            
        
        #رنگ             
        columns       = 1
        
        maxGhovatValue = [10,5,7]
        
        #رنگ             
        columns       = 1
        #دیکشنری داده ها
        context = {'extend':self.extend , 'menuBack':self.menuBack, 'header_title':header_title,'profileSelected':profileSelected,'createNewProfile':createNewProfile,
        'discribtion':discribtion,'icon_name':icon_name,'header_title':header_title,'responsible_link':responsible_link,'member_link':member_link,
        'columns':columns , 'color':color ,'partials':partials,'dictData':dictData,'allHozeData':allHozeData, 'maxGhovatValue':maxGhovatValue , 'allProfile':allProfile , 'allLenghtDo':allLenghtDo, 'responsibleCount':responsibleCount,'memberCount':memberCount , 'visio':visio
        }

        return render(request,self.template_name,context)
    

class CreateViewCorrectiveAction( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "correctiveActionCreate.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    def getMafogh(self ,profileSender):
        psotMafoghSelected = JobBank.objects.all().filter(profile=profileSender)[0].jobBankPost.postMafogh
        jobBankMafoghSelected = JobBank.objects.all().filter(jobBankPost = psotMafoghSelected)[0]

        profileReciver = jobBankMafoghSelected.profile
        return profileReciver
    def get(self, request, *args, **kwargs):
        form = CreateFormCorrectiveAction()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ثبت اطلاعات پایه اقدام اصلاحی"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک اقدام اصلاحی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menu_link':self.menu_link,'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color}
        return render(request,self.template_name,contex)


    def post(self, request, *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormCorrectiveAction(request.POST,request.FILES)
        
        profileSender  = Profile.objects.filter(user=self.request.user)[0]
        profileReciver = self.getMafogh(profileSender)
        #بررسی صحت اطلاعات ورودی
        if form.is_valid():
            f = form.save()
            f.demandantId = 'CA-' + str(f.id)
            f.save()

            textBox = TextDataBase.objects.create(title = 'شرح مسئله / درخواست' , text = request.POST.get('description'))
            

            instanceCorrectiveActionActivityManagerRegister = CorrectiveActionActivityManager.objects.create(reciver = profileSender , sender  = profileSender ,status='done', activity = 'register' , CorrectiveActionRelated  =f ,)
            instanceCorrectiveActionActivityManagerRegister.texts.add(textBox)
            
            instanceCorrectiveActionActivityManagerRegister.save()
            instanceCorrectiveActionActivityManager = CorrectiveActionActivityManager.objects.create(reciver = profileReciver , sender  = profileSender , activity = 'barresiMafogh',previousActivity = instanceCorrectiveActionActivityManagerRegister , CorrectiveActionRelated  =f)
            
            instanceCorrectiveActionActivityManager.save()
            instanceCorrectiveActionActivityManagerRegister.nextActivity = instanceCorrectiveActionActivityManager
            instanceCorrectiveActionActivityManagerRegister.save()
            #تابع نمایش پیغام
            sweetify.toast(self.request,timer=30000 , icon="success",title ='اقدام اصلاحی  جدید با موفقیت ساخته شد !!!')
            return redirect('ViewCorrectiveActionDashboard')
        else :
            sweetify.toast(self.request,timer=30000 , icon="error",title ='اقدام اصلاحی  مورد نظر ساخته نشد !')
        context = {'extend':self.extend,'form': form }
        return render(request,self.template_name,context)



class ListViewCorrectiveActionDoing(ListView):
  

    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست اقدام اصلاحی  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام اقدام اصلاحی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        
        #اسم داده های جدول

        #دریافت تمام داده ها
        typeList = self.request.GET.get('type')
        list_data = []
        userProfile = Profile.objects.get(user=self.request.user)
        
        #queryset = CorrectiveActionActivityManager.objects.all().filter(status='doing').filter(reciver = userProfile )
        if(typeList == 'all'):
            queryset = CorrectiveActionActivityManager.objects.all().filter(Q(status='doing') | Q(status='completed'))
            

        else:
            queryset = CorrectiveActionActivityManager.objects.all().filter(Q(status='doing') )
            header_table   = [ 'کد اقدام' ,'عنوان' , 'مرحله اقدام' , 'گیرنده' ,  ]
            for query in queryset:
                if(query.reciver == userProfile or userProfile.user.is_superuser):
                    data = []
                    dict_temp = {}
                    data.append(query.CorrectiveActionRelated.demandantId)
                    data.append(query.firstStep().texts.all()[0].text)
                    
                
                    data.append(query.get_activity_display)
                    data.append(query.reciver)          
                    dict_temp = {query.id : data}
                    list_data.append(dict_temp)
        
       
        
        #ایجاد لیست داده ها
        
        #دیکشنری داده ها
        context = { 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,'typeList':typeList,'queryset':queryset,
        'columns':columns , 'color':color  ,'done' : True
          ,  'list_data' : list_data ,'extend':self.extend , 'menu_link':self.menu_link , 'userProfile' : userProfile , }
        return context

    model = CorrectiveAction
    ordering = 'created_at' 
    template_name ='correctiveActionListStep.html'


class ListViewCorrectiveActionDone(ListView):
  

    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    def get_context_data(self, **kwargs):
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "لیست اقدام اصلاحی  ها"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "در این بخش لیست تمام اقدام اصلاحی  ها را می توانید مشاهده کنید ،جهت جستجو و یا گرفتن خروجی از گزینه های زیر می توانید داستفاده کنید "
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "table_chart"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        #عنوان های جدول
        header_table   = ['کد اقدام' , 'واحد مجری ' , 'عنوان' , ]
        #اسم داده های جدول

        #دریافت تمام داده ها
        
        list_data = []
        userProfile = Profile.objects.filter(user=self.request.user)[0]
        selectedE =  self.request.GET.get('e') 
        if(selectedE == 'True'):
            
            queryset = CorrectiveActionActivityManager.objects.all().filter(Q(status='completed') & Q(CorrectiveActionRelated__effective = True))
            
        elif(selectedE == 'False'):
            queryset = CorrectiveActionActivityManager.objects.all().filter(Q(status='completed') & Q(CorrectiveActionRelated__effective = False))
        else:
            queryset = CorrectiveActionActivityManager.objects.all().filter(status='completed')
        
        icon = 'view'
        
        #ایجاد لیست داده ها
        for query in queryset:
            data = []
            dict_temp = {}
            data.append(query.CorrectiveActionRelated.demandantId)
            
            data.append(query.CorrectiveActionRelated.vahed.title)
            data.append(query.firstStep().texts.all()[0].text)
         

   
            
 

         
            
           
            dict_temp = {query.id : data}
            list_data.append(dict_temp)
        #دیکشنری داده ها
        context = { 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name,
        'columns':columns , 'color':color , 'header_table': header_table ,'icon' : icon
          ,  'list_data' : list_data ,'extend':self.extend , 'menu_link':self.menu_link}
        return context

    model = CorrectiveAction
    ordering = '-created_at' 
    template_name ='correctiveActionListDone.html'




class CreateViewCorrectiveActionStep( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    #قالب کلی ایجاد 
    template_name = "correctiveCreateStep2.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    def getMafogh(self ,profileSender):
        psotMafoghSelected = JobBank.objects.all().filter(profile=profileSender)[0].jobBankPost.postMafogh
        jobBankMafoghSelected = JobBank.objects.all().filter(jobBankPost = psotMafoghSelected)[0]

        profileReciver = jobBankMafoghSelected.profile
        return profileReciver
    def saveing(self ,activitySelected , text  , profileSender , profileReciver ,confirm , titleText  ,nextStep ,file=None ,nextFailStep=None ,profileReciverField=None ):  
        if(confirm =='yes'):
            
                
            CorrectiveChangeSelected = activitySelected.CorrectiveActionRelated
            cdb = ConfirmationDataBase.objects.create( title =titleText ,profile =profileReciver  ,confirm =confirm ,text = text ) 
            activitySelected.confirmations=cdb
            activitySelected.status = 'done'
            instancCorrectiveChangeActivityManager = CorrectiveActionActivityManager.objects.create(reciver = profileReciver , sender  = profileSender , activity = nextStep,previousActivity = activitySelected , CorrectiveActionRelated  =activitySelected.CorrectiveActionRelated)
            activitySelected.nextActivity = instancCorrectiveChangeActivityManager
            if(file != None):
                activitySelected.file = file
            activitySelected.save()
            instancCorrectiveChangeActivityManager.save()
            return True
        elif(confirm =='no'):
            activitySelected.status = 'completed'
            if  text != None:
                
                activitySelected.texts.add(TextDataBase.objects.create(title =titleText , text= text))
            activitySelected.save()
            return False
        elif(confirm =='completed'):
            if  text != None:
                activitySelected.texts.add(TextDataBase.objects.create(title =titleText , text= text))
            activitySelected.status = 'completed'
            activitySelected.save()
            return True
        else:
            cdb = ConfirmationDataBase.objects.create( title =titleText ,profile =profileReciver  ,confirm ='no' ,text = text ) 
            activitySelected.confirmations=cdb
            activitySelected.status = 'done'
            instancCorrectiveChangeActivityManager = CorrectiveActionActivityManager.objects.create(reciver = profileReciverField , sender  = profileSender , activity = nextFailStep,previousActivity = activitySelected ,  CorrectiveActionRelated  =activitySelected.CorrectiveActionRelated)
            activitySelected.nextActivity = instancCorrectiveChangeActivityManager
            activitySelected.save()
            instancCorrectiveChangeActivityManager.save()
    def get(self, request, activityId,*args, **kwargs):
        form = CreateFormCorrectiveAction()
        #عنوان نمایش داده شده در بالای صفحه
        header_title  = "ثبت اطلاعات پایه اقدام اصلاحی"
        #توضحات نمایش داده شده در زیر عنوان
        discribtion   = "جهت ایجاد یک اقدام اصلاحی  جدید ، موارد خواسته شده را تکمیل نمایید"
        #آیکون نمایش داده شده در بخش بالای سایت
        icon_name     = "person_add"
        #تعداد ستون ها
        columns       = 1
        #رنگ 
        color         = "info"
        texts = []
        boolians = []
        confirmation = ''
        fields = ''
        cause = ''
        profiles = ''
        definitionCorrectiveaAtion = ''
        profilesPosts = ''
        filedSelected = ''
        activitySelected = CorrectiveActionActivityManager.objects.all().filter(id = activityId)[0]
        
     #   queryset = MostanadatDakheli.objects.all()

        firstActivity = activitySelected.firstStep()
        all = activitySelected.listActivity()
        allVahed = Vahed.objects.all()
        allPostType  =  TypePostSazmani.objects.all()
        profilesPosts = Profile.objects.all()
        allSystem    = Standard.objects.all()
      #  allType   = TypeMadrak.objects.all()

        vahedSelected = None



       
       
            
            


        if(activitySelected.activity == 'barresiMoaven'):
            vahedSelected = activitySelected.findStep('executiveUnit').CorrectiveActionRelated.vahed
            dataSet = [{'1- نام واحد درخواست کننده ' : activitySelected.CorrectiveActionRelated.demandantVahed.title , '2- نوع مسئله ' :activitySelected.CorrectiveActionRelated.get_problem_display }
            
            ,{'3- کد درخواست' :activitySelected.CorrectiveActionRelated.demandantId } 
            ,{'4- مرتبط با سیستم ' : activitySelected.CorrectiveActionRelated.standardRelated.standardTitlePersian , '5- منشا بروز ' : activitySelected.CorrectiveActionRelated.get_source_display} 
            ,{'6- شرح مسئله / درخواست ' :activitySelected.findStep('register').texts.all()[0].text}
            ,{'7-  بررسی درخواست توسط مافوق:  عدم انطباق مورد تایید می‌باشد؟ بلی    ' : 'توسط '  + activitySelected.findStep('barresiMafogh').confirmations.profile.lastName + ' ' +  activitySelected.findStep('barresiMafogh').confirmations.profile.firstName + ' ' + 'مورد تایید قرار گرفت' + '( ' + activitySelected.findStep('barresiMafogh').confirmations.text + ' )'} 
            ,{'8-  بررسی درخواست توسط مدیر دفتر توسعه مدیریت و تحقیقات :  عدم انطباق مورد تایید می‌باشد؟ بلی    ' : 'توسط '  + activitySelected.findStep('barresiModir').confirmations.profile.lastName + ' ' +  activitySelected.findStep('barresiModir').confirmations.profile.firstName + ' ' + 'مورد تایید قرار گرفت' + '( ' + activitySelected.findStep('barresiModir').confirmations.text + ' )'} 
            ,{'9-  واحد مجری  : '  : activitySelected.findStep('executiveUnit').CorrectiveActionRelated.vahed } ]
            title = '10- آیا واحد مجری انتخاب شده توسط مدیر دفتر توسعه مدیریت و تحقیقات مورد تایید است ؟ '
            fields = Vahed.objects.all()
            filedSelected = vahedSelected.id
            texts = []
            boolians = []
            confirmation = '321'
       
      
        
       
        

        #دیکشنری داده ها
        contex = {'extend':self.extend , 'menu_link':self.menu_link,'form': form, 'header_title':header_title,
        'discribtion':discribtion,'icon_name':icon_name ,
        'columns' : columns , 'color' : color , 'activitySelected':activitySelected , 'texts' : texts,'boolians' : boolians,
        'confirmation' : confirmation , 'fields' : fields ,'cause' :cause , 'profilesPosts':profilesPosts , 'definitionCorrectiveaAtion' : definitionCorrectiveaAtion , 'filedSelected' : filedSelected,
        'firstActivity':firstActivity ,'all':all , 'allVahed':allVahed,'allSystem':allSystem , 'allPostType' : allPostType , 'profilesPosts':profilesPosts , 'vahedSelected' : vahedSelected} 
        return render(request,self.template_name,contex)


    def post(self, request,activityId , *args, **kwargs):
        #فرم دریافت شده
        form = CreateFormCorrectiveAction(request.POST,request.FILES)
        profileReciver = Profile.objects.filter(id=321)[0]
        profileSender  = Profile.objects.filter(user=self.request.user)[0]
        activitySelected = CorrectiveActionActivityManager.objects.all().filter(id = activityId)[0]
        CorrectiveActionSelected = activitySelected.CorrectiveActionRelated
        modirToseProfile = Profile.objects.all().filter(id =298 )[0]
        karshenasProfile = Profile.objects.all().filter(id =246 )[0]
        moavenProfile = Profile.objects.all().filter(id =105 )[0]

        if(activitySelected.activity == 'register' and activitySelected.previousActivity ==None):    
        #بررسی صحت اطلاعات ورودی
            if form.is_valid():
                f = form.save()
                f.demandantId = 'CA-' + str(f.id)
                f.save()
                instanceCorrectiveActionActivityManagerRegister = CorrectiveActionActivityManager.objects.create(reciver = profileSender , sender  = profileSender ,status='done', activity = 'register' , CorrectiveActionRelated  =f ,)
                instanceCorrectiveActionActivityManagerRegister.save()
                instanceCorrectiveActionActivityManager = CorrectiveActionActivityManager.objects.create(reciver = self.getMafogh(profileSender) , sender  = profileSender , activity = 'description',previousActivity = instanceCorrectiveActionActivityManagerRegister , CorrectiveActionRelated  =f)
                instanceCorrectiveActionActivityManager.save()
                instanceCorrectiveActionActivityManagerRegister.nextActivity = instanceCorrectiveActionActivityManager
                instanceCorrectiveActionActivityManagerRegister.save()
                #تابع نمایش پیغام
                sweetify.toast(self.request,timer=30000 , icon="success",title ='اقدام اصلاحی  جدید با موفقیت ساخته شد !!!')
                return redirect('ViewCorrectiveActionDashboard')
            else :
                sweetify.toast(self.request,timer=30000 , icon="error",title ='اقدام اصلاحی  مورد نظر ساخته نشد !')
        elif(activitySelected.activity == 'register' and activitySelected.previousActivity !=None):
           
            result = self.saveing(activitySelected , text = request.POST.get('description') ,  profileSender = profileSender , profileReciver = self.getMafogh(profileSender) , confirm = request.POST.get('submit')  , titleText = 'اصلاحات توسط درخواست کننده' , nextStep = 'barresiMafogh',nextFailStep = 'description'  )
            if(result):
                sweetify.toast(self.request,timer=30000 , icon="success",title ='اقدام اصلاحی توسط مافوق مورد تایید قرار گرفت!!!')
            else:
                sweetify.toast(self.request,timer=30000 , icon="warning",title ='اقدام اصلاحی توسط مافوق مورد تایید قرار گرفت!!!')
            return redirect('ViewCorrectiveActionDashboard')
        if(activitySelected.activity == 'description'):
           
            result = self.saveing(activitySelected , text = request.POST.get('description') ,  profileSender = profileSender , profileReciver = self.getMafogh(profileSender) , confirm = request.POST.get('submit')  , titleText = 'بررسی درخواست توسط مافوق' , nextStep = 'barresiMafogh',nextFailStep = 'description'  )
            if(result):
                sweetify.toast(self.request,timer=30000 , icon="success",title ='اقدام اصلاحی به روزشد!!!')
            else:
                sweetify.toast(self.request,timer=30000 , icon="warning",title ='اقدام اصلاحی توسط مافوق مورد تایید قرار گرفت!!!')
            return redirect('ViewCorrectiveActionDashboard')
        if(activitySelected.activity == 'barresiMafogh'):
           
            result = self.saveing(activitySelected , text = request.POST.get('description') ,  profileSender = profileSender , profileReciver = modirToseProfile , confirm = request.POST.get('submit')  , titleText = 'بررسی درخواست توسط مافوق' , nextStep = 'barresiModir',nextFailStep = 'description' ,profileReciverField=activitySelected.firstStep().sender )
            if(result):
                sweetify.toast(self.request,timer=30000 , icon="success",title ='اقدام اصلاحی توسط مافوق مورد تایید قرار گرفت!!!')
            else:
                sweetify.toast(self.request,timer=30000 , icon="warning",title ='اقدام اصلاحی توسط مافوق مورد تایید قرار گرفت!!!')
            return redirect('ViewCorrectiveActionDashboard')

         
        if(activitySelected.activity == 'barresiModir'):
            result = self.saveing(activitySelected , text = request.POST.get('description') ,  profileSender = profileSender , profileReciver = modirToseProfile , confirm = request.POST.get('submit')  , titleText = 'بررسی درخواست توسط مدیر' , nextStep = 'executiveUnit',nextFailStep = 'complate' ,profileReciverField=self.getMafogh(activitySelected.firstStep().sender) )
            if(result):
                sweetify.toast(self.request,timer=30000 , icon="success",title ='اقدام اصلاحی   مورد تایید مدیر دفتر توسعه مدیریت و تحقیقات قرار گرفت!!!')
            else:
                sweetify.toast(self.request,timer=30000 , icon="warning",title ='اقدام اصلاحی   مورد تایید مدیر دفتر توسعه مدیریت و تحقیقات قرار گرفت!!!')
            return redirect('ViewCorrectiveActionDashboard')
        if(activitySelected.activity == 'executiveUnit'):
            if(request.POST.get('submit') =='yes'):
                vahedId = request.POST.get('vahedMortabetCode')
                vahedSelected = Vahed.objects.all().filter(id = vahedId)[0]
                activitySelected.status = 'done'
                
                CorrectiveActionSelected.vahed =  vahedSelected
                CorrectiveActionSelected.save()
                
                

                instanceCorrectiveActionActivityManager = CorrectiveActionActivityManager.objects.create(reciver = moavenProfile , sender  = profileSender , activity = 'barresiMoaven',previousActivity = activitySelected , CorrectiveActionRelated  =activitySelected.CorrectiveActionRelated)
                activitySelected.nextActivity = instanceCorrectiveActionActivityManager
                activitySelected.save()
                instanceCorrectiveActionActivityManager.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='مجری اقدام اصلاحی مشخص شد!!!')
                return redirect('ViewCorrectiveActionDashboard')
            else:
                return redirect('ViewCorrectiveActionDashboard')
        if(activitySelected.activity == 'barresiMoaven'):
            if(request.POST.get('submit') =='yes'):
                
                texts = request.POST.get('description')
                vahedId = request.POST.get('vahedMortabetCode')
                vahedSelected = Vahed.objects.all().filter(id = vahedId)[0]
                CorrectiveActionSelected.vahed =  vahedSelected
                CorrectiveActionSelected.save()
                
                activitySelected.status = 'done'
                postSelected = Post.objects.all().filter(vahed =vahedSelected ).filter(PostTypePostSazmani =vahedSelected.typePostSazmani )[0]
                profileSelected = JobBank.objects.all().filter(jobBankPost =postSelected )[0].profile
                

                instanceCorrectiveActionActivityManager = CorrectiveActionActivityManager.objects.create(reciver = profileSelected , sender  = profileSender , activity = 'cause',previousActivity = activitySelected , CorrectiveActionRelated  =activitySelected.CorrectiveActionRelated)
                activitySelected.nextActivity = instanceCorrectiveActionActivityManager
                activitySelected.save()
                instanceCorrectiveActionActivityManager.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='اقدام اصلاحی توسط معاون مورد تایید قرار گرفت!!!')
                return redirect('ViewCorrectiveActionDashboard')
            else:
               
                return redirect('ViewCorrectiveActionDashboard')        
        if(activitySelected.activity == 'cause'):
            if(request.POST.get('submit') =='yes'):
                if(len(request.FILES)!=0):
                    document = request.FILES['document']
                    activitySelected.file = document
                
                textBox = TextDataBase.objects.create(title = 'علت یابی اقدام اصلاحی' , text = request.POST.get('causeAnswer'))
                activitySelected.status = 'done'

                activitySelected.texts.add(textBox)
                
                
                
                profileSender = activitySelected.reciver

                instanceCorrectiveActionActivityManager = CorrectiveActionActivityManager.objects.create(reciver = profileSender , sender  = profileSender , activity = 'definitionCorrectiveaAtion',previousActivity = activitySelected , CorrectiveActionRelated  =activitySelected.CorrectiveActionRelated )
                activitySelected.nextActivity = instanceCorrectiveActionActivityManager
                activitySelected.save()
                instanceCorrectiveActionActivityManager.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='نیاز به علت یابی و حل مسئله توسط واحد متولی انجام شد !!!')
                return redirect('ViewCorrectiveActionDashboard')
            else:
                return redirect('ViewCorrectiveActionDashboard')
        if(activitySelected.activity == 'definitionCorrectiveaAtion'):
            if(request.POST.get('submit') =='yes'):
                try:
                    if request.POST["correctiveAction"]:
                        


                        ProfileId = request.POST["correctiveActionProfile"]
                        ProfileSelectedEntered = Profile.objects.all().filter(id =ProfileId )[0]
                        DateEntered = request.POST.get("correctiveActionDate" )
                        DescriptionEntered = request.POST["correctiveActionDescription"]
                        gor = jalali_to_gregorian(int(DateEntered.split('-')[0]) , int(DateEntered.split('-')[1]), int(DateEntered.split('-')[2]) )
                        gorDate = datetime.date(year =gor[0]  , month =gor[1] , day =gor[2] )
                        
                        jobBankProfileSelectedEntered = JobBank.objects.get(profile = ProfileSelectedEntered)
                        textBox = TextDataBase.objects.create(title = 'علت یابی اقدام اصلاحی' , text = DescriptionEntered)
                        instanceCorrectiveAction = CorrectiveAction.objects.create( problem = 'correctiveAction', demandantVahed = activitySelected.CorrectiveActionRelated.demandantVahed ,standardRelated = activitySelected.CorrectiveActionRelated.standardRelated ,source = activitySelected.CorrectiveActionRelated.source,vahed = activitySelected.CorrectiveActionRelated.vahed ,owner = ProfileSelectedEntered ,deadLine = gorDate )
                        instanceCorrectiveAction.problem = 'correctiveAction'
                        instanceCorrectiveAction.save()
                        instanceCorrectiveAction.demandantId = 'CA-' + str(instanceCorrectiveAction.id)
                        instanceCorrectiveAction.save()
                        instanceCorrectiveActionActivityManager = CorrectiveActionActivityManager.objects.create(reciver = ProfileSelectedEntered , sender  = profileSender , activity = 'ejraNatije',previousActivity = activitySelected , CorrectiveActionRelated  =instanceCorrectiveAction )
                        instanceCorrectiveActionActivityManager.texts.add(textBox)
                        instanceCorrectiveActionActivityManager.save()
                        try:
                            if request.POST["PlanProfileCorrectiveAction"]:
                                instancePlanProfile = PlanProfile.objects.create(title ='برنامه اجرایی مرتبط با اقدام اصلاحی ' + instanceCorrectiveAction.demandantId  ,responsible =jobBankProfileSelectedEntered  , description = DescriptionEntered,sourcePlan = 'corrective' ,startTiem = instanceCorrectiveAction.created_at ,deadLine = gorDate)
                                Notifications.objects.create( title = 'در اقدام اصلاحی کد ' +instanceCorrectiveAction.demandantId +' یک برنامه اجرایی مرتبط با اقدام تعریف شده درخواست شده است . لطفا بررسی نمایید.' , recivers = jobBankProfileSelectedEntered.profile )
                        except:
                            pass
                       
                            
                        
                except:
                    pass
                try:
                    if request.POST["corrective"]:
                        ProfileId = request.POST["correctiveProfile"]
                        ProfileSelectedEntered = Profile.objects.all().filter(id =ProfileId )[0]
                        DateEntered = request.POST.get("correctiveDate" )
                        DescriptionEntered = request.POST["correctiveDescription"]
                        gor = jalali_to_gregorian(int(DateEntered.split('-')[0]) , int(DateEntered.split('-')[1]), int(DateEntered.split('-')[2]) )
                        gorDate = datetime.date(year =gor[0]  , month =gor[1] , day =gor[2] )

                        jobBankProfileSelectedEntered = JobBank.objects.get(profile = ProfileSelectedEntered)
                        textBox = TextDataBase.objects.create(title = 'علت یابی اصلاح' , text = DescriptionEntered)
                        instanceCorrectiveAction = CorrectiveAction.objects.create( problem = 'Correction', demandantVahed = activitySelected.CorrectiveActionRelated.demandantVahed ,standardRelated = activitySelected.CorrectiveActionRelated.standardRelated ,source = activitySelected.CorrectiveActionRelated.source,vahed = activitySelected.CorrectiveActionRelated.vahed ,owner = ProfileSelectedEntered ,deadLine = gorDate )
                        instanceCorrectiveAction.problem = 'Correction'
                        instanceCorrectiveAction.save()
                        instanceCorrectiveAction.demandantId = 'CA-' + str(instanceCorrectiveAction.id)
                        instanceCorrectiveAction.save()
                        instanceCorrectiveActionActivityManager = CorrectiveActionActivityManager.objects.create(reciver = ProfileSelectedEntered , sender  = profileSender , activity = 'ejraNatije',previousActivity = activitySelected , CorrectiveActionRelated  =instanceCorrectiveAction )
                        instanceCorrectiveActionActivityManager.texts.add(textBox)
                        instanceCorrectiveActionActivityManager.save()
                        try:
                            if request.POST["PlanProfileCorrective"]:
                                instancePlanProfile = PlanProfile.objects.create(title ='برنامه اجرایی مرتبط با درخواست اصلاح ' + instanceCorrectiveAction.demandantId  ,responsible =jobBankProfileSelectedEntered  , description = DescriptionEntered,sourcePlan = 'corrective' ,startTiem = instanceCorrectiveAction.created_at ,deadLine = gorDate)
                                Notifications.objects.create( title = 'در درخواست اصلاحی کد ' +instanceCorrectiveAction.demandantId +' یک برنامه اجرایی مرتبط با اقدام تعریف شده درخواست شده است . لطفا بررسی نمایید.' , recivers = jobBankProfileSelectedEntered.profile )

                        except:
                            pass
                except:
                    pass
                activitySelected.status = 'done'
                activitySelected.save()
                
                

                
                sweetify.toast(self.request,timer=30000 , icon="success",title ='مسئول و مدت انجام اقدام مشخص گردید !!!')
                return redirect('ViewCorrectiveActionDashboard')
            else:
                return redirect('ViewCorrectiveActionDashboard')
        if(activitySelected.activity == 'ejraNatije'):
            if(request.POST.get('submit') =='yes'):
                
                textBox = TextDataBase.objects.create(title = 'شرح اقدام اصلاحی / اصلاح انجام شده' , text = request.POST.get('description'))
                activitySelected.status = 'done'

                activitySelected.texts.add(textBox)
             
                if(len(request.FILES)!=0):
                    document = request.FILES['document']
                    activitySelected.file = document
                profileReciver = activitySelected.findStep('cause').reciver
                instanceCorrectiveActionActivityManager = CorrectiveActionActivityManager.objects.create(reciver = profileReciver , sender  = profileSender , activity = 'confirmRiportMotevali',previousActivity = activitySelected , CorrectiveActionRelated  =activitySelected.CorrectiveActionRelated )
                activitySelected.nextActivity = instanceCorrectiveActionActivityManager
                activitySelected.save()
                instanceCorrectiveActionActivityManager.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='شرح اقدام اصلاحی / اصلاح انجام شده   توسط واحد مجری ثبت شد !!!')
                return redirect('ViewCorrectiveActionDashboard')
            else:
                return redirect('ViewCorrectiveActionDashboard')
        if(activitySelected.activity == 'confirmRiportMotevali'):
            if(request.POST.get('submit') =='yes'):
                result = self.saveing(activitySelected , text = request.POST.get('description') ,  profileSender = profileSender , profileReciver = modirToseProfile , confirm = request.POST.get('submit')  , titleText = 'مدیر دفتر توسعه مدیریت و تحقیقات' , nextStep = 'confirmRiportModir',nextFailStep = 'ejraNatije' ,profileReciverField=activitySelected.previousActivity.sender )
            else:
                textBox = TextDataBase.objects.create(title = 'شرح اقدام اصلاحی / اصلاح انجام شده' , text = request.POST.get('description'))
                activitySelected.status = 'done'

                activitySelected.texts.add(textBox)
             
                if(len(request.FILES)!=0):
                    document = request.FILES['document']
                    activitySelected.file = document
                profileReciver = activitySelected.findStep('ejraNatije').reciver
                instanceCorrectiveActionActivityManager = CorrectiveActionActivityManager.objects.create(reciver = profileReciver , sender  = profileSender , activity = 'ejraNatije',previousActivity = activitySelected , CorrectiveActionRelated  =activitySelected.CorrectiveActionRelated )
                activitySelected.nextActivity = instanceCorrectiveActionActivityManager
                activitySelected.save()
                instanceCorrectiveActionActivityManager.save()
                result=False
            if(result):
                sweetify.toast(self.request,timer=30000 , icon="success",title ='اقدام اصلاحی توسط مافوق مورد تایید قرار گرفت!!!')
            else:
                sweetify.toast(self.request,timer=30000 , icon="warning",title ='اقدام اصلاحی توسط مافوق مورد تایید قرار گرفت!!!')
            return redirect('ViewCorrectiveActionDashboard')
            
        if(activitySelected.activity == 'confirmRiportModir'):
            result = self.saveing(activitySelected , text = request.POST.get('description') ,  profileSender = profileSender , profileReciver = profileReciver , confirm = request.POST.get('submit')  , titleText = 'بررسی نتیجه توسط مدیر دفتر بهبود' , nextStep = 'complate',nextFailStep = 'ejraNatije'  )
            if(result):
                sweetify.toast(self.request,timer=30000 , icon="success",title ='اقدام اصلاحی توسط مدیر  مورد تایید قرار گرفت!!!')
            else:
                sweetify.toast(self.request,timer=30000 , icon="warning",title ='اقدام اصلاحی توسط مورد مورد تایید قرار گرفت!!!')
            return redirect('ViewCorrectiveActionDashboard')
        context = {'extend':self.extend,'form': form }
        return render(request,self.template_name,context)




class UpdateViewCorrectiveAction( LoginRequiredMixin,View): 
    redirect_field_name = '/profile/login'
    template_name = "create.html"
    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    def get_obj(self):
        
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(CorrectiveAction,id = id)
        return obj

    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            form = CreateFormCorrectiveAction(instance=obj)
            
            obj = get_object_or_404(CorrectiveAction,id = id)
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "ویرایش اقدام اصلاحی  "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "جهت ویرایش این اقدام اصلاحی  ، موارد جدید را وارد کنید"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "person_add"
            #تعداد ستون ها            
            color         = "info"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context =  {'form': form,'object':obj , 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name,
            'color':color , 'columns':columns ,'extend':self.extend , 'menu_link':self.menu_link}


        return render(request,self.template_name,context)
    
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            form = CreateFormCorrectiveAction(request.POST or request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                sweetify.toast(self.request,timer=30000 , icon="success",title ='اقدام اصلاحی  جدید با موفقیت ساخته شد !!!')
                return redirect('ListViewCorrectiveActionDoing')
            else:
                sweetify.toast(self.request,timer=30000 , icon="error",title ='اقدام اصلاحی  مورد نظر ساخته نشد !')           
            context = {'form': form,'object':obj ,'extend':self.extend , 'menu_link':self.menu_link}
        return render(request,self.template_name,context)



class DeleteViewCorrectiveAction( LoginRequiredMixin,View):
    redirect_field_name = '/profile/login'
    extend = 'baseEmployee.html'
    menu_link = 'ViewCorrective'
    template_name = "delete.html"
    #تایع یافتن رکورد خاص
    def get_obj(self):
        id = self.kwargs.get('id')
        obj=None
        if id is not None:
            obj = get_object_or_404(CorrectiveAction,id = id)
        return obj
    def get(self, request,id=None ,*args, **kwargs):

        obj = self.get_obj()
        if obj is not None:
            #عنوان نمایش داده شده در بالای صفحه
            header_title  = "پاک کردن یک اقدام اصلاحی "
            #توضحات نمایش داده شده در زیر عنوان
            discribtion   = "آیا می خواهید که اقدام اصلاحی   " + obj.problem + " "  + " را پاک کنید   ؟"
            #آیکون نمایش داده شده در بخش بالای سایت            
            icon_name     = "delete_forever"
            #تعداد ستون ها            
            color         = "danger"
            #رنگ             
            columns       = 1
            #دیکشنری داده ها
            context       = {'object': obj, 'header_title':header_title,
            'discribtion':discribtion,'icon_name':icon_name , 'color':color ,'extend':self.extend , 'menu_link':self.menu_link}
            
        return render(request,self.template_name,context)
    def post(self, request,id=None ,*args, **kwargs):
        context = {}
        obj = self.get_obj()
        if obj is not None:
            obj.delete()
            sweetify.toast(self.request,timer=30000 , icon="warning",title ='اقدام اصلاحی  با موفقیت پاک شد !!!')
            context ={'extend':self.extend , 'menu_link':self.menu_link}
            return redirect('ListViewCorrectiveActionDoing')
        return render(request,self.template_name,context)
    
    


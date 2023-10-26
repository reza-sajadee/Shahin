
from django.contrib import admin
from django.urls import path

from .views import (

    aboutUs,
    strategyPlan,
    stockHolders,
    modelProccess,
    mostanadChange,
    performanceIndex,
    qms
)


urlpatterns = [

   
    path('qms/', qms.as_view() ,name='qms'),
    path('about/', aboutUs.as_view() ,name='aboutUs'),
    path('strategyPlan/', strategyPlan.as_view() ,name='strategyPlan'),
    path('stockHolders/', stockHolders.as_view() ,name='stockHolders'),
    path('modelProccess/', modelProccess.as_view() ,name='modelProccess'),
    path('mostanadChange/', mostanadChange.as_view() ,name='mostanadChange'),
    path('performanceIndex/', performanceIndex.as_view() ,name='performanceIndex'),

    
    
]




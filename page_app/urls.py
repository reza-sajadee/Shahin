
from django.contrib import admin
from django.urls import path

from .views import (

    aboutUs,
    strategyPlan,
    stockHolders,
    modelProccess,
)


urlpatterns = [

   
    path('about/', aboutUs.as_view() ,name='aboutUs'),
    path('strategyPlan/', strategyPlan.as_view() ,name='strategyPlan'),
    path('stockHolders/', stockHolders.as_view() ,name='stockHolders'),
    path('modelProccess/', modelProccess.as_view() ,name='modelProccess'),

    
    
]




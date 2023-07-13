
from django.contrib import admin
from django.urls import path

from .views import (
    
    

    
    ListInternalCommunications,
    ListViewExternal,
   
    
)

urlpatterns = [

    

    path('internal/', ListInternalCommunications.as_view() ,name='ListInternalCommunications'),
    path('external/', ListViewExternal.as_view() ,name='ListViewExternal'),
    
   
    

    

]




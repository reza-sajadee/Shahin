
from django.contrib import admin
from django.urls import path

from .views import (
    
    

  

    CreateViewManagementChange,
    ViewManagementChangeDashboard,
    ListViewManagementChange,
    ViewMangementChange
    
)

urlpatterns = [

    

    
    path('create', CreateViewManagementChange.as_view() ,name='CreateViewManagementChange'),
    path('dashboard', ViewManagementChangeDashboard.as_view() ,name='ViewManagementChangeDashboard'),
    path('list', ListViewManagementChange.as_view() ,name='ListViewManagementChange'),
    path('view/<int:id>', ViewMangementChange.as_view() ,name='ViewMangementChange'),
    
    
    
    
    
    

    

]




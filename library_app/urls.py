
from django.contrib import admin
from django.urls import path

from .views import (
    ListViewfileProfile,

    
   
)

urlpatterns = [


    path('list', ListViewfileProfile.as_view() ,name='ListViewfileProfile'),

    
    
]






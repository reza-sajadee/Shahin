
from django.contrib import admin
from django.urls import path

from .views import (

    ViewFaqDashboard,
    
)

urlpatterns = [

    path('', ViewFaqDashboard.as_view() ,name='ViewFaqDashboard'),
   
    
]

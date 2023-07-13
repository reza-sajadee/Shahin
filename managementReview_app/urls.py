
from django.contrib import admin
from django.urls import path

from .views import (
    CreateViewManagementReview,
    ListViewManagementReview,
    ViewManagementReview,
    
    
)


urlpatterns = [
    
    
    path('create/', CreateViewManagementReview.as_view() ,name='CreateViewManagementReview'),
    path('list/', ListViewManagementReview.as_view() ,name='ListViewManagementReview'),
    path('view/<int:inviteId>', ViewManagementReview.as_view() ,name='ViewManagementReview'),
    
    
    
]




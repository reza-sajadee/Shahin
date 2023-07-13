
from django.contrib import admin
from django.urls import path

from .views import (
    
    load_events,
    
    EventHome,
    CreateViewEvent,
    ListViewEvent,
    UpdateViewEvent,
    DeleteViewEvent,
    ListViewEvent,
    
    
    
)

urlpatterns = [
    
   
    
    
    path('', ListViewEvent.as_view() ,name='Event'),
    path('create', CreateViewEvent.as_view() ,name='CreateViewEvent'),
    path('list', ListViewEvent.as_view() ,name='ListViewEvent'),
    path('<int:id>', UpdateViewEvent.as_view(),name='UpdateViewEvent'),
    path('delete/<int:id>', DeleteViewEvent.as_view(),name='DeleteViewEvent'),
    path('json/load-events/', load_events, name='json_load_events'), # AJAX
]
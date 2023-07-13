
from django.contrib import admin
from django.urls import path

from .views import (
    

    CreateViewObjective,

    
    
    
)

urlpatterns = [
    
   
    
    
      # path('', ListViewObjective.as_view() ,name='Objective'),
      path('objective/create', CreateViewObjective.as_view() ,name='CreateViewObjective'),
#     path('list', ListViewObjective.as_view() ,name='ListViewObjective'),
#     path('<int:id>', UpdateViewObjective.as_view(),name='UpdateViewObjective'),
#     path('delete/<int:id>', DeleteViewObjective.as_view(),name='DeleteViewObjective'),
#     path('json/load-events/', load_events, name='json_load_events'), # AJAX
 ]
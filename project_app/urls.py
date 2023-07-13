
from django.contrib import admin
from django.urls import path

from .views import (
    

    CreateViewProjectProfile,
    ListViewProjectProfile,
    ListViewProject,
    CreateViewProject,
    DeleteViewProject,
    ViewProject,
    ViewPlanDashboard,
    CreateViewPlanProfile,
    ListViewPlanProfile,
    ViewPlanProfile,
    ChangeActionStatus,
    change_status,
    UpdateViewPlanProfile,
    DeleteViewAction
)

urlpatterns = [
    
   
    
    
    # path('', ListViewProject.as_view() ,name='Project'),
     path('plan/dashbaord', ViewPlanDashboard.as_view() ,name='ViewPlanDashboard'),
     path('plan/create', CreateViewPlanProfile.as_view() ,name='CreateViewPlanProfile'),
     path('plan/update/<int:id>', UpdateViewPlanProfile.as_view() ,name='UpdateViewPlanProfile'),
     path('plan/list', ListViewPlanProfile.as_view() ,name='ListViewPlanProfile'),
     path('plan/<int:id>', ViewPlanProfile.as_view() ,name='ViewPlanProfile'),
     path('plan/action/status/<int:actionId>', ChangeActionStatus.as_view() ,name='ChangeActionStatus'),
     path('plan/action/delete/<int:id>', DeleteViewAction.as_view() ,name='DeleteViewAction'),

     path('profile/create', CreateViewProjectProfile.as_view() ,name='CreateViewProjectProfile'),
     path('profile/list', ListViewProjectProfile.as_view() ,name='ListViewProjectProfile'),
     path('list', ListViewProject.as_view() ,name='ListViewProject'),
     path('<int:profileId>/create', CreateViewProject.as_view() ,name='CreateViewProject'),
     path('<int:profileId>/delete/<int:id>', DeleteViewProject.as_view() ,name='DeleteViewProject'),
     path('view/<int:id>', ViewProject.as_view() ,name='ViewProject'),
#     path('<int:id>', UpdateViewProject.as_view(),name='UpdateViewProject'),
#     path('delete/<int:id>', DeleteViewProject.as_view(),name='DeleteViewProject'),
#     path('json/load-events/', load_events, name='json_load_events'), # AJAX
 ]
htmx_urlpatterns =[
    path('change-status/' , change_status , name='change-status'),
    
]
urlpatterns += htmx_urlpatterns
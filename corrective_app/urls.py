
from django.contrib import admin
from django.urls import path

from .views import (
    
    

    
    CorrectiveActionHome,
    ViewCorrectiveActionDashboard,
    CreateViewCorrectiveAction,
    ListViewCorrectiveActionDoing,
    UpdateViewCorrectiveAction,
    DeleteViewCorrectiveAction,
    CreateViewCorrectiveActionStep,
    ListViewCorrectiveActionDone,
   
    
)

urlpatterns = [

    

    path('CorrectiveAction/dashboard', ViewCorrectiveActionDashboard.as_view() ,name='ViewCorrectiveActionDashboard'),
    path('CorrectiveAction/create', CreateViewCorrectiveAction.as_view() ,name='createViewCorrectiveAction'),
    path('CorrectiveAction/step/<int:activityId>', CreateViewCorrectiveActionStep.as_view() ,name='CreateViewCorrectiveActionStep'),
    path('CorrectiveAction/list', ListViewCorrectiveActionDoing.as_view() ,name='ListViewCorrectiveActionDoing'),
    path('CorrectiveAction/list/done', ListViewCorrectiveActionDone.as_view() ,name='ListViewCorrectiveActionDone'),
    path('CorrectiveAction/<int:id>', UpdateViewCorrectiveAction.as_view(),name='MomayeziUpdateViewCorrectiveAction'),
    path('CorrectiveAction/delete/<int:id>', DeleteViewCorrectiveAction.as_view(),name='MomayeziDeleteViewCorrectiveAction'),
    

    

]




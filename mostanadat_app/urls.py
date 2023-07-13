
from django.contrib import admin
from django.urls import path

from .views import (
    TypeMadrakHome,
    CreateViewTypeMadrak,
    ListViewTypeMadrak,
    UpdateViewTypeMadrak,
    DeleteViewTypeMadrak,
    ListViewTypeMadrak,
   
    MostanadatDakheliHome,
    CreateViewMostanadatDakheli,
    ListViewMostanadatDakheli,
    UpdateViewMostanadatDakheli,
    DeleteViewMostanadatDakheli,
    ListViewMostanadatDakheli,
    ListViewMostanadatDakheliOutdated,
    ViewMostanadatDakheli,
    ViewMostanadatDakheliOutdated,
    CreateViewMostanadatDakheliChange,
    ListViewMostanadatDakheliChangeDoing,
    CreateViewMostanadatDakheliChangeStep,
    ViewMostanadatDakheliDashboard,
    
    MostanadatKharejiHome,
    CreateViewMostanadatKhareji,
    ListViewMostanadatKhareji,
    UpdateViewMostanadatKhareji,
    DeleteViewMostanadatKhareji,
    ListViewMostanadatKhareji,
    ViewMostanadatKhareji,



    ViewRecordDataBase,
    CreateViewRecordChange,
    CreateViewRecordChangeStep,
    ListViewRecordChangeDoing,
    UpdateViewRecord,
    ViewRecordDashboard,
)

urlpatterns = [

    path('type/', ListViewTypeMadrak.as_view() ,name='TypeMadrak'),
    path('type/create', CreateViewTypeMadrak.as_view() ,name='MostanadatCreateViewTypeMadrak'),
    path('type/list', ListViewTypeMadrak.as_view() ,name='MostanadatListViewTypeMadrak'),
    path('type/<int:id>', UpdateViewTypeMadrak.as_view(),name='MostanadatUpdateViewTypeMadrak'),
    path('type/delete/<int:id>', DeleteViewTypeMadrak.as_view(),name='MostanadatDeleteViewTypeMadrak'),
    
   
    
    path('dakheli/dashboard', ViewMostanadatDakheliDashboard.as_view() ,name='ViewMostanadatDakheliDashboard'),
    path('dakheli/', ListViewMostanadatDakheli.as_view() ,name='MostanadatDakheli'),
    path('dakheli/create', CreateViewMostanadatDakheli.as_view() ,name='MostanadatCreateViewDakheli'),
    path('dakheli/change/create', CreateViewMostanadatDakheliChange.as_view() ,name='CreateViewMostanadatDakheliChange'),
    path('dakheli/change/list', ListViewMostanadatDakheliChangeDoing.as_view() ,name='ListViewMostanadatDakheliChangeDoing'),
    path('dakheli/change/step/<int:activityId>', CreateViewMostanadatDakheliChangeStep.as_view() ,name='CreateViewMostanadatDakheliChangeStep'),
    path('dakheli/list', ListViewMostanadatDakheli.as_view() ,name='MostanadatListViewDakheli'),
    path('dakheli/outdated/list', ListViewMostanadatDakheliOutdated.as_view() ,name='ListViewMostanadatDakheliOutdated'),
    path('dakheli/<int:id>', ViewMostanadatDakheli.as_view(),name='MostanadatViewDakheli'),
    path('dakheli/delete/<int:id>', DeleteViewMostanadatDakheli.as_view(),name='MostanadatDeleteViewDakheli'),
    path('dakheli/view/<int:id>', ViewMostanadatDakheli.as_view(),name='MostanadatViewDakheli'),
    path('dakheli/outdated/<int:id>', ViewMostanadatDakheliOutdated.as_view(),name='ViewMostanadatDakheliOutdated'),
    
    path('khareji/', ListViewMostanadatKhareji.as_view() ,name='MostanadatKhareji'),
    path('khareji/create', CreateViewMostanadatKhareji.as_view() ,name='MostanadatCreateViewKhareji'),
    path('khareji/list', ListViewMostanadatKhareji.as_view() ,name='MostanadatListViewKhareji'),
    path('khareji/<int:id>', UpdateViewMostanadatKhareji.as_view(),name='MostanadatUpdateViewKhareji'),
    path('khareji/delete/<int:id>', DeleteViewMostanadatKhareji.as_view(),name='MostanadatDeleteViewKhareji'),
    path('khareji/view/<int:id>', ViewMostanadatKhareji.as_view(),name='MostanadatViewKhareji'),

#

    path('record/dashboard', ViewRecordDashboard.as_view() ,name='ViewRecordDashboard'),
    path('record/list', ViewRecordDataBase.as_view() ,name='ViewRecordDataBase'),
    path('record/change/create/<int:recordId>', CreateViewRecordChange.as_view() ,name='CreateViewRecordChange'),
    path('record/change/list', ListViewRecordChangeDoing.as_view() ,name='ListViewRecordChangeDoing'),
    path('record/change/step/<int:activityId>', CreateViewRecordChangeStep.as_view() ,name='CreateViewRecordChangeStep'),
    path('record/<int:id>', UpdateViewRecord.as_view(),name='UpdateViewRecord'),
]




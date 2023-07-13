
from django.contrib import admin
from django.urls import path

from .views import (
    StandardHome,
    CreateViewStandard,
    ListViewStandard,
    UpdateViewStandard,
    DeleteViewStandard,
    ListViewStandard,
    ListViewStandardBand,
    
    StandardReferenceReleaseHome , 
    CreateViewStandardReferenceRelease , 
    ListViewStandardReferenceRelease , 
    DeleteViewStandardReferenceRelease , 
    UpdateViewStandardReferenceRelease,
)

urlpatterns = [

    path('', ListViewStandard.as_view() ,name='Standard'),
    path('create', CreateViewStandard.as_view() ,name='CreateViewStandard'),
    path('list', ListViewStandard.as_view() ,name='ListViewStandard'),
    path('list/<int:band>', ListViewStandardBand.as_view() ,name='ListViewStandardBand'),
    path('<int:id>', UpdateViewStandard.as_view(),name='UpdateViewStandard'),
    path('delete/<int:id>', DeleteViewStandard.as_view(),name='DeleteViewStandard'),
    
    path('reference/', ListViewStandardReferenceRelease.as_view() ,name='StandardReferenceRelease'),
    path('reference/create', CreateViewStandardReferenceRelease.as_view() ,name='CreateViewStandardReferenceRelease'),
    path('reference/list', ListViewStandardReferenceRelease.as_view() ,name='ListViewStandardReferenceRelease'),
    path('reference/<int:id>', UpdateViewStandardReferenceRelease.as_view(),name='UpdateViewStandardReferenceRelease'),
    path('reference/delete/<int:id>', DeleteViewStandardReferenceRelease.as_view(),name='DeleteViewStandardReferenceRelease'),
    
]





from django.contrib import admin
from django.urls import path

from .views import (
    ProcessMap,
    
    NahiyeHome,
    CreateViewNahiye,
    ListViewNahiye,
    UpdateViewNahiye,
    DeleteViewNahiye,
    ListViewNahiye,
    
    
    GroupHome,
    CreateViewGroup,
    ListViewGroup,
    UpdateViewGroup,
    DeleteViewGroup,
    ListViewGroup,
    
    ProcessHome,
    CreateViewProcess,
    ListViewProcess,
    UpdateViewProcess,
    DeleteViewProcess,
    ListViewProcess,
    
    HozeHome,
    CreateViewHoze,
    ListViewHoze,
    UpdateViewHoze,
    DeleteViewHoze,
    ListViewHoze,

  
    CreateViewProcessDocument,
    ListViewProcessDocument,
    ViewProcessDocument,
    UpdateViewProcessDocument,
    DeleteViewProcessDocument,


    ProcessDescriptionHome,
    CreateViewProcessDescription,
    ListViewProcessDescription,
    ViewProcessDescription,
    UpdateViewProcessDescription,
    DeleteViewProcessDescription,
)

urlpatterns = [
    path('map', ProcessMap.as_view() ,name='ProcessMap'),
    
    path('nahiye/', ListViewNahiye.as_view() ,name='ProcessNahiye'),
    path('nahiye/create', CreateViewNahiye.as_view() ,name='ProcessCreateViewNahiye'),
    path('nahiye/list', ListViewNahiye.as_view() ,name='ProcessListViewNahiye'),
    path('nahiye/<int:id>', UpdateViewNahiye.as_view(),name='ProcessUpdateViewNahiye'),
    path('nahiye/delete/<int:id>', DeleteViewNahiye.as_view(),name='ProcessDeleteViewNahiye'),
    
    path('group/', ListViewGroup.as_view() ,name='ProcessGroup'),
    path('group/create', CreateViewGroup.as_view() ,name='ProcessCreateViewGroup'),
    path('group/list', ListViewGroup.as_view() ,name='ProcessListViewGroup'),
    path('group/<int:id>', UpdateViewGroup.as_view(),name='ProcessUpdateViewGroup'),
    path('group/delete/<int:id>', DeleteViewGroup.as_view(),name='ProcessDeleteViewGroup'),
    
    path('', ListViewProcess.as_view() ,name='ProcessProcess'),
    path('create', CreateViewProcess.as_view() ,name='ProcessCreateViewProcess'),
    path('list', ListViewProcess.as_view() ,name='ListViewProcess'),
    path('<int:id>', UpdateViewProcess.as_view(),name='ProcessUpdateViewProcess'),
    path('delete/<int:id>', DeleteViewProcess.as_view(),name='ProcessDeleteViewProcess'),
    
    path('hoze/', ListViewHoze.as_view() ,name='ProcessHoze'),
    path('hoze/create', CreateViewHoze.as_view() ,name='ProcessCreateViewHoze'),
    path('hoze/list', ListViewHoze.as_view() ,name='ProcessListViewHoze'),
    path('hoze/<int:id>', UpdateViewHoze.as_view(),name='ProcessUpdateViewHoze'),
    path('hoze/delete/<int:id>', DeleteViewHoze.as_view(),name='ProcessDeleteViewHoze'),



    path('processdocument/create', CreateViewProcessDocument.as_view() ,name='CreateViewProcessDocument'),
    path('processdocument/list', ListViewProcessDocument.as_view() ,name='ListViewProcessDocument'),
    path('processdocument/update/<int:id>', UpdateViewProcessDocument.as_view(),name='UpdateViewProcessDocument'),
    path('processdocument/<int:id>', ViewProcessDocument.as_view(),name='ViewProcessDocument'),
    path('processdocument/delete/<int:id>', DeleteViewProcessDocument.as_view(),name='DeleteViewProcessDocument'),


    path('processdescription/create', CreateViewProcessDescription.as_view() ,name='CreateViewProcessDescription'),
    path('processdescription/list', ListViewProcessDescription.as_view() ,name='ListViewProcessDescription'),
    path('processdescription/update/<int:id>', UpdateViewProcessDescription.as_view(),name='UpdateViewProcessDescription'),
    path('processdescription/<int:id>', ViewProcessDescription.as_view(),name='ViewProcessDescription'),
    path('processdescription/delete/<int:id>', DeleteViewProcessDescription.as_view(),name='DeleteViewProcessDescription'),    
]

from django.contrib import admin
from django.urls import path

from .views import (
    EmployeeListHome,
    CreateViewEmployeeList,
    ListViewEmployeeList,
    UpdateViewEmployeeList,
    DeleteViewEmployeeList,
    ListViewEmployeeList,
    treeEmployeeList,
    ChartData,
)

urlpatterns = [

    path('', ListViewEmployeeList.as_view() ,name='EmployeeList'),
    path('create', CreateViewEmployeeList.as_view() ,name='CreateViewEmployeeList'),
    path('list', ListViewEmployeeList.as_view() ,name='ListViewEmployeeList'),
    path('list3', treeEmployeeList.as_view() ,name='treeEmployeeList'),
    path('api/chart/data/', ChartData.as_view(), name='api-ChartData'),
    path('<int:id>', UpdateViewEmployeeList.as_view(),name='UpdateViewEmployeeList'),
    
    path('delete/<int:id>', DeleteViewEmployeeList.as_view(),name='DeleteViewEmployeeList'),

]
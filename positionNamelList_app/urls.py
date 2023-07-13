
from django.contrib import admin
from django.urls import path

from .views import (
    PositionNameListHome,
    CreateViewPositionNameList,
    ListViewPositionNameList,
    UpdateViewPositionNameList,
    DeleteViewPositionNameList,
    ListViewPositionNameList,
)

urlpatterns = [

    path('', ListViewPositionNameList.as_view() ,name='PositionNameList'),
    path('create', CreateViewPositionNameList.as_view() ,name='CreateViewPositionNameList'),
    path('list', ListViewPositionNameList.as_view() ,name='ListViewPositionNameList'),
    path('<int:id>', UpdateViewPositionNameList.as_view(),name='UpdateViewPositionNameList'),
    path('delete/<int:id>', DeleteViewPositionNameList.as_view(),name='DeleteViewPositionNameList'),

]
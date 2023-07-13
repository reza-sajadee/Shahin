
from django.contrib import admin
from django.urls import path

from .views import (
    PositionLevelListHome,
    CreateViewPositionLevelList,
    ListViewPositionLevelList,
    UpdateViewPositionLevelList,
    DeleteViewPositionLevelList,
    ListViewPositionLevelList,
)

urlpatterns = [

    path('', ListViewPositionLevelList.as_view() ,name='PositionLevelList'),
    path('create', CreateViewPositionLevelList.as_view() ,name='CreateViewPositionLevelList'),
    path('list', ListViewPositionLevelList.as_view() ,name='ListViewPositionLevelList'),
    path('<int:id>', UpdateViewPositionLevelList.as_view(),name='UpdateViewPositionLevelList'),
    path('delete/<int:id>', DeleteViewPositionLevelList.as_view(),name='DeleteViewPositionLevelList'),

]
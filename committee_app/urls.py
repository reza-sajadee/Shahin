
from django.contrib import admin
from django.urls import path

from .views import (
    CommitteeHome,
    CreateViewCommittee,
    ListViewCommittee,
    EditViewCommittee,
    ViewCommittee,
    UpdateViewCommittee,
    DeleteViewCommittee,
    ListCommitteeAPI,
    DeleteViewCommitteeMember,
    ViewCommitteeDashboard,
   
)

urlpatterns = [

    path('dashboard', ViewCommitteeDashboard.as_view() ,name='ViewCommitteeDashboard'),
    path('create', CreateViewCommittee.as_view() ,name='CreateViewCommittee'),
    path('list', ListViewCommittee.as_view() ,name='ListViewCommittee'),
    path('update/<int:id>', UpdateViewCommittee.as_view(),name='UpdateViewCommittee'),
    path('<int:id>', ViewCommittee.as_view(),name='ViewCommittee'), 
    path('edit/<int:id>', EditViewCommittee.as_view(),name='EditViewCommittee'), 
    path('delete/<int:id>', DeleteViewCommittee.as_view(),name='DeleteViewCommittee'),
    path('<int:id>/delete/member/<int:jobId>/', DeleteViewCommitteeMember.as_view(),name='DeleteViewCommitteeMember'),
    
    path('api/all', ListCommitteeAPI.as_view(),name='ListCommitteeAPI'),
    path('api/createMemberCommittee/<int:id>', ListCommitteeAPI.as_view(),name='ListViewCommitteeAPI'),
    
    
]






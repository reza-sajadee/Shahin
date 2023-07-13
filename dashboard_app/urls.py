
from django.contrib import admin
from django.urls import path
from .views import (
    DashboardEmployeeHome,
    DashboardHome,
    CreateViewDasboard,
    ListViewDashboard,
    UpdateViewDashboard,
    DeleteViewDashboard,
    ListViewDashboard,
    Login,
    
    
    ViewModelProccess,
    ViewStrategyPlan,
    ViewStockHoldersOrganization,
    ViewGoalAndPlan,
    ViewProccessManagment,
    ViewAdamEntebagh,
    ViewParadigmManagment,
    ViewMomayezi,
    ViewMostanadatChange,
    ViewManagmentReview,
    ViewProfileMeeting,
    VieweMeeting,
    ViewReport,
    ViewProject,
    VieweInternalComunication,
    VieweExternalComunication,
    ViewPerformanceIndex,
    ViewCommittee,

)

urlpatterns = [

    path('', DashboardEmployeeHome.as_view() ,name='DashboardEmployee'),
    path('a/', DashboardHome.as_view() ,name='Dashboard'),
    path('login', Login.as_view() ,name='Login'),
    path('create', CreateViewDasboard.as_view() ,name='CreateViewDasboard'),
    path('list', ListViewDashboard.as_view() ,name='ListViewDashboard'),
    path('<int:id>', UpdateViewDashboard.as_view(),name='UpdateViewDashboard'),
    path('delete/<int:id>', DeleteViewDashboard.as_view(),name='DeleteViewDashboard'),

    path('basic/proccessModel', ViewModelProccess.as_view() ,name='ViewModelProccess'),
    path('basic/strategyPlan', ViewStrategyPlan.as_view() ,name='ViewStrategyPlan'),
    path('basic/stockHoldersOrganization', ViewStockHoldersOrganization.as_view() ,name='ViewStockHoldersOrganization'),
    path('qm/ViewGoalAndPlan', ViewGoalAndPlan.as_view() ,name='ViewGoalAndPlan'),
    path('qm/ViewCommittee', ViewCommittee.as_view() ,name='ViewCommittee'),
    path('qm/proccessManagment', ViewProccessManagment.as_view() ,name='ViewProccessManagment'),
    path('qm/adamEntebagh', ViewAdamEntebagh.as_view() ,name='ViewAdamEntebagh'),
    path('qm/paradigmManagment', ViewParadigmManagment.as_view() ,name='ViewParadigmManagment'),
    path('qm/Momayezi', ViewMomayezi.as_view() ,name='ViewMomayezi'),
    path('qm/PerformanceIndex', ViewPerformanceIndex.as_view() ,name='ViewPerformanceIndex'),
    path('qm/managmentReview', ViewManagmentReview.as_view() ,name='ViewManagmentReview'),
    path('mostanadat/change', ViewMostanadatChange.as_view() ,name='ViewMostanadatChange'),
    path('meeting/Profile', ViewProfileMeeting.as_view() ,name='ViewProfileMeeting'),
    path('report/', ViewReport.as_view() ,name='ViewReport'),
    path('meeting/execute', VieweMeeting.as_view() ,name='VieweMeeting'),
    path('project/menu', ViewProject.as_view() ,name='ViewProject'),
    path('comunication/internal', VieweInternalComunication.as_view() ,name='VieweInternalComunication'),
    path('comunication/external', VieweExternalComunication.as_view() ,name='VieweExternalComunication'),
]
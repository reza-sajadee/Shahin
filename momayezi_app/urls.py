
from django.contrib import admin
from django.urls import path

from .views import (
    get_json_bands_data,
    
    MomayeziTeamHome,
    CreateViewMomayeziTeam,
    ListViewMomayeziTeam,
    ViewMomayeziTeam,
    UpdateViewMomayeziTeam,
    DeleteViewMomayeziTeam,
    RegisterViewMomayeziTeamRequest,
    
    TypeMomayeziHome,
    CreateViewTypeMomayezi,
    ListViewTypeMomayezi,
    UpdateViewTypeMomayezi,
    DeleteViewTypeMomayezi,
    ListViewTypeMomayezi,
   
    ReportMomayeziHome,
    CreateViewReportMomayezi,
    ListViewReportMomayezi,
    UpdateViewReportMomayezi,
    DeleteViewReportMomayezi,
    ListViewReportMomayezi,
    
    ForsatBehbodHome,
    CreateViewForsatBehbod,
    ListViewForsatBehbod,
    UpdateViewForsatBehbod,
    DeleteViewForsatBehbod,
    ListViewForsatBehbod,
    
    
    NoghatGhovatHome,
    CreateViewNoghatGhovat,
    ListViewNoghatGhovat,
    UpdateViewNoghatGhovat,
    DeleteViewNoghatGhovat,
    ListViewNoghatGhovat,
   
    AdamEntebaghHome,
    CreateViewAdamEntebagh,
    ListViewAdamEntebagh,
    UpdateViewAdamEntebagh,
    DeleteViewAdamEntebagh,
    ListViewAdamEntebagh,
    
    
    CalenderMomayeziHome,
    CreateViewCalenderMomayezi,
    ListViewCalenderMomayezi,
    UpdateViewCalenderMomayezi,
    DeleteViewCalenderMomayezi,
    ListViewCalenderMomayezi,
    ViewCalenderMomayezi,
    ListViewCalenderMomayeziType,
    CreateViewCalenderMomayeziListType,
    
    
    
    CreateViewRoleMomayezi,
    ListViewRoleMomayezi,
    ViewRoleMomayezi,
    UpdateViewRoleMomayezi,
    DeleteViewRoleMomayezi,
    
    MomayeziActivityManagerHome,
    CreateViewMomayeziActivityManager,
    ListViewMomayeziActivityManager,
    ViewMomayeziActivityManager,
    UpdateViewMomayeziActivityManager,
    DeleteViewMomayeziActivityManager,
   
   
   
    CheckListMomayeziHome,
    ListViewCheckListMomayezi,
    ViewCheckListMomayezi,
    ViewCheckListMomayeziList,
    UpdateViewCheckListMomayezi,
    DeleteViewCheckListMomayezi,
    ListViewCheckListMomayeziSelecting,
    ChangeViewCheckListMomayeziSelecting,
    DeleteViewCheckListMomayeziCalender, 
    CreateViewCheckListQuestion,
    ListViewCheckListMomayeziEntering,

   
    CreateViewQuestionMomayeziList,
    ListViewQuestionMomayeziList,
    UpdateViewQuestionMomayeziList,
    DeleteViewQuestionMomayeziList,
    ListViewQuestionMomayeziList,
    ListViewQuestionMomayeziListVahed,
    CreateViewQuestionSelecting,


    ListViewVahedReportMomayezi,
    ViewReportMomayezi,
    ListViewReportType,
    ListViewReportEntering,
    ListViewVahedReportEnteringVahed,
    CreateViewReportEntering,
    
    
    ViewMomayeziDashboard,
    select_type_momayezi,
    
   ViewMomayeziDashboardResponsible,
    ViewMomayeziDashboardMember,
    ViewChangeMomayeziProfileStep,
    
    add_report,
)

urlpatterns = [

    path('json/get_json_band_data/<int:system>/', get_json_bands_data, name='json_load_process'), # AJAX\

    path('type/', ListViewTypeMomayezi.as_view() ,name='MomayeziTypeMomayezi'),
    path('type/create', CreateViewTypeMomayezi.as_view() ,name='MomayeziCreateViewTypeMomayezi'),
    path('type/list', ListViewTypeMomayezi.as_view() ,name='MomayeziListViewTypeMomayezi'),
    path('type/<int:id>', UpdateViewTypeMomayezi.as_view(),name='MomayeziUpdateViewTypeMomayezi'),
    path('type/delete/<int:id>', DeleteViewTypeMomayezi.as_view(),name='MomayeziDeleteViewTypeMomayezi'),
    
   
    
    path('report/', ListViewReportMomayezi.as_view() ,name='MomayeziReportMomayezi'),
    path('report/create', CreateViewReportMomayezi.as_view() ,name='MomayeziCreateViewReportMomayezi'),
    path('report/list', ListViewReportMomayezi.as_view() ,name='MomayeziListViewReportMomayezi'),
    path('report/list/type', ListViewReportType.as_view() ,name='ListViewReportType'),
    path('report/list/entering', ListViewReportEntering.as_view() ,name='ListViewReportEntering'),
    path('report/list/entering/<int:typeId>/vahed', ListViewVahedReportEnteringVahed.as_view() ,name='ListViewVahedReportEnteringVahed'),
    path('report/list/entering/<int:typeId>/<int:actId>', CreateViewReportEntering.as_view() ,name='CreateViewReportEntering'),
    path('report/list/<int:typeId>', ListViewVahedReportMomayezi.as_view() ,name='ListViewVahedReportMomayezi'),
    path('report/<int:id>', UpdateViewReportMomayezi.as_view(),name='MomayeziUpdateViewReportMomayezi'),
    path('report/view/<int:typeId>/<int:vahedId>', ViewReportMomayezi.as_view(),name='ViewReportMomayezi'),
    path('report/delete/<int:id>', DeleteViewReportMomayezi.as_view(),name='MomayeziDeleteViewReportMomayezi'),
    
    path('forsat/', ListViewForsatBehbod.as_view() ,name='MomayeziForsatBehbod'),
    path('forsat/create', CreateViewForsatBehbod.as_view() ,name='MomayeziCreateViewForsatBehbod'),
    path('forsat/list', ListViewForsatBehbod.as_view() ,name='MomayeziListViewForsatBehbod'),
    path('forsat/<int:id>', UpdateViewForsatBehbod.as_view(),name='MomayeziUpdateViewForsatBehbod'),
    path('forsat/delete/<int:id>', DeleteViewForsatBehbod.as_view(),name='MomayeziDeleteViewForsatBehbod'),
    
    
    
    path('ghovat/', ListViewNoghatGhovat.as_view() ,name='MomayeziNoghatGhovat'),
    path('ghovat/create', CreateViewNoghatGhovat.as_view() ,name='MomayeziCreateViewNoghatGhovat'),
    path('ghovat/list', ListViewNoghatGhovat.as_view() ,name='MomayeziListViewNoghatGhovat'),
    path('ghovat/<int:id>', UpdateViewNoghatGhovat.as_view(),name='MomayeziUpdateViewNoghatGhovat'),
    path('ghovat/delete/<int:id>', DeleteViewNoghatGhovat.as_view(),name='MomayeziDeleteViewNoghatGhovat'),
    
   
    
    path('adamentebagh/', ListViewAdamEntebagh.as_view() ,name='MomayeziAdamEntebagh'),
    path('adamentebagh/create', CreateViewAdamEntebagh.as_view() ,name='MomayeziCreateViewAdamEntebagh'),
    path('adamentebagh/list', ListViewAdamEntebagh.as_view() ,name='MomayeziListViewAdamEntebagh'),
    path('adamentebagh/<int:id>', UpdateViewAdamEntebagh.as_view(),name='MomayeziUpdateViewAdamEntebagh'),
    path('adamentebagh/delete/<int:id>', DeleteViewAdamEntebagh.as_view(),name='MomayeziDeleteViewAdamEntebagh'),
    
   
   
    path('calender/', ViewCalenderMomayezi.as_view() ,name='CalenderMomayezi'),
    path('calender/create', CreateViewCalenderMomayeziListType.as_view() ,name='CreateViewCalenderMomayeziListType'),
    path('calender/create/<int:typeMomayezi>', CreateViewCalenderMomayezi.as_view() ,name='CreateViewCalenderMomayezi'),
    path('calender/type', ListViewCalenderMomayeziType.as_view() ,name='ListViewCalenderMomayeziType'),
    path('calender/<int:typeMomayezi>', ViewCalenderMomayezi.as_view() ,name='ViewCalenderMomayezi'),
    #path('calender/<int:id>', UpdateViewCalenderMomayezi.as_view(),name='UpdateViewCalenderMomayezi'),
    path('calender/delete/<int:id>', DeleteViewCalenderMomayezi.as_view(),name='DeleteViewCalenderMomayezi'),
    
    path('role/', ListViewRoleMomayezi.as_view() ,name='ListViewRoleMomayezi'),
    path('role/create', CreateViewRoleMomayezi.as_view() ,name='CreateViewRoleMomayezi'),
    path('role/list', ListViewRoleMomayezi.as_view() ,name='ListViewRoleMomayezi'),
    path('role/update/<int:id>', UpdateViewRoleMomayezi.as_view(),name='UpdateViewRoleMomayezi'),
    path('role/<int:id>', ViewRoleMomayezi.as_view(),name='ViewRoleMomayezi'),
    path('role/delete/<int:id>', DeleteViewRoleMomayezi.as_view(),name='DeleteViewRoleMomayezi'),
    
    path('team/', ListViewMomayeziTeam.as_view() ,name='ListViewMomayeziTeam'),
    path('team/create', CreateViewMomayeziTeam.as_view() ,name='CreateViewMomayeziTeam'),
    path('team/list', ListViewMomayeziTeam.as_view() ,name='ListViewMomayeziTeam'),
    path('team/update/<int:id>', UpdateViewMomayeziTeam.as_view(),name='UpdateViewMomayeziTeam'),
    path('team/<int:id>', ViewMomayeziTeam.as_view(),name='ViewMomayeziTeam'),
    path('team/delete/<int:id>', DeleteViewMomayeziTeam.as_view(),name='DeleteViewMomayeziTeam'),
    path('team/request/', RegisterViewMomayeziTeamRequest.as_view(),name='RegisterViewMomayeziTeamRequest'),
    
    path('activity/create', CreateViewMomayeziActivityManager.as_view() ,name='CreateViewMomayeziActivityManager'),
    path('activity/list', ListViewMomayeziActivityManager.as_view() ,name='ListViewMomayeziActivityManager'),
    path('activity/update/<int:id>', UpdateViewMomayeziActivityManager.as_view(),name='UpdateViewMomayeziActivityManager'),
    path('activity/<int:id>', ViewMomayeziActivityManager.as_view(),name='ViewMomayeziActivityManager'),
    path('activity/delete/<int:id>', DeleteViewMomayeziActivityManager.as_view(),name='DeleteViewMomayeziActivityManager'),
    
    
    path('checklist/list/entering/<int:calenderId>', ViewCheckListMomayeziList.as_view() ,name='ViewCheckListMomayeziList'),
    #path('checklist/list/entering/<int:profileId>', ViewCheckListMomayeziList.as_view() ,name='ViewCheckListMomayeziList'),
    #path('checklist/list', ListViewCheckListMomayezi.as_view() ,name='ListViewCheckListMomayezi'),
    path('checklist/update/<int:id>', UpdateViewCheckListMomayezi.as_view(),name='UpdateViewCheckListMomayezi'),
    path('checklist/<int:id>', ViewCheckListMomayezi.as_view(),name='ViewCheckListMomayezi'),
    path('checklist/delete/<int:id>', DeleteViewCheckListMomayezi.as_view(),name='DeleteViewCheckListMomayezi'),
    path('checklist/create/delete/<int:id>', DeleteViewCheckListMomayeziCalender.as_view(),name='DeleteViewCheckListMomayeziCalender'),
    path('checklist/list/selecting/<int:profileId>', ListViewCheckListMomayeziSelecting.as_view(),name='ListViewCheckListMomayeziSelecting'),
    path('checklist/list/entering', ListViewCheckListMomayeziEntering.as_view(),name='ListViewCheckListMomayeziEntering'),
    path('checklist/<int:calenderId>/create/submit', ChangeViewCheckListMomayeziSelecting.as_view() ,name='ChangeViewCheckListMomayeziSelecting'),
    path('checklist/<int:activityId>/question', CreateViewCheckListQuestion.as_view() ,name='CreateViewCheckListQuestion'),

    path('question/', ListViewQuestionMomayeziList.as_view() ,name='QuestionMomayeziList'),
    path('question/create', CreateViewQuestionMomayeziList.as_view() ,name='CreateViewQuestionMomayeziList'),
    path('question/list', ListViewQuestionMomayeziList.as_view() ,name='ListViewQuestionMomayeziList'),
    path('question/listVahed', ListViewQuestionMomayeziListVahed.as_view() ,name='ListViewQuestionMomayeziListVahed'),
    path('question/<int:id>', UpdateViewQuestionMomayeziList.as_view(),name='UpdateViewQuestionMomayeziList'),
    path('question/delete/<int:id>', DeleteViewQuestionMomayeziList.as_view(),name='DeleteViewQuestionMomayeziList'),
    path('question/selecting/<int:vahed>', CreateViewQuestionSelecting.as_view() ,name='CreateViewQuestionSelecting'),
    path('dashboard/', ViewMomayeziDashboard.as_view() ,name='ViewMomayeziDashboard'),
    

    path('dashboard/<int:profileId>/responsible/change/<int:stepId>', ViewChangeMomayeziProfileStep.as_view() ,name='ViewChangeMomayeziProfileStep'),
    path('dashboard/<int:profileId>/responsible', ViewMomayeziDashboardResponsible.as_view() ,name='ViewMomayeziDashboardResponsible'),
    path('dashboard/<int:profileId>/member', ViewMomayeziDashboardMember.as_view() ,name='ViewMomayeziDashboardMember'),
    path('dashboard/<int:profileId>/member', ViewMomayeziDashboardMember.as_view() ,name='ViewMomayeziDashboardMember'),

]



htmx_urlpatterns =[
    path('select_type_momayezi/' , select_type_momayezi , name='select_type_momayezi'),
     path('add-report/' , add_report , name='add-report'),
  
]
urlpatterns += htmx_urlpatterns


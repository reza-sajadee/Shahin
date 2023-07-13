
from django.contrib import admin
from django.urls import path

from .views import (
    QuestionDasteHome,
    CreateViewQuestionDaste,
    ListViewQuestionDaste,
    ViewQuestionDaste,
    UpdateViewQuestionDaste,
    DeleteViewQuestionDaste,
    
    RiskProfileHome,
    CreateViewRiskProfile,
    ListViewRiskProfile,
    UpdateViewRiskProfile,
    DeleteViewRiskProfile,
    ViewRiskProfile,
    ViewRiskProfile,
    
    RiskTeamHome,
    CreateViewRiskTeam,
    ListViewRiskTeam,
    UpdateViewRiskTeam,
    DeleteViewRiskTeam,
    ListViewRiskTeam,
    
    RiskIdentificationHome,
    CreateViewRiskIdentification,
    ListViewRiskIdentification,
    UpdateViewRiskIdentification,
    DeleteViewRiskIdentification,
    ListViewRiskIdentification,
    ListRiskIdentificationAPI,
    ChangeViewRiskIdentification,
    ListViewRiskIdentificationConcule,
    
    load_process,
    get_json_group_data,
    
    RiskActivityManagerHome,
    CreateViewRiskActivityManager,
    ListViewRiskActivityManager,
    UpdateViewRiskActivityManager,
    DeleteViewRiskActivityManager,
    ListViewRiskActivityManager,
    
    
    RiskIdentificationSelectingHome,
    CreateViewRiskIdentificationSelecting,
    ListViewRiskIdentificationSelecting,
    ViewRiskIdentificationSelecting,
    UpdateViewRiskIdentificationSelecting,
    DeleteViewRiskIdentificationSelecting,

    RiskMeasurementHome,
    CreateViewRiskMeasurement,
    ListViewRiskMeasurement,
    UpdateViewRiskMeasurement,
    DeleteViewRiskMeasurement,
    ListViewRiskMeasurement,
    ChangeViewRiskMeasurement,
    
    
    RiskProcessRelatedHome,
    CreateViewRiskProcessRelated,
    ListViewRiskProcessRelated,
    UpdateViewRiskProcessRelated,
    DeleteViewRiskProcessRelated,
    ListViewRiskProcessRelated,
    
    ListViewRiskProcess,
    ViewRiskProcces,
    ListViewRiskProcess2,
    ViewRiskDashboard,
    ViewRiskDashboardResponsible,
    ViewRiskDashboardMember,
    ViewRiskMenu,
    ViewChangeRiskProfileStep,
)


urlpatterns = [
    
    
    path('', ViewRiskMenu.as_view() ,name='ViewRiskMenu'),
    
    path('create', CreateViewQuestionDaste.as_view() ,name='CreateViewQuestionDaste'),
    path('list', ListViewQuestionDaste.as_view() ,name='ListViewQuestionDaste'),
    path('update/<int:id>', UpdateViewQuestionDaste.as_view(),name='UpdateViewQuestionDaste'),
    path('<int:id>', ViewQuestionDaste.as_view(),name='ViewQuestionDaste'),
    path('delete/<int:id>', DeleteViewQuestionDaste.as_view(),name='DeleteViewQuestionDaste'),
    
    
    path('profile/', ListViewRiskProfile.as_view() ,name='RiskProfile'),
    path('profile/create', CreateViewRiskProfile.as_view() ,name='CreateViewRiskProfile'),
    path('profile/list', ListViewRiskProfile.as_view() ,name='ListViewRiskProfile'),
    path('profile/update/<int:id>', UpdateViewRiskProfile.as_view(),name='UpdateViewRiskProfile'),
    path('profile/<int:id>', ViewRiskProfile.as_view(),name='ViewRiskProfile'), 
    path('profile/delete/<int:id>', DeleteViewRiskProfile.as_view(),name='DeleteViewRiskProfile'),
    
    path('team/', ListViewRiskTeam.as_view() ,name='RiskTeam'),
    path('team/create', CreateViewRiskTeam.as_view() ,name='CreateViewRiskTeam'),
    path('team/list', ListViewRiskTeam.as_view() ,name='ListViewRiskTeam'),
    path('team/<int:id>', UpdateViewRiskTeam.as_view(),name='UpdateViewRiskTeam'),
    path('team/delete/<int:id>', DeleteViewRiskTeam.as_view(),name='DeleteViewRiskTeam'),
    
    path('identification/', ListViewRiskIdentification.as_view() ,name='RiskIdentification'),
    path('identification/<int:activityId>/create', CreateViewRiskIdentification.as_view() ,name='CreateViewRiskIdentification'),
    path('identification/<int:activityId>/create/submit', ChangeViewRiskIdentification.as_view() ,name='ChangeViewRiskActivityChange'),
    path('identification/list', ListViewRiskIdentification.as_view() ,name='ListViewRiskIdentification'),
    path('identification/<int:id>', UpdateViewRiskIdentification.as_view(),name='UpdateViewRiskIdentification'),
    path('identification/delete/<int:id>', DeleteViewRiskIdentification.as_view(),name='DeleteViewRiskIdentification'),
    path('identification/json/load-prcoess/', load_process, name='json_load_process'), # AJAX
    path('identification/json/get_json_group_data/<str:group>/', get_json_group_data, name='json_load_process'), # AJAX\
    path('identification/api/all/', ListRiskIdentificationAPI.as_view(), name='ListRiskIdentificationAPI'), # AJAX\
    
    path('identification/conclude/<int:id>', ListViewRiskIdentificationConcule.as_view() ,name='ListViewRiskIdentificationConclude'),
    
    
    
    path('activity/', ListViewRiskActivityManager.as_view() ,name='RiskActivityManager'),
    path('activity/create', CreateViewRiskActivityManager.as_view() ,name='CreateViewRiskActivityManager'),
    path('activity/list', ListViewRiskActivityManager.as_view() ,name='ListViewRiskActivityManager'),
    path('activity/<int:id>', UpdateViewRiskActivityManager.as_view(),name='UpdateViewRiskActivityManager'),
    path('activity/delete/<int:id>', DeleteViewRiskActivityManager.as_view(),name='DeleteViewRiskActivityManager'),
    
    path('identification/selecting/', ListViewRiskIdentificationSelecting.as_view() ,name='RiskIdentificationSelecting'),
    path('identification/selecting/<int:hoze>/create', CreateViewRiskIdentificationSelecting.as_view() ,name='CreateViewRiskIdentificationSelecting'),
    path('identification/selecting/list', ListViewRiskIdentificationSelecting.as_view() ,name='ListViewRiskIdentificationSelecting'),
    path('identification/selecting/update/<int:id>', UpdateViewRiskIdentificationSelecting.as_view(),name='UpdateViewRiskIdentificationSelecting'),
    path('identification/selecting/<int:id>', ViewRiskIdentificationSelecting.as_view(),name='ViewRiskIdentificationSelecting'),
    path('identification/selecting/delete/<int:id>', DeleteViewRiskIdentificationSelecting.as_view(),name='DeleteViewRiskIdentificationSelecting'),
    
    path('measurement/', ListViewRiskMeasurement.as_view() ,name='RiskMeasurement'),
    #path('measurement/<int:id>/create', CreateViewRiskMeasurement.as_view() ,name='CreateViewRiskMeasurement'),
    path('measurement/<int:hoze>/create', CreateViewRiskMeasurement.as_view() ,name='CreateViewRiskMeasurement'),
    path('measurement/<int:id>/submit', ChangeViewRiskMeasurement.as_view() ,name='ChangeViewRiskMeasurement'),
    path('measurement/list', ListViewRiskMeasurement.as_view() ,name='ListViewRiskMeasurement'),
    path('measurement/<int:id>', UpdateViewRiskMeasurement.as_view(),name='UpdateViewRiskMeasurement'),
    path('measurement/delete/<int:id>', DeleteViewRiskMeasurement.as_view(),name='DeleteViewRiskMeasurement'),
    
    
    path('related/', ListViewRiskProcessRelated.as_view() ,name='RiskProcessRelated'),    
    path('related/create', CreateViewRiskProcessRelated.as_view() ,name='CreateViewRiskProcessRelated'),
    path('related/list', ListViewRiskProcessRelated.as_view() ,name='ListViewRiskProcessRelated'),
    path('related/<int:id>', UpdateViewRiskProcessRelated.as_view(),name='UpdateViewRiskProcessRelated'),
    path('related/delete/<int:id>', DeleteViewRiskProcessRelated.as_view(),name='DeleteViewRiskProcessRelated'),
    
    path('dashboard/', ViewRiskDashboard.as_view() ,name='ViewRiskDashboard'),
    path('dashboard/<int:profileId>/responsible', ViewRiskDashboardResponsible.as_view() ,name='ViewRiskDashboardResponsible'),
    path('dashboard/<int:profileId>/member', ViewRiskDashboardMember.as_view() ,name='ViewRiskDashboardMember'),
    path('dashboard/<int:profileId>/responsible/change/<int:stepId>', ViewChangeRiskProfileStep.as_view() ,name='ViewChangeRiskProfileStep'),
    
    path('procces/list', ListViewRiskProcess.as_view() ,name='ListViewRiskProcess'),
    path('procces2/', ListViewRiskProcess2.as_view() ,name='ListViewRiskProcess2'),
    path('procces/<int:id>', ViewRiskProcces.as_view() ,name='ViewRiskProcces'),
    
    
    
    
]




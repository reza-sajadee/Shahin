
from django.contrib import admin
from django.urls import path

from .views import (

    CreateViewMeetingProfile,
    ListViewMeetingProfile,
    DeleteViewMeetingProfile ,
    CreateViewMeetingDate,
    ListViewMeeting,
    UpdateViewMeetingDate,
    CreateViewMeeting,
    CreateViewMeetingMembers,
    CreateViewMeetingInvitation,
    CreateViewMeetingAgenda,
    CreateViewMeetingMinute,
    CreateViewMeetingEnactment,
    CreateViewMeetingDocument,
    CreateViewMeetingPlan,
    CreateViewMeetingComplate,
    ListViewMeetingReview,
    ViewMeetingtReview,
    add_agenda,
    add_enactment,
    ViewMeetingDashboard
    # CreateViewPerformanceFormula,
    # CreateViewPerformanceVariables,
    # add_variable,
    # add_variable_toFormula,
    # delete_variable,
    # ListViewPerformanceFormula,
    # ViewPerformanceFormula,
)

urlpatterns = [

    path('dashboard', ViewMeetingDashboard.as_view() ,name='ViewMeetingDashboard'),
    path('profile/create', CreateViewMeetingProfile.as_view() ,name='CreateViewMeetingProfile'),
    path('meeting/create/<int:id>' , CreateViewMeeting.as_view() ,name='CreateViewMeeting'),
    path('profile/list', ListViewMeetingProfile.as_view() ,name='ListViewMeetingProfile'),
    path('profile/delete/<int:id>', DeleteViewMeetingProfile.as_view() ,name='DeleteViewMeetingProfile'),
    path('date/create/<int:meetingId>', CreateViewMeetingDate.as_view() ,name='CreateViewMeetingDate'),
    path('member/create/<int:meetingId>', CreateViewMeetingMembers.as_view() ,name='CreateViewMeetingMembers'),
    path('agenda/create/<int:meetingId>', CreateViewMeetingAgenda.as_view() ,name='CreateViewMeetingAgenda'),
    path('minute/create/<int:meetingId>', CreateViewMeetingMinute.as_view() ,name='CreateViewMeetingMinute'),
    path('enactment/create/<int:meetingId>', CreateViewMeetingEnactment.as_view() ,name='CreateViewMeetingEnactment'),
    path('document/create/<int:meetingId>', CreateViewMeetingDocument.as_view() ,name='CreateViewMeetingDocument'),
    path('plan/create/<int:meetingId>', CreateViewMeetingPlan.as_view() ,name='CreateViewMeetingPlan'),
    path('complate/create/<int:meetingId>', CreateViewMeetingComplate.as_view() ,name='CreateViewMeetingComplate'),
    path('invitation/create/<int:meetingId>', CreateViewMeetingInvitation.as_view() ,name='CreateViewMeetingInvitation'),
    path('profile/date/<int:id>/update', UpdateViewMeetingDate.as_view(),name='UpdateViewMeetingDate'),
    path('list', ListViewMeeting.as_view() ,name='ListViewMeeting'),
    path('review/list', ListViewMeetingReview.as_view() ,name='ListViewMeetingReview'),
    path('review/<int:meetingId>', ViewMeetingtReview.as_view() ,name='ViewMeetingtReview'),
    
]
htmx_urlpatterns =[
    path('add-agenda/' , add_agenda , name='add-agenda'),
    path('add-enactment/' , add_enactment , name='add-enactment')
]
urlpatterns += htmx_urlpatterns
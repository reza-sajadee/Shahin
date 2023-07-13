
from django.contrib import admin
from django.urls import path
from autocomplete import HTMXAutoComplete

from .views import (
    
    

    
    CreateViewReport,
    ListViewReportRequest,
    CreateViewReportUpload,
    ListViewReportDone,
    ViewReportReview,
    ViewReportDashboard
)

urlpatterns = [

    
 
    path('dashboard', ViewReportDashboard.as_view() ,name='ViewReportDashboard'),
    path('create', CreateViewReport.as_view() ,name='CreateViewReport'),
    path('<int:reportId>/upload', CreateViewReportUpload.as_view() ,name='CreateViewReportUpload'),
    path('request/list', ListViewReportRequest.as_view() ,name='ListViewReportRequest'),
    path('done/list', ListViewReportDone.as_view() ,name='ListViewReportDone'),
    path('view/<int:reportId>', ViewReportReview.as_view() ,name='ViewReportReview'),
    

    

]




"""Caspian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconfs
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls.static import static
from helpers_app.views import handle_file_not_found
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard_app.urls')),
    
    path('employeeList/', include('employeeList_app.urls')),
    
    path('news/', include('news_app.urls')),
    
    path('standard/', include('standardTable_app.urls')),
    
    path('profile/', include('django.contrib.auth.urls')),
    path('profile/', include('profile_app.urls')),
    
    path('organization/', include('organization_app.urls')),
    path('process/', include('process_app.urls')),
    path('mostanadat/', include('mostanadat_app.urls')),
    path('momayezi/', include('momayezi_app.urls')),
    path('committe/', include('committee_app.urls')),

    path('notifications/', include('notifications_app.urls')),
    path('messages/', include('messages_app.urls')),
   

       path('risk/', include('risk_app.urls')),
    path('event/', include('event_app.urls')),
    path('corrective/', include('corrective_app.urls')),
    path('management/', include('managementReview_app.urls')),
    path('beneficiary/', include('beneficiary_app.urls')),
    path('communications/', include('communications_app.urls')),
    path('performance/', include('performanceIndex_app.urls')),
    path('meeting/', include('meeting_app.urls')),
    path('report/', include('report_app.urls')),
    path('library/', include('library_app.urls')),
    path('goal/', include('goal_app.urls')),
    path('project/', include('project_app.urls')),
    path('faq/', include('faq_app.urls')),
    path('page/', include('page_app.urls')),
    path('managementChange/', include('managementChange_app.urls')),
    path('file-not-found', handle_file_not_found ,name='file_not_found'),


]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = "helpers_app.views.handle_not_found"
handler500 = "helpers_app.views.handle_server_error"
#handler404 = "helpers_app.views.handle_not_found"
#handler500 = "helpers.views.handle_server_error"
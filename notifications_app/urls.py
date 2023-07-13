from django.contrib import admin
from django.urls import path

from .views import (
    NotificationsHome,
    CreateViewNotifications,
    ListViewNotifications,
    UpdateViewNotifications,
    DeleteViewNotifications,
    ListViewAdminNotifications,
    read_notifications,
)



urlpatterns = [

    path('', ListViewAdminNotifications.as_view() ,name='Notifications'),
    path('create', CreateViewNotifications.as_view() ,name='CreateViewNotifications'),
    path('admin/list', ListViewAdminNotifications.as_view() ,name='ListViewAdminNotifications'),
    path('list', ListViewNotifications.as_view() ,name='ListViewNotifications'),
    path('read/<int:id>', read_notifications ,name='read_notifications'),
    path('<int:id>', UpdateViewNotifications.as_view(),name='UpdateViewNotifications'),
    path('delete/<int:id>', DeleteViewNotifications.as_view(),name='DeleteViewNotifications'),
]
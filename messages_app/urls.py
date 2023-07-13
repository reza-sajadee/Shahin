from django.contrib import admin
from django.urls import path

from .views import (
    MessagesHome,
    CreateViewMessages,
    ListViewMessages,
    UpdateViewMessages,
    DeleteViewMessages,
    ListViewAdminMessages,
)



urlpatterns = [

    path('', ListViewAdminMessages.as_view() ,name='Messages'),
    path('create', CreateViewMessages.as_view() ,name='CreateViewMessages'),
    path('admin/list', ListViewAdminMessages.as_view() ,name='ListViewAdminMessages'),
    path('list', ListViewMessages.as_view() ,name='ListViewMessages'),
    path('<int:id>', UpdateViewMessages.as_view(),name='UpdateViewMessages'),
    path('delete/<int:id>', DeleteViewMessages.as_view(),name='DeleteViewMessages'),
]
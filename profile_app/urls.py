
from django.contrib import admin
from django.urls import path
from .views import (
    UserRegisterView ,
    ProfileHome,
    UpdateViewNotifStatusPersonal,

)

urlpatterns = [
    path('profile/',UserRegisterView.as_view(),name='register'),
    path('<int:notifId>',UpdateViewNotifStatusPersonal.as_view(),name='UpdateViewNotifStatusPersonal'),
    path('', ProfileHome.as_view() ,name='ProfileHome'),

]
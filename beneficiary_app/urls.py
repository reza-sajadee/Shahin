
from django.contrib import admin
from django.urls import path

from .views import (
    # BeneficiaryListHome,
    # CreateViewBeneficiaryList,
    ListViewBeneficiaryList,
    # ViewBeneficiaryList,
    # UpdateViewBeneficiaryList,
    # DeleteViewBeneficiaryList,
    ListViewBeneficiary
    
    
)


urlpatterns = [
    
    
    
    
    # path('create', CreateViewBeneficiaryList.as_view() ,name='CreateViewBeneficiaryList'),
    path('list', ListViewBeneficiaryList.as_view() ,name='ListViewBeneficiaryList'),
    path('beneficiary', ListViewBeneficiary.as_view() ,name='ListViewBeneficiary'),
    # path('update/<int:id>', UpdateViewBeneficiaryList.as_view(),name='UpdateViewBeneficiaryList'),
    # path('<int:id>', ViewBeneficiaryList.as_view(),name='ViewBeneficiaryList'),
    # path('delete/<int:id>', DeleteViewBeneficiaryList.as_view(),name='DeleteViewBeneficiaryList'),
    
    
   
    
]




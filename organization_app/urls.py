
from django.contrib import admin
from django.urls import path
from autocomplete import HTMXAutoComplete
from .views import (
    
    ChartMap,
    ChartSelectedMap,
    ChartMapH,
    
    RadeHome,
    CreateViewRade,
    ListViewRade,
    UpdateViewRade,
    DeleteViewRade,
    ListViewRade,
    
    
    DasteHome,
    CreateViewDaste,
    ListViewDaste,
    UpdateViewDaste,
    DeleteViewDaste,
    ListViewDaste,
    
    HozeHome,
    CreateViewHoze,
    ListViewHoze,
    UpdateViewHoze,
    DeleteViewHoze,
    ListViewHoze,
    
    BakhshHome,
    CreateViewBakhsh,
    ListViewBakhsh,
    UpdateViewBakhsh,
    DeleteViewBakhsh,
    ListViewBakhsh,
    
    
    VahedHome,
    CreateViewVahed,
    ListViewVahed,
    UpdateViewVahed,
    DeleteViewVahed,
    ListViewVahed,
    
    
    SatheVahedHome,
    CreateViewSatheVahed,
    ListViewSatheVahed,
    UpdateViewSatheVahed,
    DeleteViewSatheVahed,
    ListViewSatheVahed,
    
    TypePostSazmaniHome,
    CreateViewTypePostSazmani,
    ListViewTypePostSazmani,
    UpdateViewTypePostSazmani,
    DeleteViewTypePostSazmani,
    ListViewTypePostSazmani,
    ListViewTypePostSazmaniClient,
    ViewTypePostSazmani,
    
    
    SathPostHome,
    CreateViewSathPost,
    ListViewSathPost,
    UpdateViewSathPost,
    DeleteViewSathPost,
    ListViewSathPost,
    
    
    IndexMahaleKhedmatHome,
    CreateViewIndexMahaleKhedmat,
    ListViewIndexMahaleKhedmat,
    UpdateViewIndexMahaleKhedmat,
    DeleteViewIndexMahaleKhedmat,
    ListViewIndexMahaleKhedmat,
    
    ListViewJobBank,
    CreateViewJobBank,
    ListViewJobBank,
    UpdateViewJobBank,
    DeleteViewJobBank,
    
    PostHome,
    CreateViewPost,
    ListViewPost,
    UpdateViewPost,
    DeleteViewPost,
    ListViewPost,
    load_Job,
)

urlpatterns = [
    
    path('json/load-job/', load_Job, name='json_load_jobs'), # AJAX
    path('json/load-job/', load_Job, name='json_load_jobs'), # AJAX
    path('post/', ListViewTypePostSazmaniClient.as_view() ,name='ListViewTypePostSazmaniClient'),
    path('map/', ChartMap.as_view() ,name='ChartMap'),
    path('maph/', ChartMapH.as_view() ,name='ChartMapH'),
    path('map/chart', ChartSelectedMap.as_view() ,name='ChartSelectedMap'),
    
    path('rade/', ListViewRade.as_view() ,name='OrganizationRade'),
    path('rade/create', CreateViewRade.as_view() ,name='OrganizationCreateViewRade'),
    path('rade/list', ListViewRade.as_view() ,name='OrganizationListViewRade'),
    path('rade/<int:id>', UpdateViewRade.as_view(),name='OrganizationUpdateViewRade'),
    path('rade/delete/<int:id>', DeleteViewRade.as_view(),name='OrganizationDeleteViewRade'),
    
    
    path('daste/', ListViewDaste.as_view() ,name='OrganizationDaste'),
    path('daste/create', CreateViewDaste.as_view() ,name='OrganizationCreateViewDaste'),
    path('daste/list', ListViewDaste.as_view() ,name='OrganizationListViewDaste'),
    path('daste/<int:id>', UpdateViewDaste.as_view(),name='OrganizationUpdateViewDaste'),
    path('daste/delete/<int:id>', DeleteViewDaste.as_view(),name='OrganizationDeleteViewDaste'),
    
    path('hoze/', ListViewHoze.as_view() ,name='OrganizationHoze'),
    path('hoze/create', CreateViewHoze.as_view() ,name='OrganizationCreateViewHoze'),
    path('hoze/list', ListViewHoze.as_view() ,name='OrganizationListViewHoze'),
    path('hoze/<int:id>', UpdateViewHoze.as_view(),name='OrganizationUpdateViewHoze'),
    path('hoze/delete/<int:id>', DeleteViewHoze.as_view(),name='OrganizationDeleteViewHoze'),
    
    path('bakhsh/', ListViewBakhsh.as_view() ,name='OrganizationBakhsh'),
    path('bakhsh/create', CreateViewBakhsh.as_view() ,name='OrganizationCreateViewBakhsh'),
    path('bakhsh/list', ListViewBakhsh.as_view() ,name='OrganizationListViewBakhsh'),
    path('bakhsh/<int:id>', UpdateViewBakhsh.as_view(),name='OrganizationUpdateViewBakhsh'),
    path('bakhsh/delete/<int:id>', DeleteViewBakhsh.as_view(),name='OrganizationDeleteViewBakhsh'),
    
    path('chartevahed/', ListViewVahed.as_view() ,name='OrganizationVahed'),
    path('chartevahed/create', CreateViewVahed.as_view() ,name='OrganizationCreateViewVahed'),
    path('chartevahed/list', ListViewVahed.as_view() ,name='OrganizationListViewVahed'),
    path('chartevahed/<int:id>', UpdateViewVahed.as_view(),name='OrganizationUpdateViewVahed'),
    path('chartevahed/delete/<int:id>', DeleteViewVahed.as_view(),name='OrganizationDeleteViewVahed'),
    
    path('sathevahed/', ListViewSatheVahed.as_view() ,name='OrganizationSatheVahedl'),
    path('sathevahed/create', CreateViewSatheVahed.as_view() ,name='OrganizationCreateViewSatheVahed'),
    path('sathevahed/list', ListViewSatheVahed.as_view() ,name='OrganizationListViewSatheVahed'),
    path('sathevahed/<int:id>', UpdateViewSatheVahed.as_view(),name='OrganizationUpdateViewSatheVahed'),
    path('sathevahed/delete/<int:id>', DeleteViewSatheVahed.as_view(),name='OrganizationDeleteViewSatheVahed'),
    
    
    path('postsazmani/', ListViewTypePostSazmani.as_view() ,name='OrganizationTypePostSazmani'),
    path('postsazmani/create', CreateViewTypePostSazmani.as_view() ,name='OrganizationCreateViewTypePostSazmani'),
    path('postsazmani/list', ListViewTypePostSazmani.as_view() ,name='OrganizationListViewTypePostSazmani'),
    path('postsazmani/<int:id>', UpdateViewTypePostSazmani.as_view(),name='OrganizationUpdateViewTypePostSazmani'),
    path('postsazmani/view/<int:postId>', ViewTypePostSazmani.as_view(),name='OrganizationViewTypePostSazmani'),
    path('postsazmani/delete/<int:id>', DeleteViewTypePostSazmani.as_view(),name='OrganizationDeleteViewTypePostSazmani'),
    
    
    
    path('sathpost/', ListViewSathPost.as_view() ,name='OrganizationSathPost'),
    path('sathpost/create', CreateViewSathPost.as_view() ,name='OrganizationCreateViewSathPost'),
    path('sathpost/list', ListViewSathPost.as_view() ,name='OrganizationListViewSathPost'),
    path('sathpost/<int:id>', UpdateViewSathPost.as_view(),name='OrganizationUpdateViewSathPosti'),
    path('sathpost/delete/<int:id>', DeleteViewSathPost.as_view(),name='OrganizationDeleteViewSathPosti'),
    
    
    path('chartePost/', ListViewPost.as_view() ,name='OrganizationPost'),
    path('chartePost/create', CreateViewPost.as_view() ,name='OrganizationCreateViewPost'),
    path('chartePost/list', ListViewPost.as_view() ,name='OrganizationListViewPost'),
    path('chartePost/<int:id>', UpdateViewPost.as_view(),name='OrganizationUpdateViewPost'),
    path('chartePost/delete/<int:id>', DeleteViewPost.as_view(),name='OrganizationDeleteViewPost'),
    
    
    
    
    path('index/', ListViewIndexMahaleKhedmat.as_view() ,name='OrganizatioIndexMahaleKhedmat'),
    path('index/create', CreateViewIndexMahaleKhedmat.as_view() ,name='OrganizationCreateVieIndexMahaleKhedmat'),
    path('index/list', ListViewIndexMahaleKhedmat.as_view() ,name='OrganizationListVieIndexMahaleKhedmat'),
    path('index/<int:id>', UpdateViewIndexMahaleKhedmat.as_view(),name='OrganizationUpdateViewIndexMahaleKhedmat'),
    path('index/delete/<int:id>', DeleteViewIndexMahaleKhedmat.as_view(),name='OrganizationDeleteViewIndexMahaleKhedmat'),

    
    path('jobBank/', ListViewJobBank.as_view() ,name='OrganizationJobBank'),
    path('jobBank/create', CreateViewJobBank.as_view() ,name='OrganizationCreateViewJobBank'),
    path('jobBank/list', ListViewJobBank.as_view() ,name='OrganizationListViewJobBank'),
    path('jobBank/<int:id>', UpdateViewJobBank.as_view(),name='OrganizationUpdateViewJobBank'),
    path('jobBank/delete/<int:id>', DeleteViewJobBank.as_view(),name='OrganizationDeleteViewJobBank'),
    
    
    

]
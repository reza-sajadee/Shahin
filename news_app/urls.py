
from django.contrib import admin
from django.urls import path

from .views import (
    CategoriyHome,
    CreateViewCategoriy,
    ListViewCategoriy,
    ViewCategoriy,
    UpdateViewCategoriy,
    DeleteViewCategoriy,
    
    
    NewsHome,
    CreateViewNews,
    ListViewNews,
    ViewNews,
    UpdateViewNews,
    DeleteViewNews,
    ArchiveViewNews,
   
)


urlpatterns = [

    path('categoriy/', ListViewCategoriy.as_view() ,name='Categoriy'),

    path('categoriy/create', CreateViewCategoriy.as_view() ,name='CreateViewCategoriy'),
    path('categoriy/list', ListViewCategoriy.as_view() ,name='ListViewCategoriy'),
    path('categoriy/<int:id>', UpdateViewCategoriy.as_view(),name='UpdateViewCategoriy'),
    #path('categoriy/<int:id>', ViewCategoriy.as_view(),name='ViewCategoriy'),
    path('categoriy/delete/<int:id>', DeleteViewCategoriy.as_view(),name='DeleteViewCategoriy'),
    
    
    
    path('', ListViewNews.as_view() ,name='News'),
    path('create', CreateViewNews.as_view() ,name='CreateViewNews'),
    path('list', ListViewNews.as_view() ,name='ListViewNews'),
    path('archive', ArchiveViewNews.as_view() ,name='ArchiveViewNews'),
    path('<int:id>', UpdateViewNews.as_view(),name='UpdateViewNews'),
    path('view/<int:id>', ViewNews.as_view(),name='ViewNews'),
    path('delete/<int:id>', DeleteViewNews.as_view(),name='DeleteViewNews'),
    
]




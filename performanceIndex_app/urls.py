
from django.contrib import admin
from django.urls import path

from .views import (

    CreateViewPerformanceIndex,
    CreateViewPerformanceFormula,
    CreateViewPerformanceVariables,
    add_variable,
    add_variable_toFormula,
    delete_variable,
    ListViewPerformanceFormula,
    ViewPerformanceFormula,
)

urlpatterns = [

   
    path('create', CreateViewPerformanceIndex.as_view() ,name='CreateViewPerformanceIndex'),
    path('formula/list', ListViewPerformanceFormula.as_view() ,name='ListViewPerformanceFormula'),
    path('formula/<int:id>', ViewPerformanceFormula.as_view() ,name='ViewPerformanceFormula'),
    path('formula/<int:performanceIndexId>/create', CreateViewPerformanceFormula.as_view() ,name='CreateViewPerformanceFormula'),
    path('formula/<int:performanceFormulaId>/variable/create', CreateViewPerformanceVariables.as_view() ,name='CreateViewPerformanceVariables'),
    path('add-variable/<int:performanceFormulaId>', add_variable ,name='add-variable'),
    path('add-variable-toFormula/<int:performanceFormulaId>/<int:variableId>', add_variable_toFormula ,name='add-variable-toFormula'),
    path('delete-variable/<int:performanceFormulaId>/<int:variableId>', delete_variable ,name='delete-variable'),
]

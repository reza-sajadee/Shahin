from django.contrib import admin
from .models import Project ,Task  , ProjectProfile , PlanProfile , Action
from import_export.admin import ImportExportModelAdmin 
from .resources import  ProjectResource , TaskResource , ProjectProfileResource , PlanProfileResource ,ActionResource


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
     list_display = ('id' ,)
     list_filter = ('id' ,)
     search_fields = ('id' ,)
     resource_class  = ProjectResource
@admin.register(Task)
class TaskAdmin(ImportExportModelAdmin):
     list_display = ('id' ,)
     list_filter = ('id' ,)
     search_fields = ('id' ,)
     resource_class  = TaskResource
@admin.register(ProjectProfile)
class ProjectProfileAdmin(ImportExportModelAdmin):
     list_display = ('id' ,)
     list_filter = ('id' ,)
     search_fields = ('id' ,)
     resource_class  = ProjectProfileResource
@admin.register(PlanProfile)
class PlanProfileAdmin(ImportExportModelAdmin):
     list_display = ('id' ,)
     list_filter = ('id' ,)
     search_fields = ('id' ,)
     resource_class  = PlanProfileResource
@admin.register(Action)
class ActionAdmin(ImportExportModelAdmin):
     list_display = ('id' ,)
     list_filter = ('id' ,)
     search_fields = ('id' ,)
     resource_class  = ActionResource

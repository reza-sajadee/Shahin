from django.contrib import admin
from .models import Standard , StandardReferenceRelease , RequirementStandards
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from standardTable_app.resources import standardTableResource , standardReferenceResource , RequirementStandardsResource
# Register your models here.standardTableResource




@admin.register(Standard)
class StandardAdmin(ImportExportModelAdmin):
     list_display = ('standardNumber','standardTitlePersian','standardTitleEnglish' ,'namad' )
     list_filter = ('standardNumber','standardTitlePersian','standardTitleEnglish' ,'namad')
     search_fields = ('standardNumber','standardTitlePersian','standardTitleEnglish' ,'namad')
     resource_class  = standardTableResource
     

@admin.register(StandardReferenceRelease)
class StandardReferenceReleaseAdmin(ImportExportModelAdmin):
     list_display = ('persianReferenceName','englishReferenceName','namad' )
     list_filter = ('persianReferenceName','englishReferenceName','namad')
     search_fields = ('persianReferenceName','englishReferenceName','namad')
     resource_class  = standardReferenceResource
     
     
@admin.register(RequirementStandards)
class RequirementStandardsAdmin(ImportExportModelAdmin):
     list_display = ('clauseNumber','title','parentClause' ,  )
     list_filter = ('standard' ,  )
     search_fields = ('clauseNumber','title','parentClause' ,  )
     resource_class  = RequirementStandardsResource
from django.contrib import admin
from .models import  BeneficiaryList ,ClassificationBeneficiary , GroupBeneficiary, Beneficiary,CurrentNeed , FutureExpectations
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .resources import BeneficiaryListResource  ,ClassificationBeneficiaryResource ,GroupBeneficiaryResource ,BeneficiaryResource ,CurrentNeedResource ,FutureExpectationsResource
# Register your models here.standardTableResource


# Register your models here.
@admin.register(BeneficiaryList)
class BeneficiaryListAdmin(ImportExportModelAdmin):
    
     resource_class  = BeneficiaryListResource
     
@admin.register(ClassificationBeneficiary)
class ClassificationBeneficiaryAdmin(ImportExportModelAdmin):
    
     resource_class  = ClassificationBeneficiaryResource
@admin.register(GroupBeneficiary)
class GroupBeneficiaryAdmin(ImportExportModelAdmin):
    
     resource_class  = GroupBeneficiaryResource
@admin.register(Beneficiary)
class BeneficiaryAdmin(ImportExportModelAdmin):
    
     resource_class  = BeneficiaryResource
@admin.register(CurrentNeed)
class CurrentNeedAdmin(ImportExportModelAdmin):
    
     resource_class  = CurrentNeedResource
@admin.register(FutureExpectations)
class FutureExpectationsAdmin(ImportExportModelAdmin):
    
     resource_class  = FutureExpectationsResource
     

    
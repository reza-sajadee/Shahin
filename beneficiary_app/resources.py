from import_export import resources
from .models import BeneficiaryList  ,ClassificationBeneficiary , GroupBeneficiary, Beneficiary,CurrentNeed ,FutureExpectations

class BeneficiaryListResource(resources.ModelResource):
     class Meta:
          model = BeneficiaryList
class ClassificationBeneficiaryResource(resources.ModelResource):
     class Meta:
          model = ClassificationBeneficiary
class GroupBeneficiaryResource(resources.ModelResource):
     class Meta:
          model = GroupBeneficiary
class BeneficiaryResource(resources.ModelResource):
     class Meta:
          model = Beneficiary
class CurrentNeedResource(resources.ModelResource):
     class Meta:
          model = CurrentNeed
class FutureExpectationsResource(resources.ModelResource):
     class Meta:
          model = FutureExpectations

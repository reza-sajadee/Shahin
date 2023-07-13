from import_export import resources
from .models import Standard , StandardReferenceRelease , RequirementStandards

class standardTableResource(resources.ModelResource):
     class Meta:
          model = Standard
          
          
class standardReferenceResource(resources.ModelResource):
     class Meta:
          model = StandardReferenceRelease
          
class RequirementStandardsResource(resources.ModelResource):
     class Meta:
          model = RequirementStandards
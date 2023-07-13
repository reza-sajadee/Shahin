from import_export import resources
from .models import Nahiye , Hoze , Group  ,Process ,ProcessDocument , ProcessDescription ,ProcessFrom ,ProcessTo

class NahiyeResource(resources.ModelResource):
     class Meta:
          model = Nahiye
          
class HozeResource(resources.ModelResource):
     class Meta:
          model = Hoze
          
class GroupResource(resources.ModelResource):
     class Meta:
          model = Group
          
          
class ProcessResource(resources.ModelResource):
     class Meta:
          model = Process

class ProcessDocumentResource(resources.ModelResource):
     class Meta:
          model = ProcessDocument

class ProcessDescriptionResource(resources.ModelResource):
     class Meta:
          model = ProcessDescription
class ProcessFromResource(resources.ModelResource):
     class Meta:
          model = ProcessFrom
class ProcessToResource(resources.ModelResource):
     class Meta:
          model = ProcessTo
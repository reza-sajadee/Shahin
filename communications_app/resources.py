from import_export import resources
from .models import External

# class CommunicationsResource(resources.ModelResource):
#      class Meta:
#           model = communications
          


class ExternalResource(resources.ModelResource):
     class Meta:
          model = External
          
          

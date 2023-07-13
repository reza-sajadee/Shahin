from import_export import resources
from .models import Faq 

class FaqResource(resources.ModelResource):
     class Meta:
          model = Faq

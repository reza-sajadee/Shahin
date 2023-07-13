from import_export import resources
from .models import Categoriy  , News

class CategoriyResource(resources.ModelResource):
     class Meta:
          model = Categoriy


class NewsResource(resources.ModelResource):
     class Meta:
          model = News
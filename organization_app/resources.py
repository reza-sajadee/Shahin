from import_export import resources

from .models import Rade,Hoze,Bakhsh,Daste,SatheVahed,TypePostSazmani,Vahed,SathPost ,IndexMahaleKhedmat,JobBank , Post , PostDescription

class RadeResource(resources.ModelResource):
     class Meta:
          model = Rade
          
class HozeResource(resources.ModelResource):
     class Meta:
          model = Hoze
          
          
class BakhshResource(resources.ModelResource):
     class Meta:
          model = Bakhsh
          
class DasteResource(resources.ModelResource):
     class Meta:
          model = Daste
          
          
class SatheVahedResource(resources.ModelResource):
     class Meta:
          model = SatheVahed
          
          
class TypePostSazmaniResource(resources.ModelResource):
     class Meta:
          model = TypePostSazmani
          
          
class VahedResource(resources.ModelResource):
     class Meta:
          model = Vahed
          
          
class SathPostResource(resources.ModelResource):
     class Meta:
          model = SathPost


class IndexMahaleKhedmatResource(resources.ModelResource):
     class Meta:
          model = IndexMahaleKhedmat
          
class JobBankResource(resources.ModelResource):
     class Meta:
          model = JobBank         
          


class PostResource(resources.ModelResource):
     class Meta:
          model = Post         
          

class PostDescriptionResource(resources.ModelResource):
     class Meta:
          model = PostDescription         
          

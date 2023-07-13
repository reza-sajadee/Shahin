from import_export import resources
from .models import TypeMadrak , MostanadatDakheli , MostanadatKhareji ,TextDataBase ,BoolDataBase ,ConfirmationDataBase,MostanadatDakheliChangeActivityManager  , MostanadatDakheliChange ,RecordDataBase ,RecordChange,RecordChangeActivityManager

class TypeMadrakResource(resources.ModelResource):
     class Meta:
          model = TypeMadrak
          
          
class MostanadatDakheliResource(resources.ModelResource):
     class Meta:
          model = MostanadatDakheli
          
          
       
class MostanadatKharejiResource(resources.ModelResource):
     class Meta:
          model = MostanadatKhareji
class TextDataBaseResource(resources.ModelResource):
     class Meta:
          model = TextDataBase
class BoolDataBaseResource(resources.ModelResource):
     class Meta:
          model = BoolDataBase
class ConfirmationDataBaseResource(resources.ModelResource):
     class Meta:
          model = ConfirmationDataBase
class MostanadatDakheliChangeActivityManagerResource(resources.ModelResource):
     class Meta:
          model = MostanadatDakheliChangeActivityManager
class MostanadatDakheliChangeResource(resources.ModelResource):
     class Meta:
          model = MostanadatDakheliChange
class RecordDataBaseResource(resources.ModelResource):
     class Meta:
          model = RecordDataBase
class RecordChangeResource(resources.ModelResource):
     class Meta:
          model = RecordChange
class RecordChangeActivityManagerResource(resources.ModelResource):
     class Meta:
          model = RecordChangeActivityManager


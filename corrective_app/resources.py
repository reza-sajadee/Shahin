from import_export import resources
from .models import CorrectiveAction , TextDataBase , BoolDataBase , CorrectiveActionActivityManager , ConfirmationDataBase

class CorrectiveActionResource(resources.ModelResource):
     class Meta:
          model = CorrectiveAction

class TextDataBaseResource(resources.ModelResource):
     class Meta:
          model = TextDataBase

class BoolDataBaseResource(resources.ModelResource):
     class Meta:
          model = BoolDataBase
class CorrectiveActionActivityManagerResource(resources.ModelResource):
     class Meta:
          model = CorrectiveActionActivityManager
class ConfirmationDataBaseResource(resources.ModelResource):
     class Meta:
          model = ConfirmationDataBase
          
    
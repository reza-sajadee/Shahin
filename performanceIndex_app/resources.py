from import_export import resources

from .models import  TextDataBase , BoolDataBase  , ConfirmationDataBase , SubjectPerformanceIndex,TopicPerformanceIndex ,PerformanceIndex , VariableDataBase,PerformanceFormula,PerformanceIndexActivityManager  ,PerformanceSettings



class PerformanceSettingsResource(resources.ModelResource):
     class Meta:
          model = PerformanceSettings
class TextDataBaseResource(resources.ModelResource):
     class Meta:
          model = TextDataBase

class BoolDataBaseResource(resources.ModelResource):
     class Meta:
          model = BoolDataBase

class ConfirmationDataBaseResource(resources.ModelResource):
     class Meta:
          model = ConfirmationDataBase
class SubjectPerformanceIndexResource(resources.ModelResource):
     class Meta:
          model = SubjectPerformanceIndex
class TopicPerformanceIndexResource(resources.ModelResource):
     class Meta:
          model = TopicPerformanceIndex
class PerformanceIndexResource(resources.ModelResource):
     class Meta:
          model = PerformanceIndex
class VariableDataBaseResource(resources.ModelResource):
     class Meta:
          model = VariableDataBase
class PerformanceFormulaResource(resources.ModelResource):
     class Meta:
          model = PerformanceFormula
class PerformanceIndexActivityManagerResource(resources.ModelResource):
     class Meta:
          model = PerformanceIndexActivityManager
          
    
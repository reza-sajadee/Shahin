from import_export import resources
from .models import QuestionDaste , RiskProfile , RiskTeam , RiskIdentification , RiskTopic , RiskActivityManager ,RiskIdentificationSelecting , RiskMeasurement , RiskProcessRelated , RiskProcess , extraData
class QuestionDasteResource(resources.ModelResource):
     class Meta:
          model = QuestionDaste

class RiskProfileResource(resources.ModelResource):
     class Meta:
          model = RiskProfile          
          


class RiskTeamResource(resources.ModelResource):
     class Meta:
          model = RiskTeam 
          


class RiskIdentificationResource(resources.ModelResource):
     class Meta:
          model = RiskIdentification 
class RiskIdentificationSelectingResource(resources.ModelResource):
     class Meta:
          model = RiskIdentificationSelecting 

class RiskTopicResource(resources.ModelResource):
     class Meta:
          model = RiskTopic         
          

class RiskActivityManagerResource(resources.ModelResource):
     class Meta:
          model = RiskActivityManager         
          
          

class RiskMeasurementResource(resources.ModelResource):
     class Meta:
          model = RiskMeasurement         
          
class RiskProcessRelatedResource(resources.ModelResource):
     class Meta:
          model = RiskProcessRelated
          
          
          
class RiskProcessResource(resources.ModelResource):
     class Meta:
          model = RiskProcess
class extraDataResource(resources.ModelResource):
     class Meta:
          model = extraData

from import_export import resources
from .models import TypeMomayezi , ReportMomayezi , ForsatBehbod ,NoghatGhovat ,AdamEntebagh ,CalenderMomayezi,RoleMomayezi , MomayeziTeam  ,MomayeziActivityManager , CheckListMomayezi , MomayeziTeamRequest , QuestionMomayeziList

class TypeMomayeziResource(resources.ModelResource):
     class Meta:
          model = TypeMomayezi
          
          
class ReportMomayeziResource(resources.ModelResource):
     class Meta:
          model = ReportMomayezi
          
          
       
class ForsatBehbodResource(resources.ModelResource):
     class Meta:
          model = ForsatBehbod
          
class NoghatGhovatResource(resources.ModelResource):
     class Meta:
          model = NoghatGhovat
          
          
       
class AdamEntebaghResource(resources.ModelResource):
     class Meta:
          model = AdamEntebagh
          
class CalenderMomayeziResource(resources.ModelResource):
     class Meta:
          model = CalenderMomayezi
          
          
class RoleMomayeziResource(resources.ModelResource):
     class Meta:
          model = RoleMomayezi
          
          
class MomayeziTeamResource(resources.ModelResource):
     class Meta:
          model = MomayeziTeam

class MomayeziTeamRequestResource(resources.ModelResource):
     class Meta:
          model = MomayeziTeamRequest
          
          
class MomayeziActivityManagerResource(resources.ModelResource):
     class Meta:
          model = MomayeziActivityManager
          
          
class CheckListMomayeziResource(resources.ModelResource):
     class Meta:
          model = CheckListMomayezi
class QuestionMomayeziListResource(resources.ModelResource):
     class Meta:
          model = QuestionMomayeziList
from import_export import resources
from .models import Project , Task , ProjectProfile , PlanProfile , Action

class ProjectResource(resources.ModelResource):
     class Meta:
          model = Project

class TaskResource(resources.ModelResource):
     class Meta:
          model = Task
class ProjectProfileResource(resources.ModelResource):
     class Meta:
          model = ProjectProfile
class PlanProfileResource(resources.ModelResource):
     class Meta:
          model = PlanProfile
class PlanProfileResource(resources.ModelResource):
     class Meta:
          model = PlanProfile
class ActionResource(resources.ModelResource):
     class Meta:
          model = Action

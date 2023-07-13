from import_export import resources
from .models import Report , ReportActivityManager

class ReportResource(resources.ModelResource):
     class Meta:
          model = Report
class ReportActivityManagerResource(resources.ModelResource):
     class Meta:
          model = ReportActivityManager

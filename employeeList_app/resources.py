from import_export import resources
from .models import EmployeeList 

class EmployeeListResource(resources.ModelResource):
     class Meta:
          model = EmployeeList
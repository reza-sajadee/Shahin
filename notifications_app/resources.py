from import_export import resources
from .models import Notifications

class NotificationsResource(resources.ModelResource):
     class Meta:
          model = Notifications
          
          

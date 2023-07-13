from import_export import resources
from .models import Messages , FileAttached

class MessagesResource(resources.ModelResource):
     class Meta:
          model = Messages
class FileAttachedResource(resources.ModelResource):
     class Meta:
          model = FileAttached
          
          

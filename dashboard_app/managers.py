from django.db import models



        
class DashboardQuerySet(models.QuerySet):
    pass
    
class DashboardManager(models.Manager):


    def get_query_set(self):
        return DashboardQuerySet(self.model)


from import_export import resources
from .models import InviteManagementReview ,ProfileManagementReview ,InputManagementReview ,approveManagementReview

class InviteManagementReviewResource(resources.ModelResource):
     class Meta:
          model = InviteManagementReview
class ProfileManagementReviewResource(resources.ModelResource):
     class Meta:
          model = ProfileManagementReview
class InputManagementReviewResource(resources.ModelResource):
     class Meta:
          model = InputManagementReview
class approveManagementReviewResource(resources.ModelResource):
     class Meta:
          model = approveManagementReview


    
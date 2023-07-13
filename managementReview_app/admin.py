from django.contrib import admin
from .models import InviteManagementReview ,ProfileManagementReview ,InputManagementReview , approveManagementReview
from.resources import InviteManagementReviewResource , ProfileManagementReviewResource,InputManagementReviewResource ,approveManagementReviewResource
# Register your models here.
from import_export.admin import ImportExportModelAdmin



@admin.register(InviteManagementReview)
class InviteManagementReviewAdmin(ImportExportModelAdmin):
     list_display = ('dateManagementReview', )
     list_filter = ('dateManagementReview', )
     search_fields = ('dateManagementReview',)
     resource_class  = InviteManagementReviewResource
@admin.register(ProfileManagementReview)
class ProfileManagementReviewAdmin(ImportExportModelAdmin):
     list_display = ('systemProfileManagementReview', )
     list_filter = ('systemProfileManagementReview', )
     search_fields = ('systemProfileManagementReview',)
     resource_class  = ProfileManagementReviewResource
@admin.register(InputManagementReview)
class InputManagementReviewAdmin(ImportExportModelAdmin):
     list_display = ('systemInputManagementReview', )
     list_filter = ('systemInputManagementReview', )
     search_fields = ('systemInputManagementReview',)
     resource_class  = InputManagementReviewResource
@admin.register(approveManagementReview)
class InputManagementReviewAdmin(ImportExportModelAdmin):
     list_display = ('title', )
     list_filter = ('title', )
     search_fields = ('title',)
     resource_class  = approveManagementReviewResource
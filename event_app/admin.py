from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import  Event
from .resources import EventResource

# Register your models here.
@admin.register(Event)
class EventAdmin(ImportExportModelAdmin):

    list_display = [
        "id",
        "title",
        "user",
        "is_active",
        "is_deleted",
        "created_at",
        "updated_at",
    ]
    list_filter = ["is_active", "is_deleted"]
    search_fields = ["title"]
    resource_class  = EventResource
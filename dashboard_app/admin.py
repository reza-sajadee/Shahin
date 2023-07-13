from django.contrib import admin
from .models import Dashboard
# Register your models here.




@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
     list_display = ('id','name','created_at' ,'updated_at')
     list_filter = ('name','created_at','updated_at')
     search_fields = ('id','name','created_at' ,'updated_at')
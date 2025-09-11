from django.contrib import admin
from .models import  OutdoorActivity

# Register your models here.
#@admin.register(OutdoorLocation)
#class OutdoorLocationAdmin(admin.ModelAdmin):
 
 #   list_display = ['name', 'lat', 'lng', 'description']
  #  search_fields = ['name', 'description']

@admin.register(OutdoorActivity)
class OutdoorActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'location', 'created_at']
    list_filter = ['category']
    search_fields = ['title', 'description']

    def location(self, obj):
        return f"{obj.latitude}, {obj.longitude}"
    location.short_description = 'Location'


from django.contrib import admin
from .models import OutdoorLocation, OutdoorActivity

# Register your models here.
@admin.register(OutdoorLocation)
class OutdoorLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'lat', 'lng', 'description']
    search_fields = ['name', 'description']

@admin.register(OutdoorActivity)
class OutdoorActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'activity', 'location']
    list_filter = ['activity']
    search_fields = ['name']


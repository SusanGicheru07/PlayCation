from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.map_view, name="map"),
    path("api/locations/", views.locations_json, name="locations_json"),
    path("api/activities/", views.activities_json, name="activities_json"),
    path("add/activity/", views.add_activity, name="add_activity"),

]
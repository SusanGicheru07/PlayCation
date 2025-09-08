
from django.contrib import admin
from django.urls import path, include
from apps.outdoor import views as outdoor_views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('indoor/', include('apps.indoor.urls')),
    path('', include('apps.outdoor.urls')),     # include your outdoor app   

]



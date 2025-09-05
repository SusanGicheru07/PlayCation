
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('indoor/', include('apps.indoor.urls')),
    #path('', include('apps.outdoor.urls'))
]

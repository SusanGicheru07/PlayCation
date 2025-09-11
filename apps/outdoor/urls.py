from django.urls import path
from apps.outdoor import views

urlpatterns = [
    path('', views.index, name='outdoor-index'),
    path('new-event/', views.create_event, name='new-event'),
    path('api/events/', views.NewEventAPIView.as_view(), name='events'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.team_list, name='team_list'),
    path('game/<int:game_id>/', views.start_game, name='start_game'),
    path('game/<int:game_id>/add-round/', views.add_round, name='add_round'),
    path('round/<int:round_id>/declare-winner/<int:team_id>/', views.declare_winner, name='declare_winner'),
    path('scoreboard/', views.scoreboard, name='scoreboard'),

    # Singing game auto-upload
    path('singing/<int:round_id>/<int:team_id>/', views.singing_upload, name='singing_upload'),
]

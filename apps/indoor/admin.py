from django.contrib import admin
from .models import Team, Game, Round


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Team model.
    Displays team name, members, and score.
    """
    list_display = ("name", "members", "score")
    search_fields = ("name", "members")
    list_filter = ("score",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Game model.
    Displays type and status of the game.
    """
    list_display = ("type", "active_status")
    search_fields = ("type",)
    list_filter = ("active_status",)


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Round model.
    Displays round number, game type, winner, and points.
    """
    list_display = ("round_number", "game", "hint", "winner", "points")
    search_fields = ("hint", "game__type", "winner__name")
    list_filter = ("game__type", "winner", "points")
    autocomplete_fields = ("winner", "game")  
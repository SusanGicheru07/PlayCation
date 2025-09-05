from django.db import models


class Team(models.Model):
    """
    Represents a team participating in indoor games.
    Each team has a name, a list of members, and an accumulated score.
    """
    name = models.CharField(
        max_length=100,
        help_text="Enter the name of the team."
    )
    members = models.TextField(
        help_text="Comma-separated list of team members (e.g., Alice,Bob,Charlie)."
    )
    score = models.IntegerField(
        default=0,
        help_text="Current score of the team."
    )

    def __str__(self):
        return f"Team {self.name} (Score: {self.score})"


class Game(models.Model):
    """
    Stores the different game types available in the indoor app.
    A game can either be active or inactive.
    """
    GAME_TYPES = [
        ('Singing', 'Singing'),
        ('Charades', 'Charades'),
    ]

    type = models.CharField(
        max_length=100,
        choices=GAME_TYPES,
        help_text="Type of indoor game (Singing or Charades)."
    )
    active_status = models.BooleanField(
        default=True,
        help_text="Indicates whether this game is currently active."
    )

    def __str__(self):
        return f"Game: {self.type} ({'Active' if self.active_status else 'Inactive'})"


class Round(models.Model):
    """
    Represents a single round within a game session.
    Each round belongs to a specific game, has a hint (for charades), 
    and stores the winning team and awarded points.
    """
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        help_text="The game this round belongs to."
    )
    round_number = models.IntegerField(
        help_text="Sequential number of the round (e.g., 1, 2, 3)."
    )
    hint = models.CharField(
        max_length=255,
        help_text="Hint for the round (e.g., word for charades)."
    )
    winner = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The team that won this round (if any)."
    )
    points = models.IntegerField(
        default=0,
        help_text="Points awarded to the winning team in this round."
    )

    def __str__(self):
        return f"Round {self.round_number} of {self.game.type} (Winner: {self.winner.name if self.winner else 'None'})"

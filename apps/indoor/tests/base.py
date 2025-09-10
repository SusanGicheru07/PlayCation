from django.test import TestCase
from indoor.models import Game, Team, Round

class BaseTestCase(TestCase):
    def setUp(self):
        # Teams
        self.team1 = Team.objects.create(name="Team Alpha", score=0)
        self.team2 = Team.objects.create(name="Team Beta", score=0)

        # Singing Game
        self.singing_game = Game.objects.create(
            name="Singing",
            type="Singing",
            active_status=True
        )
        self.singing_round1 = Round.objects.create(
            game=self.singing_game,
            round_number=1,
            hint="Sing Happy Birthday"
        )

        # Charades Game
        self.charades_game = Game.objects.create(
            name="Charades",
            type="Charades",
            active_status=True
        )
        self.charades_round1 = Round.objects.create(
            game=self.charades_game,
            round_number=1,
            hint="Act like a cat"
        )

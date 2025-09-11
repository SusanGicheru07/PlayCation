from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from indoor.models import Game, Team, Round
from .base import BaseTestCase

class HomeViewTest(BaseTestCase):
    def test_home_page_lists_games(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Singing")
        self.assertContains(response, "Charades")

class TeamListViewTest(BaseTestCase):
    def test_team_list_displays(self):
        response = self.client.get(reverse("team_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.team1.name)

class StartGameViewTest(BaseTestCase):
    def test_start_game_displays_rounds(self):
        url = reverse("start_game", args=[self.charades_game.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.charades_round1.hint)

class AddRoundViewTest(BaseTestCase):
    def test_add_round_creates_round(self):
        url = reverse("add_round", args=[self.charades_game.id])
        response = self.client.post(url, {"hint": "Act it out"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Round.objects.filter(game=self.charades_game).count(), 2)  # base + new one


class DeclareWinnerViewTest(BaseTestCase):
    def test_declare_winner_charades(self):
        url = reverse("declare_winner", args=[self.charades_round1.id, self.team1.id])
        self.client.get(url)
        self.charades_round1.refresh_from_db()
        self.team1.refresh_from_db()
        self.assertEqual(self.charades_round1.winner, self.team1)
        self.assertEqual(self.charades_round1.points, 20)
        self.assertEqual(self.team1.score, 20)


class SingingUploadViewTest(BaseTestCase):
    def test_singing_upload_success(self):
        fake_audio = SimpleUploadedFile("test.wav", b"RIFF....WAVE", content_type="audio/wav")
        url = reverse("singing_upload", args=[self.singing_round1.id, self.team2.id])
        response = self.client.post(url, {"audio": fake_audio})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("points", data)
        self.singing_round1.refresh_from_db()
        self.team2.refresh_from_db()
        self.assertEqual(self.singing_round1.winner, self.team2)
        self.assertGreaterEqual(self.singing_round1.points, 0)
        self.assertGreaterEqual(self.team2.score, 0)

    def test_singing_upload_no_audio(self):
        url = reverse("singing_upload", args=[self.singing_round1.id, self.team1.id])
        # url = reverse("singing_upload", args=[self.round.id, self.team.id])
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

class ScoreboardViewTest(BaseTestCase):
    def test_scoreboard_orders_teams(self):
        self.team1.score = 50
        self.team2.score = 100
        self.team1.save()
        self.team2.save()

        url = reverse("scoreboard")
        response = self.client.get(url)
        teams = response.context["teams"]
        self.assertEqual(teams[0], self.team2)
        self.assertEqual(teams[1], self.team1)
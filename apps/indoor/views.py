import os
import tempfile
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import F
from .models import Team, Game, Round
from pydub import AudioSegment
import numpy as np
import librosa


def home(request):
    """Show available games (Singing, Charades)."""
    games = Game.objects.filter(active_status=True)
    return render(request, "templates/index.html", {"games": games})


def team_list(request):
    """List all teams with scores."""
    teams = Team.objects.all()
    return render(request, "templates/teams.html", {"teams": teams})


def start_game(request, game_id):
    """Start a game by selecting it and showing details."""
    game = get_object_or_404(Game, id=game_id)
    rounds = Round.objects.filter(game=game).order_by("round_number")
    return render(request, "templates/game_detail.html", {"game": game, "rounds": rounds})


def add_round(request, game_id):
    """Create a new round for the game with a hint."""
    game = get_object_or_404(Game, id=game_id)

    if request.method == "POST":
        hint = request.POST.get("hint")
        round_number = Round.objects.filter(game=game).count() + 1
        Round.objects.create(game=game, round_number=round_number, hint=hint)
        return redirect("start_game", game_id=game.id)

    return render(request, "templates/add_round.html", {"game": game})


def singing_upload(request, round_id, team_id):
    """
    Handle singing audio:
    - Measure duration, loudness, and pitch.
    - Assign points automatically.
    """
    if request.method == "POST" and request.FILES.get("audio"):
        audio_file = request.FILES["audio"]

        round_instance = get_object_or_404(Round, id=round_id)
        team = get_object_or_404(Team, id=team_id)

        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            for chunk in audio_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        # Load audio with pydub
        audio = AudioSegment.from_file(tmp_path)

        # Duration (in seconds)
        duration_sec = len(audio) / 1000.0

        # Loudness (RMS in dB)
        loudness = audio.dBFS  # average loudness

        # librosa for pitch estimation
        y, sr = librosa.load(tmp_path)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[magnitudes > np.median(magnitudes)]
        avg_pitch = np.mean(pitch_values) if len(pitch_values) > 0 else 0

        # ---------------- SCORING ----------------
        duration_points = int(duration_sec / 36)  # 1 hr (3600s) → 100 pts
        loudness_points = int(max(0, (loudness + 60)))  # normalize dBFS (-60 silence → 0, 0 dBFS → 60 pts)
        pitch_points = int(min(40, avg_pitch / 10))  # cap pitch-based bonus

        points = duration_points + loudness_points + pitch_points

        #results
        round_instance.winner = team
        round_instance.points = points
        round_instance.save()

        Team.objects.filter(id=team.id).update(score=F("score") + points)

        # Cleanup temp file
        os.remove(tmp_path)

        return JsonResponse({
            "team": team.name,
            "duration_sec": duration_sec,
            "loudness": loudness,
            "avg_pitch": avg_pitch,
            "points": points
        })

    return JsonResponse({"error": "No audio received"}, status=400)


def declare_winner(request, round_id, team_id):
    """Fallback for Charades game."""
    round_instance = get_object_or_404(Round, id=round_id)
    team = get_object_or_404(Team, id=team_id)

    if round_instance.game.type == "Charades":
        points = 20
    else:
        points = 10

    round_instance.winner = team
    round_instance.points = points
    round_instance.save()

    Team.objects.filter(id=team.id).update(score=F("score") + points)

    return redirect("start_game", game_id=round_instance.game.id)


def scoreboard(request):
    """Show all teams ranked by score."""
    teams = Team.objects.order_by("-score")
    return render(request, "templates/scoreboard.html", {"teams": teams})

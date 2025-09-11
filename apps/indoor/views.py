import os
import tempfile
import json
from django.shortcuts import render, get_object_or_404, redirect
from .utils import calculate_singing_points
from django.http import JsonResponse
from django.db.models import F
from .models import Team, Game, Round
from pydub import AudioSegment
import numpy as np
import librosa
import soundfile as sf
import subprocess


def home(request):
    """Show available games (Singing, Charades)."""
    games = Game.objects.filter(active_status=True)
    return render(request, "index.html", {"games": games})


def team_list(request):
    """List all teams with scores."""
    teams = Team.objects.all()
    return render(request, "teams.html", {"teams": teams})


def start_game(request, game_id):
    """Start a game by selecting it and showing details."""
    game = get_object_or_404(Game, id=game_id)
    rounds = Round.objects.filter(game=game).order_by("round_number")
    return render(request, "game_detail.html", {"game": game, "rounds": rounds})


def add_round(request, game_id):
    """Create a new round for the game with appropriate content based on game type."""
    game = get_object_or_404(Game, id=game_id)
    teams = Team.objects.all()
    game_type = game.type.lower().strip()
    
    if request.method == "POST":
        round_number = Round.objects.filter(game=game).count() + 1
        
        if game_type == "charades":
            # Handle charades round
            hint = request.POST.get("hint")
            team_id = request.POST.get("team") 
            team = get_object_or_404(Team, id=team_id)

            new_round = Round.objects.create(
                game=game, 
                round_number=round_number, 
                team = team,
                hint=hint,
                content_type="charades"
            )
            return redirect("handle_guesses", round_id=new_round.id)
            
        elif game_type == "singing":
            # Handle singing round - redirect to singing interface
            song_title = request.POST.get("song_title", "Free Style")
            team_id = request.POST.get("team")  
            team = get_object_or_404(Team, id=team_id)

            Round.objects.create(
                game=game,
                round_number=round_number,
                team = team,
                hint=song_title,  
                content_type="singing"
            )
            # Redirect to singing interface
            return redirect("singing_round", round_id=Round.objects.filter(game=game).last().id)
    
    return render(request, "add_round.html", {"game": game, "teams":teams})


def singing_round(request, round_id):
    """Display singing round interface."""
    round_instance = get_object_or_404(Round, id=round_id)
    teams = Team.objects.filter(id=round_instance.team.id)
    game = round_instance.game
    
    context = {
        'round': round_instance,
        'teams': teams,
        'game': game,
        'song_title': round_instance.hint  
    }
    
    return render(request, 'singing_round.html', context)


def singing_upload(request, round_id, team_id):
    """
    Fake scoring endpoint — only receives points from the frontend
    """
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        points = data.get("points")

        if points is None:
            return JsonResponse({"error": "Points not provided"}, status=400)

        round_instance = get_object_or_404(Round, id=round_id)
        team = get_object_or_404(Team, id=team_id)

        # Add points to team
        team.score += points
        team.save()

        return JsonResponse({
            "message": f"Points added to {team.name}",
            "team": team.name,
            "points_awarded": points,
            "total_score": team.score
        })

    return JsonResponse({"error": "Invalid request method"}, status=405)

def handle_guesses(request, round_id):
    round_instance = get_object_or_404(Round, id=round_id)
    game = round_instance.game

    if request.method == "POST":
        guess1 = request.POST.get("guess1", "").strip().lower()
        guess2 = request.POST.get("guess2", "").strip().lower()
        guess3 = request.POST.get("guess3", "").strip().lower()
        
        correct_answer = round_instance.hint.strip().lower()
        correct_guesses = 0
        
        # Check each guess
        guesses = [guess1, guess2, guess3]
        for guess in guesses:
            if guess == correct_answer:
                correct_guesses += 1
        
        # Majority rule: if 2 or more correct, team wins
        if correct_guesses >= 2:
            # Auto-declare winner
            points = 20 if round_instance.game.type == "Charades" else 10
            
            round_instance.winner = round_instance.team
            round_instance.points = points
            round_instance.save()
            
            Team.objects.filter(id=round_instance.team.id).update(score=F("score") + points)
            
            return JsonResponse({
                "correct": True, 
                "message": f"Team wins! ({correct_guesses}/3 correct guesses)",
                
            })
        else:
            return JsonResponse({
                "correct": False, 
                "message": f"Not enough correct guesses ({correct_guesses}/3)"
            })
    
    return render(request, "guessing_interface.html", {"round": round_instance, "game":game})

def declare_winner(request, round_id, team_id):
    """Fallback for Charades game."""
    round_instance = get_object_or_404(Round, id=round_id)
    team = get_object_or_404(Team, id=team_id)

    # Add this check
    if round_instance.winner:
        messages.error(request, "Winner already declared!")
        return redirect("start_game", game_id=round_instance.game.id)

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
    return render(request, "scoreboard.html", {"teams": teams})

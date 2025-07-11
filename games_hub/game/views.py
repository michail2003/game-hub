from django.shortcuts import get_object_or_404, render
from .models import Game, GENRE_CHOICES
from django.db import models
# Create your views here.
def home(request):
    games = Game.objects.all()

    searched_word = request.GET.get('search')
    if searched_word:
        games = games.filter(title__contains=searched_word)

    selected_genre = request.GET.get('genre')
    if selected_genre:
        games = games.filter(
            models.Q(genre=selected_genre) |
            models.Q(genre2=selected_genre) |
            models.Q(genre3=selected_genre)
        )

    genres = GENRE_CHOICES  # Pass value and display name
    return render(request, 'base.html', {
        'games': games,
        'genres': genres,
        'selected_genre': selected_genre,
    })

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'game.html', {'game': game})

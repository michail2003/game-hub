from django.shortcuts import get_object_or_404, render
from .models import Game, Game_Genre
from django.db import models
# Create your views here.
def home(request):
    games = Game.objects.all()
    genres = Game_Genre.objects.all()

    if 'genre' in request.GET:
        genre = request.GET['genre']
        games = games.filter(genres__genre=genre)

    searched_word = request.GET.get('search')
    if searched_word:
        games = games.filter(title__contains=searched_word)
    return render(request, 'base.html', {'games':games,'genres': genres})

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    genres = Game_Genre.objects.all()
    return render(request, 'game.html', {'game': game, 'genres': genres})
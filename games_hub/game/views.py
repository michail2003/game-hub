from django.shortcuts import get_object_or_404, render
from .models import Game
# Create your views here.
def home(request):
    games = Game.objects.all()

    searched_word = request.GET.get('search')
    if searched_word:
        games = games.filter(title__contains=searched_word)
    return render(request, 'base.html', {'games': games})

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'game.html', {'game': game})

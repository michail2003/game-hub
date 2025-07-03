from django.shortcuts import get_object_or_404, render
from .models import Game
# Create your views here.
def home(request):
    games = Game.objects.all()
    context = {
        'games': games
    }
    return render(request, 'base.html', context)

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'game.html', {'game': game})

def search(request):
    query = request.GET.get('q')
    results = Game.objects.filter(title__icontains=query)
    return render(request, 'search_results.html', {'results': results})
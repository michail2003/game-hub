from django.shortcuts import get_object_or_404, redirect, render
from .models import Game, Game_Genre, CartItem
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
    return render(request, 'homepage.html', {'games':games,'genres': genres})

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    genres = Game_Genre.objects.all()
    return render(request, 'game.html', {'game': game, 'genres': genres})
   
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.game.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, pk):
    game = Game.objects.get(id=pk)
    cart_item, created = CartItem.objects.get_or_create(game=game,user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

def remove_from_cart(request, pk):
    cart_item = CartItem.objects.get(id=pk)
    cart_item.delete()
    return redirect('view_cart')

def increase_quantity(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('view_cart')

def decrease_quantity(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()  # Optionally remove if it reaches 0
    return redirect('view_cart')

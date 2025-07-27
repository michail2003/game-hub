from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from .models import Game, Game_Genre, CartItem
from users_auth_app.models import Order, Voucher,OrderItem
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
    price = game.discounted_price()
    error = None

    if request.method == "POST":
        voucher_code = request.POST.get("voucher")
        applying = request.POST.get("apply-voucher")
        cart_add = request.POST.get("AddingToCart")

        if voucher_code:
            voucher_qs = Voucher.objects.filter(code=voucher_code, expiration_date__gte=timezone.now())
            if voucher_qs.exists():
                discount = voucher_qs.first().discount
                if applying:
                    voucher_price = price * (1 - discount / 100)
                    return render(request, 'game.html',{"price":voucher_price,'game':game})
            else:
                error = "Invalid or expired voucher code"
        if cart_add:
                CartItem.objects.create(game=game, user=request.user, price=price)


    return render(request, 'game.html', {
        'game': game,
        'genres': genres,
        'price': price,
        'error': error,

    })


   
def view_cart(request):
    if not request.user.is_authenticated:
        return render(request, 'cart.html')
    
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'cart.html')
    game = Game.objects.get(id=pk)
    cart_item = CartItem.objects.create(game=game, user=request.user)
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

def buy_now(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('view_cart')  # Or show message: cart is empty

    # Create the order
    order = Order.objects.create(user=request.user)

    total = 0

    # Create OrderItem for each CartItem
    for item in cart_items:
        price = item.total_price()
        OrderItem.objects.create(
            order=order,
            game_title=item.game.title,
            quantity=item.quantity,
            price=price,
            item_price = item.game_price,
        )
        total += price

    # Update total price
    order.total_price = total
    order.save()

    # Now safely delete cart items
    cart_items.delete()

    return redirect('view_orders')  # Redirect to orders list or confirmation page


def delete_all_cart_items(request):
    if request.method == "POST":
        CartItem.objects.filter(user=request.user).delete()
    return redirect('view_cart')

def view_orders(request):
    if not request.user.is_authenticated:
        return render(request, 'orders.html') # Redirect to login if not authenticated
    
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})
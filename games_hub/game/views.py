from django.core.mail import EmailMessage
from io import BytesIO
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from .models import Game, Game_Genre, CartItem
from users_auth_app.models import Order, Voucher,OrderItem
from django.core.mail import send_mail
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
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

def order_mail_invoice(request,order):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A5)
    width, height = A5

    c.setFont("Helvetica", 20)
    title = "Faturë Tatimore"
    title_width = c.stringWidth(title, "Helvetica", 20)
    c.drawString((width - title_width) / 2, height - 50, title)

    y = height - 120
    items = OrderItem.objects.filter(order=order)

    for item in items:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, f"{item.game.title}")
        y -= 20

        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"{item.quantity} cope X {item.item_price:.2f} $")
        c.drawString(350, y, f"{item.price:.2f} $")
        y -= 30

        c.drawString(50, y, '-' * 60)
        y -= 30

    c.drawString(280, y, f"Total Price: {order.total_price:.2f} $")
    c.save()
    buffer.seek(0)
    email = EmailMessage(
    subject=f'Your order with ID {order.order_id}',
    body=f'Hello Mr/Mrs. {order.user.first_name} {order.user.last_name},\n\nYour order with ID {order.order_id} and total price {order.total_price:.2f} $ will be delivered soon.\n\nYour invoice is attached.',
    from_email=settings.EMAIL_HOST_USER,
    to=[order.user.email],
)

    email.attach(f'Invoice_{order.order_id}.pdf', buffer.read(), 'application/pdf')
    email.send()

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
            game=item.game,
            quantity=item.quantity,
            price=price,
            item_price = item.game_price,
        )
        total += price

    # Update total price
    order.total_price = total
    order.save()
    order_mail_invoice(request,order)
    # Now safely delete cart items
    cart_items.delete()

    return render(request, 'cart.html', {'message': f'Order placed successfully! order ID: {order.order_id}', 'total': total})


def delete_all_cart_items(request):
    if request.method == "POST":
        CartItem.objects.filter(user=request.user).delete()
    return redirect('view_cart')

def view_orders(request):
    if not request.user.is_authenticated:
        return render(request, 'orders.html') # Redirect to login if not authenticated
    
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})
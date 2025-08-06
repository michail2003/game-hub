from django.core.mail import EmailMessage
from io import BytesIO
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from .models import Game, Game_Genre, CartItem,Milesstones
from users_auth_app.models import Order, Voucher,OrderItem,CustomUser
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


    discounted_games = Game.objects.filter(discount__gt=0).order_by('-release_date', '-discount')[:4]



    return render(request, 'homepage.html', {
        'games': games,
        'genres': genres,
        'discounted_games': discounted_games,
    })



def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    genres = Game_Genre.objects.all()
    price = game.discounted_price()

    cart_add = request.POST.get("AddingToCart")
    if cart_add:
        return add_to_cart(request,pk)


    return render(request, 'game.html', {
        'game': game,
        'genres': genres,
        'price': price,
    })


   
def view_cart(request):
    if not request.user.is_authenticated:
        return render(request, 'cart.html')
    
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    # Find first voucher used in any item (or None if none)
    coupon_applied = next((item.voucher_used for item in cart_items if item.voucher_used), None)

    context = {
        'cart_items': cart_items,
        'total': total,
        'items': total_items,
        'coupon_applied': coupon_applied,
    }

    return render(request, 'cart.html', context)

def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'cart.html')
    game = Game.objects.get(id=pk)
    try:
        cart_item = CartItem.objects.get(game=game, user=request.user)
        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
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
        item.delete() 
    return redirect('view_cart')

def order_mail_invoice(request, order, email_adress,city,street,area, apartment, phone_number):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A5)
    width, height = A5

    # Title
    c.setFont("Helvetica", 20)
    title = "Faturë Tatimore"
    title_width = c.stringWidth(title, "Helvetica", 20)
    c.drawString((width - title_width) / 2, height - 50, title)

    # Order & Shipping Info
    y = height - 90
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Order ID: {order.order_id}")
    y -= 12
    c.drawString(50, y, f"Order Date: {order.order_date.strftime('%d-%m-%Y %H:%M')}")
    y -= 12
    c.drawString(50, y, f"Customer: {order.user.first_name} {order.user.last_name}")
    y -= 12
    c.drawString(50, y, f"City: {city}")
    y -= 12
    c.drawString(50, y, f"Area: {area}")
    y -= 12
    c.drawString(50, y, f"Street: {street}")
    y -= 12
    c.drawString(50, y, f"Apartment: {apartment}")
    y -= 12
    c.drawString(50, y, f"Contact Number: {phone_number}")

    # Space before items
    y -= 25

    # Order Items
    items = OrderItem.objects.filter(order=order)
    for item in items:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, f"{item.game.title}")
        y -= 20

        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"{item.quantity} cope X {item.item_price:.2f} $")
        if item.coupon_used:
            y -= 15
            c.drawString(100, y, f"coupon used: {item.coupon_used} $")
        c.drawString(350, y, f"{item.price:.2f} $")
        y -= 30

        c.drawString(50, y, '-' * 60)
        y -= 30

    # Total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(280, y, f"Total Price: {order.total_price:.2f} $")

    # Save PDF
    c.save()
    buffer.seek(0)

    # Email with PDF
    email = EmailMessage(
        subject=f'Your order with ID {order.order_id}',
        body=f'Hello Mr/Mrs. {order.user.first_name} {order.user.last_name},\n\n'
             f'Your order with ID {order.order_id} placed on {order.order_date.strftime("%d-%m-%Y %H:%M")} '
             f'with a total price of {order.total_price:.2f} $ will be delivered soon.\n\n'
             f'Shipping to: {city}  {area}  {street}  {apartment}. '
             f'Contact Number: {phone_number}.\n\n'
             'Your invoice is attached.',
        from_email=settings.EMAIL_HOST_USER,
        to=[email_adress],
    )

    email.attach(f'Invoice_{order.order_id}.pdf', buffer.read(), 'application/pdf')
    email.send()



def milestone_voucher(request,bought):
    milestone = Milesstones.objects.all()
    total = request.user.games_ordered
    check = total - bought
    for m in milestone:
        if check < m.milestone and (check+bought) >= m.milestone:
            Voucher.objects.create(
                user = request.user,
                discount = m.discount,
                usage_limit = 1,
                milestone = m.milestone,
            )

def buy_now(request,mail,city,street,area, apartment, phone_number):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('view_cart')  # Cart empty

    order = Order.objects.create(user=request.user)
    total = 0

    for item in cart_items:
        voucher = item.voucher_used
        if voucher:
            if voucher.usage_limit == 1:
                voucher.delete()
            else:
                voucher.used_count += 1
                voucher.save()

        price = item.total_price()
        OrderItem.objects.create(
            order=order,
            game=item.game,
            quantity=item.quantity,
            price=price,
            item_price=item.game.discounted_price(),
            coupon_used=item.voucher_used if item.voucher_used else None
        )
        total += price

    order.total_price = total
    order.save()
    order_mail_invoice(request, order,mail,city,street,area, apartment, phone_number)
    total_items = sum(item.quantity for item in cart_items)
    request.user.games_ordered += total_items
    request.user.save()
    cart_items.delete()
    milestone_voucher(request,total_items)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order_confirmation.html', {
        'order_id': order.order_id,
        'total_price': order.total_price,
        'name': order.user.first_name,
        'surname': order.user.last_name,
        'date': order.order_date,
        'order_items': order_items, 
    })


def delete_all_cart_items(request):
    if request.method == "POST":
        CartItem.objects.filter(user=request.user).delete()
    return redirect('view_cart')

def voucher_apply(request):
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        cart_items = CartItem.objects.filter(user=request.user)

        coupon_code = Voucher.objects.filter(code=coupon, expiration_date__gte=timezone.now()).first()
        milestone_coupon = Voucher.objects.filter(user = request.user, usage_limit =1, code=coupon).first()
        if coupon_code:
            for item in cart_items:
                item.voucher_discount = coupon_code.discount
                item.voucher_used = coupon_code
                item.save()
            return redirect('view_cart')
        elif milestone_coupon:   
            for item in cart_items:
                item.voucher_discount = milestone_coupon.discount
                item.voucher_used = milestone_coupon
                item.save()
            return redirect('view_cart')   
    return redirect('view_cart')


def remove_voucher(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            item.voucher_discount = None
            item.voucher_used = None
            item.save()
        return redirect('view_cart')
    return redirect('view_cart')


def view_orders(request):
    if not request.user.is_authenticated:
        return render(request, 'orders.html') # Redirect to login if not authenticated
    
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})



def checkout_view(request):
    user = request.user

    # Default initial data from user profile
    initial_data = {
        'email': user.email,
        'phone_number': user.phone_number,
        'city': user.city,
        'area': user.area,
        'street': user.street,
        'apartment': user.apartment,
    }

    if request.method == 'GET':
        return render(request, 'checkout_form.html', {'initial': initial_data})

    else:  # POST
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        area = request.POST.get('area')
        street = request.POST.get('street')
        apartment = request.POST.get('apartment')
        action = request.POST.get("action")

        # Override initial_data with submitted values so they stay filled
        initial_data.update({
            'email': email,
            'phone_number': phone_number,
            'city': city,
            'area': area,
            'street': street,
            'apartment': apartment,
        })

        if not all([email, phone_number, city, area, street, apartment]):
            return render(request, 'checkout_form.html', {
                'error': 'All fields are required',
                'initial': initial_data
            })

        if action == "buy_now":
            return buy_now(request, email,city,street,area, apartment, phone_number)
        elif action == "cancel_order":
            CartItem.objects.filter(user=user).delete()
            return redirect('view_cart')


def rewards(request):
    vouchers = Voucher.objects.filter(user=request.user)
    milestones = Milesstones.objects.order_by('milestone')
    return render(request, 'users_coupons.html', {'vouchers': vouchers, 'milestones': milestones})


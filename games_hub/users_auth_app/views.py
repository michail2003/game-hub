from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout

from .models import CustomUser


def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'game.html')
        else:
            return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})


def logout_view(request):
    logout(request)
    return render(request, 'base.html')


def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        name  = request.POST.get('name')
        last_name = request.POST.get('last_name')

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'User already exists'})
        
        if password != confirm_password:
            return render(request, 'register.html', {'error': 'The passwords do not match'})

        user = CustomUser.objects.create_user(username=email, email=email, password=password, name=name, last_name=last_name)
        user.save()

        login(request, user)
        return render(request, 'base.html', {'message': 'User created successfully'})


def more_details(request):
    if request.method == 'GET':
        return render(request, 'userdetails.html')
    else:
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        area = request.POST.get('area')
        street = request.POST.get('street')
        profile_picture = request.FILES.get('profile_picture')

        user = request.user
        user.phone_number = phone_number
        user.city = city
        user.area = area
        user.street = street
        user.profile_picture = profile_picture
        user.save()
        
        return redirect('base')
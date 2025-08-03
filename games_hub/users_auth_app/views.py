from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser

def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'homepage.html')
        else:
            return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name  = request.POST.get('name')
        last_name = request.POST.get('last_name')

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'User already exists'})
        
        if password != confirm_password:
            return render(request, 'register.html', {'error': 'The passwords do not match'})

        if not all([email, password, confirm_password, first_name, last_name]):
            return render(request, 'register.html', {'error': 'All fields are required'})

        user = CustomUser.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()

        login(request, user)
        return redirect('home')


from django.contrib.auth import login

def more_details(request):
    if request.method == 'GET':
        return render(request, 'accaunt.html', {'user': request.user})
    else:
        user = request.user
        email = request.POST.get('email')
        first_name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        area = request.POST.get('area')
        street = request.POST.get('street')
        profile_picture = request.FILES.get('profile_picture')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
            return render(request, 'accaunt.html', {'error': 'Email is already taken'})
        
        if CustomUser.objects.filter(phone_number=phone_number).exclude(id=user.id).exists():
            return render(request, 'accaunt.html', {'error': 'Phone number is already taken'})
        
        if not first_name or not last_name:
            return render(request, 'accaunt.html', {'error': 'First and last name are required'})

        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                return render(request, 'accaunt.html', {'error': 'New passwords do not match'})
            elif user.check_password(new_password):
                return render(request, 'accaunt.html', {'error': 'New password cannot be the same as the old password'})
            else:
                user.set_password(new_password)

        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.city = city
        user.area = area
        user.street = street

        if profile_picture:
            user.profile_picture = profile_picture

        user.save()

        login(request, user)

        return redirect('home')


    
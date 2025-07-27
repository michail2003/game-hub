"""
URL configuration for games_hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from game import views
from users_auth_app import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('game/<int:pk>/', views.game_detail, name='game_detail'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('register/', auth_views.register_view, name='register'),
    path('accaunt/', auth_views.more_details, name='accaunt'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:pk>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:pk>/', views.decrease_quantity, name='decrease_quantity'),
    path('buy_now/', views.buy_now, name='buy_now'),
    path('cart/delete-all/', views.delete_all_cart_items, name='delete_all_cart_items'),
    path('orders/', views.view_orders, name='view_orders'),
    path('library/', auth_views.library, name='library')

]

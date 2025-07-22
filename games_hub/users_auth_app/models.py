import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from game.models import Game

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    user_saved_games = models.ManyToManyField('game.Game', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Order(models.Model):

    def generate_order_code():
        return uuid.uuid4().hex[:10].upper()
    
    status = [
        ('pending', 'Pending'),
        ('completed', 'Purchased'),    
        ]
    
    order_id = models.CharField(max_length=10, default=generate_order_code, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ManyToManyField(Game)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50, choices=status, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.order_id} by {self.user.email} - Status: {self.order_status}"


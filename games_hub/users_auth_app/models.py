import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    apartment = models.CharField(max_length=5,default='0',blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    games_ordered = models.PositiveIntegerField(default=0)

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
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50, choices=status, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.order_id} by {self.user.email} - Status: {self.order_status}"

class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    game = models.ForeignKey("game.Game",on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    coupon_used = models.CharField(max_length=10, null=True, blank=True)

class Voucher(models.Model):

    def generate_voucher_code():
            return uuid.uuid4().hex[:8].upper()
        
    code = models.CharField(max_length=8, default=generate_voucher_code, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    games= models.ManyToManyField("game.Game")
    expiration_date = models.DateTimeField(null=True, blank=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    milestone = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.discount}% off"
    

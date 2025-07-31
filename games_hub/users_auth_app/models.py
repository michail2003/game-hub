import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

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
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50, choices=status, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_library_synced = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.order_id} by {self.user.email} - Status: {self.order_status}"

class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    game = models.ForeignKey("game.Game",on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    photo = models.ImageField

class Voucher(models.Model):

    def generate_voucher_code():
            return uuid.uuid4().hex[:5].upper()
        
    code = models.CharField(max_length=10, default=generate_voucher_code, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    games= models.ManyToManyField("game.Game")
    expiration_date = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.code} - {self.discount}% off"
    
class gamelibrary(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey('game.Game', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True)
    price_bought = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField(null=True)

    def update_total_games(self):
        library = gamelibrary.objects.filter(user=self.user)
        total = sum(item.quantity or 0 for item in library)
        self.count = total
        self.save()

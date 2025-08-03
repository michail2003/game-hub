
from django.db import models
from users_auth_app.models import Voucher
from django.conf import settings



# Create your models here.
Console_CHOICES = (
    ('Ps3', 'PlayStation 3'),
    ('Ps4', 'PlayStation 4'),
    ('Ps5', 'PlayStation 5'),
    ('Xbox360', 'Xbox 360'),
    ('XboxOne', 'Xbox One'),
    ('XboxSeriesX', 'Xbox Series X/S'),
    ('Switch', 'Nintendo Switch'),
    ('PC', 'PC'),
)


MIN_AGE_CHOICES = (
    (0, 0),
    (6, 6),
    (12, 12),
    (16, 16),
    (18, 18),
    )
class Game_Genre(models.Model):
    genre = models.CharField(max_length=50)
    def __str__(self):
        return self.genre
    
class Game(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    genres = models.ManyToManyField(Game_Genre, related_name= 'GENRE_CHOICES')
    release_date = models.DateField()
    image = models.ImageField(upload_to='games_images', blank=True, null=True, help_text="Upload an image file")
    image_url = models.URLField(blank=True, null=True, help_text="Or provide an image URL")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    console = models.CharField(max_length=50, choices=Console_CHOICES)
    trailer = models.URLField(default='', blank=True)
    min_age = models.IntegerField(
        choices=MIN_AGE_CHOICES,
        default=0
    )
    discount = models.DecimalField(
        max_digits=4, decimal_places=2,
        default=0.0, blank=True
    )

    #Pc requirements
    min_cpu = models.CharField(max_length=100, default="N/A", blank=True, verbose_name="Minimum CPU")
    min_gpu = models.CharField(max_length=100, default="N/A", blank=True, verbose_name="Minimum GPU")
    min_ram = models.CharField(max_length=20, default="N/A", blank=True, verbose_name="Minimum RAM")
    min_storage = models.CharField(max_length=20, default="N/A", blank=True, verbose_name="Minimum Storage")

    rec_cpu = models.CharField(max_length=100, default="N/A", blank=True, verbose_name="Recommended CPU")
    rec_gpu = models.CharField(max_length=100, default="N/A", blank=True, verbose_name="Recommended GPU")
    rec_ram = models.CharField(max_length=20, default="N/A", blank=True, verbose_name="Recommended RAM")
    rec_storage = models.CharField(max_length=20, default="N/A", blank=True, verbose_name="Recommended Storage")

    def __str__(self):
        return self.title
    
    def discounted_price(self):
        if self.discount > 0:
            price = (self.price * (1 - self.discount / 100))
        else:
            price = self.price
            
        return price

class CartItem(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    voucher_discount = models.DecimalField(max_digits=10, decimal_places=2,null = True)
    voucher_used = models.ForeignKey(Voucher,null=True,on_delete=models.CASCADE)

    def total_price(self):
        unit_price = self.game.discounted_price()
        if self.voucher_discount:
            unit_price *= (1 - self.voucher_discount / 100)
        return unit_price * self.quantity
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
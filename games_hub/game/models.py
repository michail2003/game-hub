from django.db import models

# Create your models here.
Console_CHOICES = (
    ('Ps3', 'PlayStation3'),
    ('Ps4', 'PlayStation4'),
    ('Ps5', 'PlayStation5'),
    ('Xbox360', 'Xbox 360'),
    ('XboxOne', 'Xbox One'),
    ('XboxSeriesX', 'Xbox Series X'),
    ('Switch', 'Nintendo Switch'),
    ('PC', 'PC'),
)

GENRE_CHOICES = [
    ('action', 'Action'),
    ('adventure', 'Adventure'),
    ('rpg', 'RPG'),
    ('simulation', 'Simulation'),
    ('strategy', 'Strategy'),
    ('sports', 'Sports'),
    ('racing', 'Racing'),
    ('shooter', 'Shooter'),
    ('fighting', 'Fighting'),
    ('horror', 'Horror'),
    ('stealth', 'Stealth'),
    ('survival', 'Survival'),
    ('singleplayer', 'Singleplayer'),
    ('multiplayer', 'Multiplayer'),
    ('first_person', 'First Person'),
    ('third_person', 'Third Person'),
    ('co_op', 'Co-Op'),
    ('fps_tps', 'FPS/TPS'),
]
MIN_AGE_CHOICES = (
    (0, 0),
    (6, 6),
    (12, 12),
    (16, 16),
    (18, 18),
    )
class Game_Genre(models.Model):
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    def __str__(self):
        return self.genre
class Game(models.Model):
    title = models.CharField(max_length=15)
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
    discount = models.IntegerField(
        default=0, blank=True, null=True
    )


class Order(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class Voucher(models.Model):
    code = models.CharField(max_length=20, unique=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='vouchers')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateField()
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

class Game(models.Model):
    title = models.CharField(max_length=15)
    description = models.TextField()
    release_date = models.DateField()
    image = models.ImageField(upload_to='games_images', blank=True, null=True, help_text="Upload an image file")
    image_url = models.URLField(blank=True, null=True, help_text="Or provide an image URL")
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    genre2 = models.CharField(
        max_length=50, choices=GENRE_CHOICES, null=True, blank=True, verbose_name="Secondary Genre"
    )
    genre3 = models.CharField(
        max_length=50, choices=GENRE_CHOICES, null=True, blank=True, verbose_name="third Genre"
    )
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

    def discounted_price(self):
        if self.discount:
            return self.price * (1 - self.discount / 100)
        return self.price
    
    def __str__(self):
        return self.title
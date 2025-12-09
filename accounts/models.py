from django.db import models
from django.contrib.auth.models import AbstractUser
from products.models import products

# Custom user model
FAVORITE_GENRES = [
    ('fantasy', 'Fantasy'),
    ('scifi', 'Science Fiction'),
    ('mystery', 'Mystery'),
    ('romance', 'Romance'),
    ('nonfiction', 'Non-Fiction'),
    ('horror', 'Horror'),
    ('history', 'History'),
    ('other', 'Other'),
]



class base_user(AbstractUser):
    user_bio = models.TextField(blank=True)
    favorite_genre = models.CharField(max_length=50, choices=FAVORITE_GENRES, blank=True)
    favorite_authors = models.JSONField(blank=True, default=list) # new CQ
    user_owned_products = models.ManyToManyField(products)
    user_tags = models.ManyToManyField('general.Tag', blank=True, related_name='users')
    is_user_a_test_user = models.BooleanField(default=False)
    
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    favorite_books = models.ManyToManyField(products, blank=True, related_name='favorited_by')

    @property
    def base_user(self):
        return self
    
    @property
    def user_id(self):
        return self.id

    def __str__(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full or self.username
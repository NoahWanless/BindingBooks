from django.db import models
from django.contrib.auth.models import AbstractUser

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
    user_owned_books = models.JSONField(blank=True, default=list)
    is_user_a_test_user = models.BooleanField(default=False)
    
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    @property
    def base_user(self):
        return self
    
    @property
    def user_id(self):
        return self.id

    def __str__(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full or self.username

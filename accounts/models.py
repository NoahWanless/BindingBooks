from django.db import models
from django.contrib.auth.models import AbstractUser


class base_user(AbstractUser):
    user_bio = models.TextField(blank=True)
    user_owned_books = models.JSONField(blank=True, default=list)
    is_user_a_test_user = models.BooleanField(default=False)

    @property
    def base_user(self):
        return self
    
    @property
    def user_id(self):
        return self.id

    def __str__(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full or self.username
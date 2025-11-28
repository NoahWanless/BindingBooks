from django.db import models
from django.contrib.auth import get_user_model
from products.models import products
from datetime import date

User = get_user_model()


def today_date():
    return date.today()


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    approved = models.BooleanField(default=True)
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="reviews_written",
    )

    product = models.ForeignKey(
        products,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    created_at = models.DateField(default=today_date)
    review_text = models.TextField(blank=True, default="")
    review_tags = models.JSONField(default=list, blank=True)
    trigger_warnings = models.JSONField(default=list, blank=True)
    star_rating = models.PositiveSmallIntegerField(default=1)
    spice_rating = models.PositiveSmallIntegerField(default=1)
    violence_rating = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        author_name = self.author.username if self.author else "Unknown user"
        return f"Review by {author_name} on {self.product.product_name}"

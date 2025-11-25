from django.urls import path
from . import views

urlpatterns = [
    path("queue/", views.moderation_queue, name="moderation_queue"),
    path("review/<int:pk>/", views.review_item, name="review_item"),
]
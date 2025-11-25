from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from forums.models import forum_post  # or whatever your post model is
from .models import ModerationQueue

@receiver(post_save, sender=forum_post)
def add_post_to_moderation(sender, instance, created, **kwargs):
    if created:
        ModerationQueue.objects.create(
            content_type=ContentType.objects.get_for_model(forum_post),
            object_id=instance.post_id,
            status='pending'
        )

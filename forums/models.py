from django.db import models

from django.contrib.auth import get_user_model
from general.validators import Validators
User = get_user_model()


class forums(models.Model):
    forum_id = models.AutoField(primary_key=True)
    forum_name = models.TextField(null=False)
    forum_description = models.TextField(validators=[Validators.is_any_word_in_text_profanity])
    forum_lead = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL
    )  # changed to forum lead for clarity
    forum_tags = models.JSONField(default=list)
    start_date = models.DateField()
    meeting_day = models.CharField(
        max_length=10,
        choices=[
            ("Mon", "Monday"),
            ("Tue", "Tuesday"),
            ("Wed", "Wednesday"),
            ("Thu", "Thursday"),
            ("Fri", "Friday"),
            ("Sat", "Saturday"),
            ("Sun", "Sunday"),
        ],
        blank=False,
    )
    meeting_time = models.TimeField()

    

    def __str__(self):
        forum_lead_name = (
            self.forum_lead.username if self.forum_lead else "Unknown forum lead"
        )
        return f"{self.forum_name} (led by {forum_lead_name})"

import csv
class forum_post(models.Model):
    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    forum = models.ForeignKey(forums, on_delete=models.CASCADE, related_name="posts")
    post_text = models.TextField(null=True, blank=True,validators=[Validators.is_any_word_in_text_profanity])
    post_reactions = models.JSONField(default=list)

    def __str__(self):
        author_name = self.author.username if self.author else "Unknown author"
        return f"{author_name} said: {self.post_text}"


class forum_comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(
        forum_post, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    comment_text = models.TextField(null=False,validators=[Validators.is_any_word_in_text_profanity])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        author_name = (
            self.author.username if self.author else "Unknown author"
        )  # null owner doesnt give errors -sam
        return f"Comment by {author_name}"

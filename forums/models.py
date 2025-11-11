from django.db import models
from accounts.models import base_user


class forums(models.Model):
    forum_id = models.AutoField(primary_key=True)
    forum_name = models.TextField(null=False)
    forum_description = models.TextField()
    owner = models.ForeignKey(
        base_user, null=True, on_delete=models.SET_NULL
    )  # this is so if the owner is deleted, the owner here is simply set to null
    forum_tags = models.JSONField(default=list)
    start_date = models.DateField(null=True, blank=True)
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
        null=True,
        blank=True,
    )
    meeting_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        owner_name = (
            self.owner.name if self.owner else "Unknown owner"
        )  # changed so having null owner doesn't give errors
        return f"{self.forum_name} (owned by {owner_name})"


class forum_post(models.Model):
    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(base_user, null=True, on_delete=models.SET_NULL)
    post_text = models.TextField(null=True, blank=True)
    post_reactions = models.JSONField(default=list)

    def __str__(self):
        author_name = (
            self.author.name if self.author else "Unknown author"
        )  # changed so having null owner doesnt give errors
        return f"{author_name} said: {self.post_text}"

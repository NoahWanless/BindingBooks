from django.db import models


class Tag(models.Model):
	"""site-wide tag model :)))"""
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=110, unique=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ("name",)

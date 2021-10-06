from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Contact(models.Model):
	full_name = models.CharField(max_length=500, default="none")
	email = models.CharField(max_length=500, default="none")
	message = models.TextField(default="none")

	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.full_name
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from app_user.models import AppUser


# Create your models here.

class Referral(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
	other_user_id = models.CharField(max_length=500, default="none")
	amount = models.FloatField(default=0)

	request_status = models.BooleanField(default=False)
	paid_status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.amount



class OtherUser(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.app_user.user.username



class PrimaryList(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
	other_users = models.ManyToManyField(OtherUser, through="PrimaryListOtherUserConnector")

	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.app_user.user.username



class SecondaryList(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
	other_users = models.ManyToManyField(OtherUser, through="SecondaryListOtherUserConnector")

	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.app_user.user.username




class PrimaryListOtherUserConnector(models.Model):
	primary_list = models.ForeignKey(PrimaryList, on_delete=models.CASCADE)
	other_user = models.ForeignKey(OtherUser, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(default=timezone.now)



class SecondaryListOtherUserConnector(models.Model):
	secondary_list = models.ForeignKey(SecondaryList, on_delete=models.CASCADE)
	other_user = models.ForeignKey(OtherUser, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(default=timezone.now)
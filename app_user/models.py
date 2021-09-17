from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class AppUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_photo = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="default_files/default_face.png")

	full_name = models.CharField(max_length=500, default="none")
	other_name = models.CharField(max_length=500, default="none", null=True)
	last_name = models.CharField(max_length=500, default="none", null=True)

	#kyc
	house_address = models.TextField(default="none", null=True)
	#place_of_work = models.CharField(max_length=500, default="none")
	#place_of_work_address = models.TextField(default="none", null=True)
	dob = models.CharField(max_length=500, default="none", null=True)
	age = models.IntegerField(default=0)
	id_image = models.FileField(upload_to='account_files/id_images/', blank=True, default="default_files/default_face.png")
	id_number = models.CharField(max_length=500, default="none")
	state_of_origin = models.CharField(max_length=500, default="none")
	country = models.CharField(max_length=500, default="none")
	language = models.CharField(max_length=500, default="none")
	phone_no = models.CharField(max_length=500, default="none", null=True)
	bank_name = models.CharField(max_length=500, default="none")
	bank_verification_number = models.CharField(max_length=500, default="none", null=True)
	bank_account_number = models.CharField(max_length=500, default="none")
	bank_account_name =models.CharField(max_length=500, default="none")

	payment_wallet_address = models.CharField(max_length=500, default="none")

	public_key = models.CharField(max_length=500, default="none")
	private_key = models.CharField(max_length=500, default="none")

	status = models.BooleanField(default=False)

	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.public_key




class Investment(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

	package_type = models.CharField(max_length=500, default="none")

	amount = models.FloatField(default=0)

	#from investor 
	payment_status = models.BooleanField(default=False)

	#from admin
	payment_status_k = models.BooleanField(default=False)

	
	proof_photo1 = models.FileField(upload_to='app_files/proof_photos/', blank=True, default="default_files/default.png")
	proof_photo2 = models.FileField(upload_to='app_files/proof_photos/', blank=True, default="default_files/default.png")


	request_status = models.BooleanField(default=False)
	harvest_amount = models.IntegerField(default=0)
	ha_payment_status = models.BooleanField(default=False)

	switch_date7 = models.DateTimeField(default=timezone.now)
	switch_date30 = models.DateTimeField(default=timezone.now)

	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.app_user.full_name

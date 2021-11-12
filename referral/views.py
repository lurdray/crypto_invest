from django.shortcuts import render

from django.contrib import messages

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from app_user.models import *
from referral.models import *

from django.core.mail import send_mail

from datetime import datetime
import datetime as dt

import requests

# Create your views here.




def IndexView(request):
	app_user = AppUser.objects.get(user__pk=request.user.id)

	if request.method == "POST":
		pass

		#return HttpResponseRedirect(reverse("app_user:index"))


	else:

		try:
			primary_list = PrimaryList.objects.get(app_user=app_user)

		except:
			primary_list = []

		try:
			secondary_list = SecondaryList.objects.get(app_user=app_user)

		except:
			secondary_list = []

		#primary_referrals = primary_list.other_users.all()
		#secondary_referrals = secondary_list.other_users.all()


		referrals = Referral.objects.filter(app_user__id=app_user.id)

		referral_count = GetReferralCount(request, app_user.id)
		referral_amount = GetTotalAmount(request, app_user.id)

		context = {
			#"primary_referrals": primary_referrals,
			#"secondary_referrals": secondary_referrals,

			"primary_list": primary_list,
			"secondary_list": secondary_list,

			"referrals": referrals,

			"referral_count": referral_count,
			"referral_amount": referral_amount,
		}

		#return HttpResponse(str(primary_list))

		return render(request, "referral/index.html", context )




def ReferralDetailView(request, referral_id):
	app_user = AppUser.objects.get(user__pk=request.user.id)

	referral = Referral.objects.get(id=referral_id)

	if request.method == "POST":
	    
		app_user.otp_status = False
		app_user.save()
	    
		referral.request_status = True
		referral.save()
		RaySendMail(request, "Withdrawal Request", "%s just requested for benefits from referral." % (referral.app_user.full_name), "info@onpointcurrency.com")


		return HttpResponseRedirect(reverse("referral:index"))


	else:
	    
		if app_user.otp_choice:
			if app_user.otp_status:

				context = {
					"referral": referral,
				}
        
				return render(request, "referral/referral_detail.html", context )


			else:
				return HttpResponseRedirect(reverse("ga_app:authenticate", args=["'referral:referral_detail', args=[%s,]"%(referral_id)]))
    
		else:
			context = {
				"referral": referral,
			}
    
			return render(request, "referral/referral_detail.html", context )




def AddPrimary(request, app_user_id, other_user_id):
	app_user = AppUser.objects.get(id=app_user_id)
	other_user = AppUser.objects.get(id=other_user_id)

	other_user = OtherUser.objects.create(app_user=other_user)

	try:
		primary_list = PrimaryList.objects.get(app_user=app_user)

	except:
		primary_list = PrimaryList.objects.create(app_user=app_user)

	pl = PrimaryListOtherUserConnector(primary_list=primary_list, other_user=other_user)
	pl.save()

	primary_list.save()




def AddSecondary(request, app_user_id, other_user_id):
	app_user = AppUser.objects.get(id=app_user_id)
	other_user = AppUser.objects.get(id=other_user_id)

	other_user = OtherUser.objects.create(app_user=other_user)

	try:
		secondary_list = SecondaryList.objects.get(app_user=app_user)

	except:
		secondary_list = SecondaryList.objects.create(app_user=app_user)

	sl = SecondaryListOtherUserConnector(secondary_list=secondary_list, other_user=other_user)
	sl.save()

	secondary_list.save()




def AddReferral(request, app_user_id, other_user_id, amount):
	app_user = AppUser.objects.get(id=app_user_id)

	referral = Referral.objects.create(app_user=app_user, other_user_id=other_user_id, amount=amount)
	referral.save()



def GetTotalAmount(request, app_user_id):
	referrals = Referral.objects.filter(app_user__id=app_user_id)

	total_amount = 0
	for item in referrals:
		total_amount += item.amount


	return total_amount
		



def GetReferralCount(request, app_user_id):
	referrals = Referral.objects.filter(app_user__id=app_user_id)

	return referrals.count()
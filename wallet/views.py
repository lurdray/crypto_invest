from django.shortcuts import render

from django.contrib import messages

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from app_user.models import *

from django.core.mail import send_mail

from datetime import datetime
import datetime as dt

import requests

# Create your views here.




def WalletView(request):
	app_user = AppUser.objects.get(user__pk=request.user.id)

	bnb_balance = requests.get("http://raytechng.pythonanywhere.com/get-bnb-balance/%s/" % (app_user.public_key))
	bep_balance = requests.get("http://raytechng.pythonanywhere.com/get-bep-balance/%s/" % (app_user.public_key))

	#return HttpResponse(str(bep_balance))
	bnb_balance = bnb_balance.json()
	bep_balance = bep_balance.json()

	context = {
		"app_user": app_user,
		"bnb_balance": bnb_balance["balance"],
		"bep_balance": bep_balance["balance"],
			
            }
	
	return render(request, "wallet/index.html", context )





def SendOpyView(request):

	app_user = AppUser.objects.get(user__pk=request.user.id)

	if request.method == "POST":
		receiver = request.POST.get("receiver")
		amount = request.POST.get("amount")

		txn_hash = requests.post("http://raytechng.pythonanywhere.com/send-bep/", data={
			"sender": app_user.public_key,
			"receiver": receiver, #opy receiver wallet address
			"amount": amount,
			"sender_key": app_user.private_key

			})

		if txn_hash:
			messages.success(request, "Sent Successfully")
			return HttpResponseRedirect(reverse("wallet:index"))

		else:
			messages.success(request, "Error: Not Success!")
			return HttpResponseRedirect(reverse("app_user:index"))




	else:
		bnb_balance = requests.get("http://raytechng.pythonanywhere.com/get-bnb-balance/%s/" % (app_user.public_key))
		bep_balance = requests.get("http://raytechng.pythonanywhere.com/get-bep-balance/%s/" % (app_user.public_key))

		#return HttpResponse(str(bep_balance))
		bnb_balance = bnb_balance.json()
		bep_balance = bep_balance.json()

		context = {
			"app_user": app_user,
			"bnb_balance": bnb_balance["balance"],
			"bep_balance": bep_balance["balance"],
				
	            }
		return render(request, "wallet/send_opy.html", context )




def SendBnbView(request):

	app_user = AppUser.objects.get(user__pk=request.user.id)

	

	if request.method == "POST":
		receiver = request.POST.get("receiver")
		amount = request.POST.get("amount")

		txn_hash = requests.post("http://raytechng.pythonanywhere.com/send-bnb/", data={
			"sender": app_user.public_key,
			"receiver": receiver, #opy receiver wallet address
			"amount": amount,
			"sender_key": app_user.private_key

			})

		if txn_hash:
			messages.success(request, "Sent Successfully")
			return HttpResponseRedirect(reverse("wallet:index"))

		else:
			messages.success(request, "Error: Not Success!")
			return HttpResponseRedirect(reverse("app_user:index"))




	else:
		bnb_balance = requests.get("http://raytechng.pythonanywhere.com/get-bnb-balance/%s/" % (app_user.public_key))
		bep_balance = requests.get("http://raytechng.pythonanywhere.com/get-bep-balance/%s/" % (app_user.public_key))

		#return HttpResponse(str(bep_balance))
		bnb_balance = bnb_balance.json()
		bep_balance = bep_balance.json()

		context = {
			"app_user": app_user,
			"bnb_balance": bnb_balance["balance"],
			"bep_balance": bep_balance["balance"],
				
	            }


		return render(request, "wallet/send_bnb.html", context )


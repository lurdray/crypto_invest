from django.shortcuts import render
from .forms import UserForm

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



def IndexView(request):
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
	
	return render(request, "app_user/index.html", context )


def SignInView(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password1")
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)

				app_user = AppUser.objects.get(user__pk=request.user.id)

				public_key = app_user.public_key
				private_key = app_user.private_key

				request.session['address'] = public_key
				request.session['key'] = private_key
				messages.success(request, "Welcome Onboard")
				return HttpResponseRedirect(reverse("app_user:index"))
			else:
				messages.warning(request, "Sorry, Invalid Login Details")
				return HttpResponseRedirect(reverse("app_user:sign_in"))
				#return HttpResponse("Sorry, Invalid Login Details")
				#return HttpResponseRedirect(reverse("main:sign_in"))

		else:
			messages.warning(request, "Sorry, Invalid Login Details")
			return HttpResponseRedirect(reverse("app_user:sign_in"))
			#return HttpResponse("Sorry, Invalid Login Details")
			#return HttpResponseRedirect(reverse("main:sign_in"))
	else:
		context = {}
		return render(request, "app_user/sign_in.html", context )




def SignUpView(request):
	if request.method == "POST":

		form = UserForm(request.POST or None, request.FILES or None)
		email = request.POST.get("username")
		full_name = request.POST.get("full_name")


		if request.POST.get("password2") != request.POST.get("password1"):
			#return HttpResponse(str("Sorry, Make Sure both passwords match"))
			messages.warning(request, "Make sure both passwords match")
			return HttpResponseRedirect(reverse("app_user:sign_up"))

			
		else:
			try:
				AppUser.objects.get(user__username=request.POST.get("username"))
				messages.warning(request, "Email Address already taken, try another one!")
				return HttpResponseRedirect(reverse("app_user:sign_up"))
				#return HttpResponse(str("Sorry, Email Address already taken, try another one!"))
				


			except:
				user = form.save()
				user.set_password(request.POST.get("password1"))
				user.save()

				app_user = AppUser.objects.create(user=user, full_name=full_name)

				#key_list = createAccount(request, account_type, email)

				#app_user.public_key = key_list[0]
				#app_user.private_key = key_list[1]

				app_user.save()

				if user:
					if user.is_active:
						login(request, user)

						app_user = AppUser.objects.get(user__pk=request.user.id)
						messages.warning(request, "One Final Step!")
						return HttpResponseRedirect(reverse("app_user:complete_sign_up", args=[email,]))

	else:
		form = UserForm()
		context = {"form": form}
		return render(request, "app_user/sign_up.html", context )



	return render(request, "app_user/sign_up.html", context )



def CompleteSignUpView(request, username):
	if request.method == "POST":

		payment_wallet_address = request.POST.get("payment_wallet_address")
		app_user = AppUser.objects.get(user__pk=request.user.id, user__username=username)

		app_user.payment_wallet_address = payment_wallet_address
		house_address = request.POST.get("house_address")
		#place_of_work = request.POST.get("place_of_work")
		dob = request.POST.get("dob")
		id_number = request.POST.get("id_number")
		state_of_origin = request.POST.get("state_of_origin")
		country = request.POST.get("country")
		language = request.POST.get("language")
		phone_no = request.POST.get("phone_no")
		bank_name = request.POST.get("bank_name")
		bank_account_name = request.POST.get("bank_account_name")
		bank_account_number = request.POST.get("bank_account_number")
		bank_verification_number = request.POST.get("bank_verification_number")
	
		app_user.house_address = house_address
		#app_user.place_of_work = place_of_work
		app_user.dob = dob
		app_user.id_number = id_number
		app_user.state_of_origin = state_of_origin
		app_user.country = country
		app_user.language = language
		app_user.phone_no = phone_no
		app_user.bank_name = bank_name
		app_user.bank_account_name = bank_account_name
		app_user.bank_verification_number = bank_verification_number
		app_user.bank_account_number = bank_account_number

		try:
			id_image = request.FILES["id_image"]
			app_user.id_image

		except:
			pass

		app_user.save()


		######crypto part

		wallet = requests.post("http://raytechng.pythonanywhere.com/create-wallet/", data={"username": app_user.user.username})
		wallet = wallet.json()
		
		#return HttpResponse(str(wallet))
		public_key = wallet["public_key"]
		private_key = wallet["private_key"]


		#public_key = "none"
		#private_key = "none"
		app_user.public_key = public_key
		app_user.private_key = private_key
		app_user.save()

		public_key = app_user.public_key
		private_key = app_user.private_key

		request.session['address'] = public_key
		request.session['key'] = private_key

		#####################

		return HttpResponseRedirect(reverse("app_user:index"))


	else:

		context = {}
		return render(request, "app_user/complete_sign_up.html", context )





def SignOutView(request):
	logout(request)

	return HttpResponseRedirect(reverse("main:index"))

		


def ProfileView(request):

	app_user = AppUser.objects.get(user__pk=request.user.id)

	if request.method == "POST":
		full_name = request.POST.get("full_name")
		house_address = request.POST.get("house_address")
		#place_of_work = request.POST.get("place_of_work")
		dob = request.POST.get("dob")
		id_number = request.POST.get("id_number")
		state_of_origin = request.POST.get("state_of_origin")
		country = request.POST.get("country")
		language = request.POST.get("language")
		phone_no = request.POST.get("phone_no")
		bank_name = request.POST.get("bank_name")
		bank_account_name = request.POST.get("bank_account_name")
		bank_account_number = request.POST.get("bank_account_number")
		bank_verification_number = request.POST.get("bank_verification_number")
	

		app_user.full_name = full_name
		app_user.house_address = house_address
		#app_user.place_of_work = place_of_work
		app_user.dob = dob
		app_user.id_number = id_number
		app_user.state_of_origin = state_of_origin
		app_user.country = country
		app_user.language = language
		app_user.phone_no = phone_no
		app_user.bank_name = bank_name
		app_user.bank_account_name = bank_account_name
		app_user.bank_verification_number = bank_verification_number
		app_user.bank_account_number = bank_account_number

		try:
			id_image = request.FILES["id_image"]
			app_user.id_image

		except:
			pass

		app_user.save()


		app_user = AppUser.objects.get(user__pk=request.user.id)
		context = {
		"app_user": app_user
			
            }


	else:

		context = {
			"app_user": app_user
				
	            }

	return render(request, "app_user/profile.html", context )





def CommitView(request):
	app_user = AppUser.objects.get(user__pk=request.user.id)
	context = {
		"app_user": app_user
			
            }
	
	return render(request, "app_user/commit.html", context )





def MakeCommitView(request, package_type):

	app_user = AppUser.objects.get(user__pk=request.user.id)

	if request.method == "POST":
		investment = Investment.objects.create(app_user=app_user, package_type=package_type)

		proof_photo1 = request.POST.get("proof_photo1")
		proof_photo2 = request.POST.get("proof_photo2")

		try:
			investment.proof_photo1 = request.FILES["proof_photo1"]

		except:
			pass

		try:
			investment.proof_photo2 = request.FILES["proof_photo2"]

		except:
			pass

		if package_type == "0.001":
			investment.amount = float(package_type)

		elif package_type == "0.002":
			investment.amount = float(package_type)

		elif package_type == "0.003":
			investment.amount = float(package_type)

		else:
			pass

		investment.payment_status = True

		today = timezone.now().date()
		nextD = today + dt.timedelta(days=7)
		nextDD = today + dt.timedelta(days=30)

		investment.switch_date7 = nextD
		investment.switch_date30 = nextDD


		investment.save()

		return HttpResponseRedirect(reverse("app_user:index"))


	else:

		context = {
				"package_type": package_type
	            }
		return render(request, "app_user/make_commit.html", context )






def MakeCommitCryptoView(request, package_type):
	app_user = AppUser.objects.get(user__pk=request.user.id)

	if request.method == "POST":
		txn_hash = requests.post("http://raytechng.pythonanywhere.com/send-bnb/", data={
			"sender": app_user.public_key,
			"receiver": "0x7d8b40BBB42D05cbFF4696AAe83AcEdb22467100", #opy receiver wallet address
			"amount": package_type,
			"sender_key": app_user.private_key

			})

		if txn_hash:

			investment = Investment.objects.create(app_user=app_user, package_type=package_type)

			if package_type == "0.001":
				investment.amount = float(package_type)

			elif package_type == "0.002":
				investment.amount = float(package_type)

			elif package_type == "0.003":
				investment.amount = float(package_type)

			else:
				pass

			investment.payment_status = True

			today = timezone.now().date()
			nextD = today + dt.timedelta(days=7)
			nextDD = today + dt.timedelta(days=30)

			investment.switch_date7 = nextD
			investment.switch_date30 = nextDD


			investment.save()

			return HttpResponseRedirect(reverse("app_user:index"))


		else:
			return HttpResponse("Not Successfull!")




	else:

		context = {
				"package_type": package_type
	            }
		return render(request, "app_user/make_commit_crypto.html", context )







def ConfirmCommitView(request, investment_id):

	app_user = AppUser.objects.get(user__pk=request.user.id)

	if request.method == "POST":
		investment = Investment.objects.get(id=investment_id)
		investment.payment_status = True
		investment.save()

		return HttpResponseRedirect(reverse("app_user:index"))


	else:

		context = {
				
	            }
		return render(request, "app_user/confirm_commit.html", context )








def InvestmentView(request):
	app_user = AppUser.objects.get(user__pk=request.user.id)
	investments = Investment.objects.filter(app_user__pk=app_user.id).order_by('-pub_date')

	total_amount = 0
	counts = 0
	for item in investments:
		counts += 1
		total_amount += float(item.amount)

	bnb_balance = requests.get("http://raytechng.pythonanywhere.com/get-bnb-balance/%s/" % (app_user.public_key))
	bep_balance = requests.get("http://raytechng.pythonanywhere.com/get-bep-balance/%s/" % (app_user.public_key))

	#return HttpResponse(str(bep_balance))
	bnb_balance = bnb_balance.json()
	bep_balance = bep_balance.json()

	context = {
		"app_user": app_user,
		"total_amount": total_amount,
		"counts": counts,
		"investments": investments,

		"bnb_balance": bnb_balance["balance"],
		"bep_balance": bep_balance["balance"],

            }

	return render(request, "app_user/investments.html", context )





def InvestmentDetailView(request, investment_id):

	if request.method == "POST":
		investment = Investment.objects.get(id=investment_id)

		if investment.request_status == False:

			switch_date7 = investment.switch_date7
			switch_date30 = investment.switch_date30
			today_date = datetime.now()

			switch_date7 = int(str(switch_date7)[:4]) + (int(str(switch_date7)[5:7])*10) + int(str(switch_date7)[8:10])
			switch_date30 = int(str(switch_date30)[:4]) + (int(str(switch_date30)[5:7])*10) + int(str(switch_date30)[8:10])
			today_date = int(str(today_date)[:4]) + (int(str(today_date)[5:7])*10) + int(str(today_date)[8:10])

			#return HttpResponse(str(switch_date30))
			if switch_date7 == today_date:
				button_status = 7
				investment.harvest_amount = investment.amount + (0.015 * investment.amount)
				investment.save()

			elif switch_date30 == today_date:
				button_status = 30
				investment.harvest_amount = investment.amount + (0.025 * investment.amount)
				investment.save()

			elif today_date > switch_date30:
				button_status = 30
				investment.harvest_amount = investment.amount + (0.025 * investment.amount)
				investment.save()

			else:
				button_status = False


			investment.request_status = True

			investment.save()

			return HttpResponseRedirect(reverse("app_user:investment"))


		else:
			return HttpResponse("Sorry, you cannot withdraw more than once.")


	else:

		investment = Investment.objects.get(id=investment_id)

		switch_date7 = investment.switch_date7
		switch_date30 = investment.switch_date30
		today_date = datetime.now()

		switch_date7 = int(str(switch_date7)[:4]) + (int(str(switch_date7)[5:7])*10) + int(str(switch_date7)[8:10])
		switch_date30 = int(str(switch_date30)[:4]) + (int(str(switch_date30)[5:7])*10) + int(str(switch_date30)[8:10])
		today_date = int(str(today_date)[:4]) + (int(str(today_date)[5:7])*10) + int(str(today_date)[8:10])

		#return HttpResponse(str(switch_date30))
		if switch_date7 == today_date:
			button_status = 7

		elif switch_date30 == today_date:
			button_status = 30

		elif today_date > switch_date30:
			button_status = 30

		else:
			button_status = False


		context = {
				"investment": investment,
				"button_status": button_status,
				
	            }
		
		return render(request, "app_user/investment_detail.html", context )


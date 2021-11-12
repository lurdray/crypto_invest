from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

import pyotp
from app_user.models import *
from urllib.parse import unquote


# Create your views here.



def GAuthenticate(request, next_reverse, arg_id=None):

	if request.method == "POST":
		key = request.POST.get("key")
		auth_key = request.session["auth_key"]

		if key == auth_key:
			app_user = AppUser.objects.get(user__pk=request.user.id)
			app_user.otp_status = True
			app_user.save()
			
			if next_reverse == "app_user_index":
				return HttpResponseRedirect(reverse("app_user:index"))
            
			elif next_reverse == "app_user_investment_detail":
				return HttpResponseRedirect(reverse("app_user:investment_detail", args=[arg_id,]))
            
			elif next_reverse == "referral_detail":
				return HttpResponseRedirect(reverse("referral:referral_detail", args=[arg_id,]))
                
			else:
				logout(request)
				messages.warning(request, "Logged Out! Incorrect Google Auth Code.")
				return HttpResponseRedirect(reverse("main:index"))
		    
			 
			#return True

		else:
			logout(request)
			messages.warning(request, "Logged Out! Incorrect Google Auth Code.")
			return HttpResponseRedirect(reverse("main:index"))

			#return False


	else:

		app_user = AppUser.objects.get(user__pk=request.user.id)
		otp_code = app_user.otp_code

		otp = pyotp.TOTP(otp_code)
		auth_key = otp.now()

		request.session["auth_key"] = auth_key


		context ={}
		return render(request, "ga_app/g_authenticate.html", context )




def CreateOtpCode(app_user_id):
	app_user = AppUser.objects.get(id=app_user_id)

	otp_code = pyotp.random_base32()
	otp = pyotp.TOTP(otp_code)

	app_user.otp_code = otp_code
	app_user.save()

	auth_str = otp.provisioning_uri(name=app_user.user.username, issuer_name="OnPointCurrency.com")
	qrcode_img_url = "https://chart.googleapis.com/chart?chs=200x200&chld=M|0&cht=qr&chl=%s" % (auth_str)
	
	qrcode_img_url = unquote(qrcode_img_url)
	x = qrcode_img_url.split("=")
	secret = x[5]

	result = secret.split("&")
	final = result[0]

	result_list = [qrcode_img_url, final]

	return result_list




def ScanQrcode(request):

	app_user = AppUser.objects.get(user__pk=request.user.id)
	request.session["ga_app_status"] = "on"
	
	if request.method == "POST":
		otp_choice = request.POST.get("otp_choice")

		if otp_choice == "Accept":
			app_user.otp_choice = True
			app_user.save()

		else:
			pass

		return HttpResponseRedirect(reverse("app_user:complete_sign_up", args=[app_user.user.username, app_user.auth_code,]))


	else:

		otp = CreateOtpCode(app_user.id)

		qrcode_img_url = otp[0]
		secret = otp[1]

		context = {"qrcode_img_url": qrcode_img_url, "secret": secret, "app_user": app_user}
		return render(request, "ga_app/scan_qrcode.html", context )


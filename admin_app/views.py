from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from app_user.models import *
from main.models import *

from referral.models import *
from referral.views import *

from django.core.mail import send_mail


# Create your views here.



def IndexView(request):
	#app_user = AppUser.objects.get(user__pk=request.user.id)
	context = {
		#"app_user": app_user
			
            }
	
	return render(request, "admin_app/index.html", context )




def InvestorsView(request):
	investors = AppUser.objects.order_by("-pub_date")

	context = {
			"investors": investors,
			
            }
	
	return render(request, "admin_app/investors.html", context )



def InvestorDetailView(request, investor_id):

	if request.method == "POST":

		investor = AppUser.objects.get(id=investor_id)


		status = request.POST.get("status")
		if status == "activate":
			investor.status = True

		elif status == "deactivate":
			investor.status = False

		else:
			pass

		investor.save()


		return HttpResponseRedirect(reverse("admin_app:investors"))




	else:

		investor = AppUser.objects.get(id=investor_id)


		context = {
				"investor": investor,
				
	            }
		
		return render(request, "admin_app/investor_detail.html", context )




def InvestmentsView(request):

	investments = Investment.objects.order_by("-pub_date")

	context = {
			"investments": investments,

            }
	
	return render(request, "admin_app/investments.html", context )



def InvestmentDetailView(request, investment_id):

	if request.method == "POST":
		investment = Investment.objects.get(id=investment_id)

		status = request.POST.get("status")
		if status == "activate":
			investment.payment_status_k = True
			RaySendMail(request, "Withdrawal Request Granted!", "Your request has been granted!", investment.app_user.user.username)


		elif status == "deactivate":
			investment.payment_status_k = False

		else:
			pass

		investment.save()
		return HttpResponseRedirect(reverse("admin_app:investments"))



	else:

		investment = Investment.objects.get(id=investment_id)

		context = {
				"investment": investment,
				
	            }
		
		return render(request, "admin_app/investment_detail.html", context )





def ReferralsView(request):
	referrals = Referral.objects.filter(request_status=True)

	context = {
			"referrals": referrals,

            }
	
	return render(request, "admin_app/referrals.html", context )




def ReferralDetailView(request, referral_id):
	#app_user = AppUser.objects.get(user__pk=request.user.id)
	
	referral = Referral.objects.get(id=referral_id)

	if request.method == "POST":
		referral.paid_status = True
		referral.save()
		RaySendMail(request, "Withdrawal Request Granted!", "Your request has been granted!", referral.app_user.user.username)


		return HttpResponseRedirect(reverse("admin_app:referrals"))


	else:

		context = {
			"referral": referral,
		}

		return render(request, "admin_app/referral_detail.html", context )





def WithdrawsView(request):

	withdraws = Investment.objects.filter(request_status=True).order_by("-pub_date")

	context = {
			"withdraws": withdraws,

            }
	
	return render(request, "admin_app/withdraws.html", context )



def WithdrawDetailView(request, withdraw_id):

	if request.method == "POST":
		withdraw = Investment.objects.get(id=withdraw_id)
		investment = Investment.objects.get(id=withdraw_id)

		status = request.POST.get("status")
		if status == "activate":
			withdraw.ha_payment_status = True


			primary_lists = PrimaryList.objects.all()
			for i in primary_lists:
				for j in i.other_users.all():
					if j.app_user.id == investment.app_user.id:

						other_user_id = investment.app_user.id
						app_user_id = i.app_user.id
						amount = 0.005*(float(investment.harvest_amount))

						AddReferral(request, app_user_id, other_user_id, amount)

					else:
						#return HttpResponse(str("Some shit!"))
						pass


			secondary_lists = SecondaryList.objects.all()
			for i in secondary_lists:
				for j in i.other_users.all():
					if j.app_user.id == investment.app_user.id:
						
						other_user_id = investment.app_user.id
						app_user_id = i.app_user.id
						amount = 0.002*(float(investment.harvest_amount))

						AddReferral(request, app_user_id, other_user_id, amount)

					else:
						pass



		elif status == "deactivate":
			withdraw.ha_payment_status = False

		else:
			pass

		withdraw.save()
		return HttpResponseRedirect(reverse("admin_app:withdraws"))



	else:

		withdraw = Investment.objects.get(id=withdraw_id)

		context = {
				"withdraw": withdraw,
				
	            }
		
		return render(request, "admin_app/withdraw_detail.html", context )







def TransactionView(request):
	context = {
			
            }
	
	return render(request, "admin_app/transaction.html", context )




def MessageView(request):

	messages = Contact.objects.order_by('-pub_date')

	context = {
			"messages": messages,
            }
	
	return render(request, "admin_app/message.html", context )





def NftView(request):

	if request.method == "POST":
		pass


	else:

		nfts = Nft.objects.all().order_by("-pub_date")

		context = {
			"nfts": nfts
            }
		
		return render(request, "admin_app/nfts.html", context )




def AddNftView(request):

	if request.method == "POST":
		title = request.POST.get("title")
		amount = request.POST.get("amount")

		image = request.FILES["image"]


		nft = Nft.objects.create(title=title, amount=amount)

		nft.image = image
		nft.save()

		messages.warning(request, "NFT Added")
		return HttpResponseRedirect(reverse("admin_app:add_nft"))


	else:

		context = {
			
            }
		
		return render(request, "admin_app/add_nft.html", context )





def NftStatusView(request, nft_id):
	if request.method == "POST":

		nft = Nft.objects.get(id=nft_id)

		if nft.status == True:
			nft.status = False

		else:
			nft.status = True

		nft.save()

		return HttpResponseRedirect(reverse("admin_app:nft"))




	else:
		pass




def NftClaimersView(request, nft_id):

	if request.method == "POST":
		pass


	else:

		nft = Nft.objects.get(id=nft_id)
		claimers = nft.claimers.all()

		context = {
			"nft": nft,
			"claimers": claimers,
            }
		
		return render(request, "admin_app/nft_claimers.html", context )



def SignOutView(request):
	logout(request)

	return HttpResponseRedirect(reverse("main:index"))

		
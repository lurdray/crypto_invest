from django.urls import path
from . import views

app_name = "wallet"

urlpatterns = [

	path("wallet/", views.WalletView, name="index"),
	path("wallet/send-opy/", views.SendOpyView, name="send_opy"),
	path("wallet/send-bnb/", views.SendBnbView, name="send_bnb"),

]
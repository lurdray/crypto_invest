from django.urls import path
from . import views

app_name = "referral"

urlpatterns = [

	path("app/referral/", views.IndexView, name="index"),
	path("app/referral-detail/<int:referral_id>/", views.ReferralDetailView, name="referral_detail"),

]
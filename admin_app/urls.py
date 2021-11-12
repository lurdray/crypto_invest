from django.urls import path
from admin_app import views

app_name = "admin_app"

urlpatterns = [

	path("app/admin/", views.IndexView, name="index"),

	path("app/admin/investors/", views.InvestorsView, name="investors"),
	path("app/admin/investor-detail/<int:investor_id>/", views.InvestorDetailView, name="investor_detail"),

	path("app/admin/investments/", views.InvestmentsView, name="investments"),
	path("app/admin/investment-detail/<int:investment_id>/", views.InvestmentDetailView, name="investment_detail"),
	
	path("app/admin/investment/withdraws/", views.WithdrawsView, name="withdraws"),
	path("app/admin/investment/withdraw-detail/<int:withdraw_id>/", views.WithdrawDetailView, name="withdraw_detail"),

	path("app/admin/referrals/", views.ReferralsView, name="referrals"),
	path("app/admin/referral-detail/<int:referral_id>/", views.ReferralDetailView, name="referral_detail"),

	path("app/admin/investments/transaction/", views.TransactionView, name="transaction"),

	path("app/admin/message", views.MessageView, name="message"),

	path("app/admin/nft", views.NftView, name="nft"),
	path("app/admin/add-nft/", views.AddNftView, name="add_nft"),
	path('status/<int:nft_id>/', views.NftStatusView, name="nft_status"),
	path('nft-claimers/<int:nft_id>/', views.NftClaimersView, name="nft_claimers"),



	path('sign-out/', views.SignOutView, name="sign_out"),

]
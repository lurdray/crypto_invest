from django.urls import path
from . import views

app_name = "app_user"

urlpatterns = [

	path("app/", views.IndexView, name="index"),
	path("sign-up-payment/", views.SignUpPaymentView, name="sign_up_payment"),
	path("sign-up/", views.SignUpView, name="sign_up"),
	path('complete-sign-up/<str:username>/<str:auth_code>/', views.CompleteSignUpView, name='complete_sign_up'),
	path("sign-up/mgs/", views.SignUpMsgView, name="sign_up_msg"),
	path("sign-in/", views.SignInView, name="sign_in"),
	path('sign-out/', views.SignOutView, name="sign_out"),

	path('set-new-password/<str:email>/<str:auth_code>/', views.SetNewPwView, name='set_new_password'),
	path('forgot-password/', views.ForgotPasswordView, name='forgot_password'),
	path('forgot-password/msg/', views.ForgotPwMsgView, name='forgot_pw_msg'),


	path('profile/', views.ProfileView, name="profile"),
	
	path('commit/', views.CommitView, name="commit"),
	path('make-commit/<str:package_type>/', views.MakeCommitView, name="make_commit"),
	path('make-commit/<str:package_type>/crypto/', views.MakeCommitCryptoView, name="make_commit_crypto"),

	path('confirm-commit/<str:package_type>/', views.ConfirmCommitView, name="confirm_commit"),

	path('investment/', views.InvestmentView, name="investment"),
	path('investment-detail/<int:investment_id>/', views.InvestmentDetailView, name="investment_detail"),

	path('lock-investment/<int:investment_id>/', views.LockInvestmentView, name="lock_investment"),
	
	path('nfts/', views.NftsView, name="nfts"),
	path('claim-nft/<int:nft_id>/', views.ClaimNftView, name="claim_nft"),


]
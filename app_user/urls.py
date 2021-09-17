from django.urls import path
from . import views

app_name = "app_user"

urlpatterns = [

	path("app/", views.IndexView, name="index"),

	path("sign-up/", views.SignUpView, name="sign_up"),
	path('complete-sign-up/<str:username>/', views.CompleteSignUpView, name='complete_sign_up'),
	path("sign-in/", views.SignInView, name="sign_in"),
	path('sign-out/', views.SignOutView, name="sign_out"),

	path('profile/', views.ProfileView, name="profile"),
	
	path('commit/', views.CommitView, name="commit"),
	path('make-commit/<str:package_type>/', views.MakeCommitView, name="make_commit"),
	path('make-commit/<str:package_type>/crypto/', views.MakeCommitCryptoView, name="make_commit_crypto"),

	path('confirm-commit/<str:package_type>/', views.ConfirmCommitView, name="confirm_commit"),

	path('investment/', views.InvestmentView, name="investment"),
	path('investment-detail/<int:investment_id>/', views.InvestmentDetailView, name="investment_detail"),

]
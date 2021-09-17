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

	path("app/admin/investments/transaction/", views.TransactionView, name="transaction"),

	path('sign-out/', views.SignOutView, name="sign_out"),

]
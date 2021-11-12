from django.urls import path
from . import views

app_name = "ga_app"

urlpatterns = [

	path("authenticate/<str:next_reverse>/<int:arg_id>/", views.GAuthenticate, name="authenticate"),
	path("scan-qr-code/", views.ScanQrcode, name="scan_qrcode"),
	
]
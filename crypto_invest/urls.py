from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("", include("main.urls")),
    path("", include("admin_app.urls")),
    path("", include("app_user.urls")),
    path("", include("wallet.urls")),
    path("", include("referral.urls")),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
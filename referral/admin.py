from django.contrib import admin
from referral.models import *

# Register your models here.
admin.site.register(Referral)
admin.site.register(PrimaryList)
admin.site.register(SecondaryList)
admin.site.register(OtherUser)
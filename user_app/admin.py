from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(CustomUser,UserAdmin)
admin.site.register(otp)
admin.site.register(Kycverification)
admin.site.register(coins)
admin.site.register(setup)
admin.site.register(paymentmethod)
admin.site.register(buying_history)
admin.site.register(selling_history)
admin.site.register(giftcards)
admin.site.register(giftcardbuying_history)
admin.site.register(Network)
admin.site.register(airtime_Transaction)
admin.site.register(balance)
admin.site.register(balance_history)
admin.site.register(recent_activity)
admin.site.register(dataplan)
admin.site.register(datap_history)
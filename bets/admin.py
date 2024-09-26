from django.contrib import admin
from .models import UserWallet, Bet, Transaction, Notification


admin.site.register(UserWallet)
admin.site.register(Bet)
admin.site.register(Transaction)
admin.site.register(Notification)
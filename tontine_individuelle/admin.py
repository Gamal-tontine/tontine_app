from django.contrib import admin
from .models import Owner, Deposit, Reminder

admin.site.register(Owner)
admin.site.register(Deposit)
admin.site.register(Reminder)
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def _str_(self):
        return self.user.username

class Deposit(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def _str_(self):
        return f"{self.owner.user.username} - {self.amount} - {self.date}"

class Reminder(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def _str_(self):
        return f"{self.owner.user.username} - {self.date} - Paid: {self.is_paid}"

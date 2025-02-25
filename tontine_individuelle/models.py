import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import localdate, timedelta
from payement.models import Acquitement
from datetime import date


class TontineIndividuelle(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    amount = models.DecimalField(max_digits=20,decimal_places=0, default=0)
    create_at = models.DateField(auto_now_add=True)
    admin = models.ForeignKey('account.User', on_delete=models.PROTECT, related_name='tontine_individuelle_admin')
    user = models.ForeignKey("account.User", verbose_name="", related_name='user_tontine_individuelle' , on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def end_date(self):
        end_date = self.create_at + timedelta(days=29)
        return end_date
    
    @property
    def nbr_days(self):
        day = timezone.now().date()
        difference = day - self.create_at
        return difference.days
    
    @property
    def payement(self):
        return Acquitement.objects.filter(user= self.user, tontine = self)
    
    @property
    def objectif(self):
        return self.amount * 30
    
    @property
    def statue(self):
        if self.objectif == self.balance or self.nbr_days >= 31:
            return False
        else:
            return True
    
               
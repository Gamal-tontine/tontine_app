from django.db import models

CHOISE_MOYEN = [
    ('cash','payement cash'),
    ('orange','Orange Money'),
    ('paycard','Paycard'),
]

class Acquitement(models.Model):
    amount = models.IntegerField(null=False)
    date = models.DateTimeField(auto_now_add=True)
    tontine = models.ForeignKey('tontine.TontineCollective', on_delete=models.PROTECT, related_name='acquitement')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    moyen = models.CharField(max_length=10,choices=CHOISE_MOYEN,default='cash')

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.date})"
    
    def count_paiement_def(self):
        self.count_paiement += 1
        return self.count_paiement


class Payment(models.Model):
    tontine = models.ForeignKey("tontine.TontineCollective", on_delete=models.CASCADE, related_name="payments")
    recipient = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name='payement')
    amount = models.BigIntegerField()
    date = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)  

    def __str__(self):
        return f"Paiement de {self.amount} à {self.recipient.first_name} ({'Payé' if self.is_paid else 'Non payé'})"
    


class AcquitementIndividuelle(models.Model):
    amount = models.IntegerField(null=False)
    date = models.DateTimeField(auto_now_add=True)
    tontine = models.ForeignKey('tontine_individuelle.TontineIndividuelle', on_delete=models.PROTECT, related_name='acquitement_individuelle')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    moyen = models.CharField(max_length=10,choices=CHOISE_MOYEN,default='cash')

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.date})"

class PaymentIndividuelle(models.Model):
    tontine = models.ForeignKey("tontine_individuelle.TontineIndividuelle", on_delete=models.CASCADE, related_name="payments_individuelle")
    recipient = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name='payement_individuelle')
    amount = models.DecimalField(max_digits=20, decimal_places=0, blank=False, null=False)
    date = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)  # Marque si le paiement a été effectué

    def __str__(self):
        return f"Paiement de {self.amount} à {self.recipient.first_name} ({'Payé' if self.is_paid else 'Non payé'})"
    



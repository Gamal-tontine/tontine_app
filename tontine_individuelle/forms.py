# tontine/forms.py
from django import forms

class DepositForm(forms.Form):
    amount = forms.DecimalField(label='Montant du dépôt', max_digits=10, decimal_places=2)

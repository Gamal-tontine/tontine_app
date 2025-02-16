# tontine/forms.py
from django import forms

from .models import TontineIndividuelle
from account.models import User

class TontineIndividuelleForm(forms.ModelForm):
    name = forms.CharField(max_length=30,required=True,label='Nom', widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    description = forms.CharField(max_length=250,required=True,label='Description', widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    amount = forms.IntegerField(min_value=10000,help_text='minimum 10000',required=True,label='Montant', widget=forms.TextInput(attrs={'class':'form-control','type':'number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','type':'emailfield'}))
    class Meta:
        model = TontineIndividuelle
        fields = ('name','description','amount','email')
        

class TontineIndividuelleUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=30,required=True,label='Nom', widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    description = forms.CharField(max_length=250,required=True,label='Description', widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    amount = forms.IntegerField(min_value=10000,help_text='minimum 10000',required=True,label='Montant', widget=forms.TextInput(attrs={'class':'form-control','type':'number'}))
    class Meta:
        model = TontineIndividuelle
        fields = ('name','description','amount',)
        

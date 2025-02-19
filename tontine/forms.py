from django import forms

from .models import TontineCollective,TontineIndividuelle

class TontineCollectiveForm(forms.ModelForm):
    name = forms.CharField(max_length=30,required=True,label='Nom', widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    description = forms.CharField(max_length=250,required=True,label='Description', widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    limite_member = forms.IntegerField(min_value=2,required=True,label='Nombre de personne', widget=forms.TextInput(attrs={'class':'form-control' ,'type':'number'}))
    amount = forms.IntegerField(min_value=10000,help_text='minimum 10000',required=True,label='Montant', widget=forms.TextInput(attrs={'class':'form-control','type':'number'}))

    class Meta:
        model = TontineCollective
        fields = ('name','description','limite_member','amount','frequence','order_paiemement',)
        widgets = {
            'frequence': forms.Select(attrs={'class':'form-control'}),
            'order_paiement': forms.Select(attrs={'class':'form-control'}),
        }


class TontineIndeviduelleForm(forms.ModelForm):
    name = forms.CharField(max_length=30,required=True,label='Nom', widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    description = forms.CharField(max_length=250,required=True,label='Description', widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    amount = forms.IntegerField(min_value=10000,help_text='minimum 10000',required=True,label='Montant', widget=forms.TextInput(attrs={'class':'form-control','type':'number'}))

    class Meta:
        model = TontineIndividuelle
        fields = ('name','description','amount',)

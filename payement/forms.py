from django import forms

from .models import Acquitement,Payment,AcquitementIndividuelle

class AcquitementForm(forms.ModelForm):
    amount = forms.IntegerField(required=True,min_value=1000,help_text='minimum: 10000',label='Montant',widget=forms.NumberInput(attrs={'class':'form-control'}))

    class Meta:
        model = Acquitement
        fields = ('amount','moyen',)
        widgets = {
            'moyen': forms.Select(attrs={'class':'form-control'})
        }
        
class AcquitementIndividuelleForm(forms.ModelForm):
    amount = forms.IntegerField(required=True,min_value=1000,help_text='minimum: 10000',label='Montant',widget=forms.NumberInput(attrs={'class':'form-control'}))

    class Meta:
        model = AcquitementIndividuelle
        fields = ('amount','moyen',)
        widgets = {
            'moyen': forms.Select(attrs={'class':'form-control'})
        }
        
    

from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login
from django.core.exceptions import ValidationError

from .utils.send_mail import sender_mail
from .models import User



class CreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required= True, label='Prenom:',widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Votre prenom'}))
    last_name = forms.CharField(max_length=30, required=True, label='Nom:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Votre nom'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'form-control','type':'email', 'placeholder':'exemple@gmail.com'}))
    phone_number = forms.IntegerField(label='Numero de Telephone',widget=forms.NumberInput(attrs={'class':'form-control', 'type':'tel' , 'placeholder':'620xxxxxx'}))
    profil = forms.ImageField(label='photo de profil', required=True, widget=forms.FileInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Mot de pass', required=True, widget=forms.TextInput(attrs={'class':'form-control','type':'password' , 'placeholder':'••••••••'}))
    password2 = forms.CharField(label='Confirmation de mot de passe', required=True, widget=forms.TextInput(attrs={'class':'form-control','type':'password', 'placeholder':'••••••••'}))

    class Meta:
        model = User
        fields = ('first_name',
                    'last_name',
                    'email',
                    'phone_number',
                    'profil',
                    'statue',
                    'password1',
                    'password2',
                    )
        widgets = {
            'statue': forms.Select(attrs={'class':'form-control', 'readonly':'readonly'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('le mail doit pas etre vide')
        if User.objects.filter(email = email).exists():
            raise ValidationError('le mail existe deja dans la base de donnee') 
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError('le champ mot de pass doit etre remplie')
        
        if password1 != password2:
            raise ValidationError('les mots de pass sont differents')
        return password2


class LoginForm(AuthenticationForm):
    username = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'type':'email','placeholder':'exemple@gmail.com'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control','type':'password', 'placeholder':'••••••••'}))
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is None:
            raise ValidationError('les informations entrer sont incorects')
        if not user.is_active:
            sender_mail(user)
            raise ValidationError('le compte nest pas activer veillez consulter votre mail pour l\activer')

        return self.cleaned_data
    
class AccountFindForPasswordForm(forms.Form):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control', 'type':'email','placeholder':'exemple@gmail.com'}))
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("Aucun compte associé à cette adresse e-mail.")
        return email
    
class NewPasswordForm(forms.Form):
    password1 = forms.CharField(label='Nouveau mot de pass', required=True, widget=forms.TextInput(attrs={'class':'form-control','type':'password'}))
    password2 = forms.CharField(label='Confirmation', required=True, widget=forms.TextInput(attrs={'class':'form-control','type':'password'}))

    def claen_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError('les mots de passes se correspondent pas')
        if len(password2) < 5:
            raise ValidationError('le mot de passe doit etre supperieur a 5')
        if not any(char.isalpha() for char in password2):
            raise ValidationError('le mot de pass doit contenir au moin une lettre')
        if not any(num.isdigit() for num in password2):
            raise ValidationError('le mot de passe doit comporter au moin un chiffre')
        if not any(upp.isupper() for upp in password2):
            raise ValidationError('le mot de passe doit comporter au moin un majuscule')
        
        return password2

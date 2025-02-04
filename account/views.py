from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.views import View
from django.db import transaction
from django.contrib import messages
from django.urls import reverse_lazy

from .utils.decrypte import decrypte_token
from .forms import CreateForm, LoginForm, AccountFindForPasswordForm,NewPasswordForm
from .models import User
from .utils.send_mail import sender_mail,send_mail_for_password

class CreateUserView(CreateView):
    form_class = CreateForm
    model = User
    template_name = 'account/singup.html'
    success_url = reverse_lazy('account:singin')

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            sender_mail(user)
        messages.success(request=self.request,
                         message='Le compte a été cree avec success')
    
class LoginView(LoginView):
    authentication_form = LoginForm
    success_url = reverse_lazy('admin_tontine:dashboard')
    template_name = 'account/singin.html'
    def get_success_url(self):
        return self.success_url
    
    
class ActivationAccoutnView(View):
    def get(self,uid,token):
        user = decrypte_token(uid,token)
        if user is not None:
            user.is_active = True
            user.save()
            messages.success(request=self.request, message='Votre compte a été activer avec sucess')
            return redirect('account:singin')
        else:
            return render(request=self.request, template_name='account/error_activation.html')
        
class AccountFindForPasswordView(View):
    def get(self,request):
        form = AccountFindForPasswordForm()
        return render(request=request, template_name='account/find_account_by_password.html',context={'form':form})
    def post(self,request):
        form = AccountFindForPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                send_mail_for_password(request,user)
                messages.success(request,'le mail de reinitialisation a été envoyer a votre mail')
                return redirect('account:singin')
            except User.DoesNotExist:
                messages.error(request=request, message='le compte entrer n\'est associer a aucun compte')
            
        else:
            messages.error(request, 'le formulaire n\est pas valide')
        return render(request, 'account/find_account_by_password.html', {'form': form})


    def post(self, request):
        form = AccountFindForPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                # Envoyer l'e-mail de réinitialisation
                send_mail_for_password(request, user)
                messages.success(request, 'Le mail de réinitialisation a été envoyé à votre adresse.')
                return redirect('account:signin')  # Assurez-vous que ce nom d'URL est correct
            except User.DoesNotExist:
                # Cela ne devrait pas arriver si le formulaire est bien configuré
                messages.error(request, 'Le compte entré n’est associé à aucun utilisateur.')
        else:
            # Les erreurs de validation seront automatiquement affichées dans le formulaire
            messages.error(request, 'Le formulaire n’est pas valide.')

        # Réutiliser le formulaire contenant les erreurs
        return render(request, 'account/find_account_by_password.html', {'form': form})

class NewPasswordView(View):
    user = None
    def get(self,request,uid,token):
        user = decrypte_token(uid,token)
        if user is not None:
            form = NewPasswordForm()
            return form
        else:
            return render(request=request, template_name='account/error_activation.html')
        
    def post(self,request):
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password2')
            with transaction.atomic():
                self.user.set_password(password)
                self.user.save()
            messages.success(request,'le mot de passe a été changer avec succes')
            return redirect('')
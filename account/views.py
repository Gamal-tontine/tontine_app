from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic.edit import CreateView

from .forms import AccountFindForPasswordForm
from .forms import CreateForm
from .forms import LoginForm
from .forms import NewPasswordForm
from .models import User
from .utils.decrypte import decrypte_token
from .utils.send_mail import send_mail_for_password
from .utils.send_mail import sender_mail


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
                         message='Le compte a été cree avec success.'
                         'un mail d\'activation vous a été envoyer merci de cliquez.')
        return redirect(self.success_url)


class LoginView(LoginView):
    authentication_form = LoginForm
    success_url = reverse_lazy('admin_tontine:dashboard')
    user_dashboard_link = reverse_lazy('user_tontine:user_dashboard')
    template_name = 'account/singin.html'

    def get_success_url(self):
        if self.request.user.statue == 'user':
            return self.user_dashboard_link
        else:
            return self.success_url


class ActivationAccountView(View):
    def get(self, request, uid, token):
        id = urlsafe_base64_decode(uid)
        try:
            user = User.objects.get(pk=id)
        except ValueError:
            return render(request=self.request, template_name='account/error_activation.html')

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request=self.request,
                             message='Votre compte a été activé avec succès')
            return redirect('account:singin')
        else:
            return render(request=self.request, template_name='account/error_activation.html')


class AccountFindForPasswordView(View):
    def get(self, request):
        form = AccountFindForPasswordForm()
        return render(request=request, template_name='account/find_account_by_password.html', context={'form': form})

    def post(self, request):
        form = AccountFindForPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                send_mail_for_password(request, user)
                messages.success(
                    request, 'le mail de reinitialisation a été envoyer a votre mail')
                return redirect('account:singin')
            except User.DoesNotExist:
                messages.error(
                    request=request, message='le compte entrer n\'est associer a aucun compte')

        else:
            messages.error(request, 'le formulaire n\est pas valide')
        return render(request, 'account/find_account_by_password.html', {'form': form})


class NewPasswordView(View):
    def get(self, request, uid, token):
        try:
            user_id = int(urlsafe_base64_decode(uid).decode())
            user = User.objects.get(pk=user_id)
        except (ValueError, TypeError, User.DoesNotExist):
            return render(request, 'account/error_activation.html')

        if default_token_generator.check_token(user, token):
            request.session['user_id'] = user.id
            form = NewPasswordForm()
            return render(request, 'account/new_password.html', {'form': form})
        else:
            return render(request, 'account/error_activation.html')

    def post(self, request, uid, token):
        form = NewPasswordForm(request.POST)
        user_id = request.session.get('user_id')

        if not user_id:
            return render(request, 'account/error_activation.html')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return render(request, 'account/error_activation.html')

        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if password1 == password2:
                with transaction.atomic():
                    user.set_password(password1)
                    user.save()

                messages.success(
                    request, 'Le mot de passe a été changé avec succès.')
                del request.session['user_id']
                return redirect('account:singin')
            else:
                messages.error(
                    request, "Les mots de passe ne correspondent pas.")

        return render(request, 'account/new_password.html', {'form': form})


def profil(request):
    user = request.user
    return render(request, 'account/profil.html', {'user': user})


class LogOutView(View):
    def get(self, request):
        logout(request=request)
        return redirect('account:singin')

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from config.settings import DOMAINE
from django.contrib import messages

def sender_mail(user):
    subject = 'Mail d\'activation'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    context = {
        'uid': uid,
        'token': token,
        'user': user,
        'domaine': DOMAINE
    }
    message = render_to_string(template_name='account/activation_account.html', context=context)
    send_mail(subject=subject, message=message, from_email='dounoh0@gmail.com', recipient_list=[user.email], fail_silently=True)

def send_mail_for_password(request, user):
    subject = 'Demande de réinitialisation de mot de passe'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    context = {
        'uid': uid,
        'user': user,
        'token': token,
        'domain': DOMAINE
    }
    message = render_to_string(template_name='account/reset_password_email.html', context=context)
    try:
        send_mail(subject=subject,
                  message=message,
                  from_email='dounoh0@gmail.com',
                  recipient_list=[user.email],
                  fail_silently=False)
    except Exception:
        messages.error(request, 'Erreur d\'envoi du mail')

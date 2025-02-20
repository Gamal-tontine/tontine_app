from django.core.mail import send_mail
from celery import shared_task
from account.models import User
from django.shortcuts import get_object_or_404
from config.settings import DEFAULT_FROM_EMAIL


@shared_task
def send_mail_acquitement(user_id,amount):
    user = get_object_or_404(User, pk=user_id)
    send_mail(
        subject='Acquitement tontine',
        message= f'cher(e) {user.first_name} {user.last_name} votre acquitement du jours la somme de {amount} GNF pour la tontine a ete affectuer avec success ',
        from_email= DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )


@shared_task
def sender_mail_for_info(email,subject,message):
    send_mail(subject=subject,message=message,
              from_email=DEFAULT_FROM_EMAIL,
              recipient_list=[email])

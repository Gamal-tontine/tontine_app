from celery import shared_task
from django.core.mail import send_mail
from .models import TontineCollective
from config.settings import DEFAULT_FROM_EMAIL
from django.shortcuts import get_object_or_404

@shared_task
def reminder_paiement_for_day():
    tontines = TontineCollective.objects.all()
    for tontine in tontines:
        if tontine.frequence == 'jours':
            user_liste = [member.email for member in tontine.members.all()]
            for email in user_liste:
                send_mail(
                    'Rappel de paiement',
                    f'Ceci est un rappel pour votre prochain acquitement de la  Tontine.{tontine.name} ',
                    DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )


@shared_task
def reminder_paiement_for_week():
    tontines = TontineCollective.objects.all()
    for tontine in tontines:
        if tontine.frequence == 'semaine':
            user_liste = [member.email for member in tontine.members.all()]
            for email in user_liste:
                send_mail(
                    'Rappel de paiement',
                    f'Ceci est un rappel pour votre prochain acquitement de la  Tontine.{tontine.name} ',
                    DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

@shared_task
def reminder_paiement_for_month():
    tontines = TontineCollective.objects.all()
    for tontine in tontines:
        if tontine.frequence == 'mois':
            user_liste = [member.email for member in tontine.members.all()]
            for email in user_liste:
                send_mail(
                    'Rappel de paiement',
                    f'Ceci est un rappel pour votre prochain acquitement de la  Tontine.{tontine.name} ',
                    DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )


@shared_task
def recipient_date():
    tontines = TontineCollective.objects.all()
    for tontine in tontines:
        if tontine.periode_amount == tontine.objectif:
            send_mail(
                subject='RAPPEL DE PAIEMENT',
                message= f' chere administrateur la tontine {tontine.name} a atteinte la fin de sa periode vous pouvez payer le preneur merci',
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[tontine.admin.email]
            )

@shared_task
def mail_for_start_tontine(tontine_id):
    tontine = get_object_or_404(TontineCollective,pk=tontine_id)
    admin = tontine.admin
    send_mail(
        'DEMARAGE',
        f'la tontine {tontine.name} peut maintenant commencer les membres sont au grand complet merci.',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[admin.email]
    )

@shared_task
def starte_tontine(tontine_id):
    tontine = get_object_or_404(TontineCollective,pk=tontine_id)
    user_liste = [member.email for member in tontine.members.all()]
    for email in user_liste:
        send_mail(
            'Anonce ',
            f'chere membre de la tontine nous vous informons que la tontine {tontine.name} a ete demarer',
            DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
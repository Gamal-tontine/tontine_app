from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView,ListView,DetailView,UpdateView
from django.views import View
from django.db import transaction
from django.contrib import messages
from django.core.mail import send_mail

from config.settings import DEFAULT_FROM_EMAIL
from tontine.models import TontineCollective
from account.models import User
from .froms import AcquitementForm
from .models import Acquitement

class AcquitementView(View):
    def post(self, request, uid_tontine, id_user):
        tontine = get_object_or_404(TontineCollective, uid=uid_tontine)
        user = get_object_or_404(User, id=id_user)

        form = AcquitementForm(request.POST)
        if form.is_valid():
            acquitement = form.save(commit=False)
            with transaction.atomic():
                acquitement.tontine = tontine
                acquitement.user = user
                acquitement.save()
                # Envoyer l'email
                send_mail(
                    'Paiement de l\'acquittement',
                    f'Votre paiement de {acquitement.amount} GNF pour la tontine {tontine.name} a été effectué avec succès.',
                    'noreply@example.com',  # Changez par DEFAULT_FROM_EMAIL si défini
                    [user.email],
                )
            messages.success(request, 'Acquittement effectué avec succès.')
            return redirect('tontine:detail_tontine', tontine.uid)
        else:
            # Si le formulaire n'est pas valide, afficher les erreurs
            messages.error(request, 'Erreur dans le formulaire. Veuillez réessayer.')
            return render(request, 'tontine/acquitement_form.html', {'form': form, 'tontine': tontine})
        

# def pay_preneur(tontine):
#     # Vérifier si tous les membres ont payé
#     all_paid_members = tontine.payers.count()
#     total_members = tontine.total_members

#     # Si tous les membres ont payé, procéder au paiement
#     if all_paid_members == total_members:
#         recipient = tontine.next_recipient

#         # Vérifier si un paiement a déjà été effectué pour cette période
#         if not Payment.objects.filter(tontine=tontine, recipient=recipient, date=tontine.period_end_date).exists():
#             # Créer un enregistrement de paiement pour ce membre
#             payment = Payment.objects.create(
#                 tontine=tontine,
#                 recipient=recipient,
#                 amount=tontine.amount,
#                 is_paid=True  # Marquer comme payé
#             )

#             # Envoyer une notification au preneur
#             tontine.send_payment_notification(recipient, payment.amount)

#             return payment
#         else:
#             return None
#     else:
#         # Si tous les membres n'ont pas payé, ne pas procéder au paiement
#         return None

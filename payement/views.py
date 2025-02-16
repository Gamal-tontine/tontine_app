from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView,ListView,DetailView,UpdateView
from django.views import View
from django.db import transaction
from django.contrib import messages
from django.core.mail import send_mail
from .utils.send_mail_info import sender_mail_for_info

from config.settings import DEFAULT_FROM_EMAIL
from tontine.models import TontineCollective, TontineIndividuelle
from account.models import User
from .forms import AcquitementForm
from .models import Acquitement,Payment, AcquitementIndividuelle

class AcquitementCollectiveView(View):
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
                    'dounoh0y@gmail.com', 
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



class HistoriqueView(View):
    def get(self, request, user, tontine):
        payement = Payment.objects.filter(tontine = tontine, recipient = user)
        acquitement = Acquitement.objects.filter(tontine = tontine, user = user)
        context = {
            'payement': payement,
            'acquitement': acquitement
        }
        return render(request= request, temeplate_name = 'payement/historique.html', context= context)
    
   
class AcquitementIndividuelleAdmin(View):
    def post(self,request,uid):
        tontine = get_object_or_404(TontineIndividuelle,uid = uid)
        amount = request.POST.get('amount')
        moyen = request.POST.get('moyen')
        amount = int(amount)
        if amount > tontine.objectif or (amount + tontine.balance) > tontine.objectif:
            messages.error(request=request, message='le montant saisie est superieur a l objectif de la tontine')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)
        if not amount < tontine.amount:
            with transaction.atomic():
                AcquitementIndividuelle.objects.create(user = tontine.user,amount = amount,moyen =moyen,tontine = tontine)
                tontine.balance += amount
                tontine.save()
                sender_mail_for_info(tontine.user.email,'paiement effectuer',f'votre paiement a bien ete effectuer pour la tontine {tontine.name}')
            messages.success(request=request, message='le paiement a bien ete effectuer')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)
        else:
            messages.error(request=request, message='le montant saisie est inferieur au montant a deposer chaque jours')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)


class PayementIndividuelleView(View):
    def post(self,request,uid):
        tontine = get_object_or_404(TontineIndividuelle,uid=uid)
        if not tontine.objectif  == tontine.balance:
            messages.error(request,'vous ne pouvez pas effectuer le payement')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)
        with transaction.atomic():
            Payment.objects.create(tontine= tontine,recipient=tontine.user,amount= tontine.balence )
            tontine.balance = 0.0
            tontine.save()
            sender_mail_for_info(tontine.user.email,'Payement de la tontine',f'Cher(e) {tontine.user.first_name} vous avez reçu virement de {tontine.balence - tontine.amount} GNF pour votre participation a la tontine individuelle {tontine.name}')
        messages.success(request,'le payement a ete effectuer avec success ')
    
    
class AcquitementIndividuelleUserView(View):
    def post(self,request,uid):
        tontine = get_object_or_404(TontineIndividuelle,uid = uid)
        amount = request.POST.get('amount')
        moyen = request.POST.get('moyen')
        amount = int(amount)
        if amount > tontine.objectif or (amount + tontine.balance) > tontine.objectif:
            messages.error(request=request, message='le montant saisie est superieur a l objectif de la tontine')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)
        if not amount < tontine.amount:
            with transaction.atomic():
                AcquitementIndividuelle.objects.create(user = request.user,amount = amount,moyen =moyen,tontine = tontine)
                tontine.balance += amount
                tontine.save()
                sender_mail_for_info(tontine.user.email,'paiement effectuer',f'votre paiement de {amount} GNF a bien ete effectuer pour la tontine {tontine.name}')
            messages.success(request=request, message='le paiement a bien ete effectuer')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)
        else:
            messages.error(request=request, message='le montant saisie est inferieur au montant a deposer chaque jours')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)


from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .forms import AcquitementForm
from .models import Acquitement
from .models import AcquitementIndividuelle
from .models import Payment
from .models import PaymentIndividuelle
from .tasks import send_mail_acquitement
from .tasks import sender_mail_for_info
from account.models import User
from config.settings import DEFAULT_FROM_EMAIL
from tontine.models import Blocked_user
from tontine.models import TontineCollective
from tontine_individuelle.models import TontineIndividuelle


class AcquitementCollectiveView(View):
    def post(self, request, uid_tontine, id_user):
        tontine = get_object_or_404(TontineCollective, uid=uid_tontine)
        user = get_object_or_404(User, id=id_user)

        form = AcquitementForm(request.POST)

        if form.is_valid():
            acquitement = form.save(commit=False)
            if not Acquitement.objects.filter(date=timezone.now().date()).exists():
                with transaction.atomic():
                    acquitement.tontine = tontine
                    acquitement.user = user
                    acquitement.save()
                    tontine.periode_amount += acquitement.amount
                    tontine.save()
                    send_mail_acquitement.apply_async(
                        args=[user.pk, acquitement.amount])
                messages.success(request, 'Acquittement effectué avec succès.')
                if request.user.statue == 'admin':
                    return redirect('tontine:detail_tontine', tontine.uid)
                else:
                    return redirect('user_tontine:tontine_collective', tontine.uid)

            messages.error(
                request, 'Erreur dans le formulaire. Veuillez réessayer.')
            return render(request, 'tontine/acquitement_form.html', {'form': form, 'tontine': tontine})


class PayementCollective(View):
    template = 'payement/confirme_paiement.html'

    def _can_make_payment(self, tontine):
        return tontine.objectif <= tontine.periode_amount

    def paiement(self, tontine, recipient, amount, blocked_list):
        if recipient.id not in blocked_list:
            with transaction.atomic():
                Payment.objects.create(
                    tontine=tontine,
                    recipient=recipient,
                    amount=amount
                )
                tontine.periode_amount -= int(amount)
                tontine.save()

                sender_mail_for_info.apply_async(args=[
                    recipient.email,
                    'Paiement de la tontine',
                    f'Vous avez reçu votre paiement de la tontine {tontine.name} '
                    f'd\'une somme de {amount} GNF'
                ])

            messages.success(self.request, 'Paiement effectué avec succès')
            return render(self.request, self.template, {'context': 'Le paiement a été effectué avec succès', 'confirm': False})

        messages.error(
            self.request, 'Ce membre est sur la liste noire et ne peut pas recevoir sa paie')
        return redirect('tontine:detail_tontine', tontine.uid)

    def get(self, request, uid):
        tontineCollective = get_object_or_404(TontineCollective, uid=uid)

        if not tontineCollective.start_at:
            messages.error(
                request, 'Paiement impossible, la tontine n\'a pas débuté !!')
            return redirect('tontine:detail_tontine', tontineCollective.uid)

        recipient = get_object_or_404(
            User, pk=tontineCollective.recipient_tontine_id)
        blocked_users_ids = Blocked_user.objects.values_list('id', flat=True)

        if self._can_make_payment(tontineCollective):
            return self.paiement(
                tontine=tontineCollective,
                recipient=recipient,
                amount=tontineCollective.periode_amount,
                blocked_list=blocked_users_ids
            )

        if blocked_users_ids:
            return render(request, self.template, {
                'context': 'Tous les membres de cette tontine n\'ont pas effectué l\'intégralité de leurs acquittements. '
                           'Voulez-vous passer au paiement du preneur ?',
                'confirm': True,
                'tontine_uid': tontineCollective.uid
            })

        messages.error(request, 'Paiement impossible pour le moment !!')
        return redirect('tontine:detail_tontine', tontineCollective.uid)

    def post(self, request, uid):
        tontineCollective = get_object_or_404(TontineCollective, uid=uid)
        recipient = get_object_or_404(
            User, pk=tontineCollective.recipient_tontine_id)

        blocked_users_ids = Blocked_user.objects.values_list('id', flat=True)

        if self._can_make_payment(tontineCollective):
            return self.paiement(
                tontine=tontineCollective,
                recipient=recipient,
                amount=tontineCollective.periode_amount,
                blocked_list=blocked_users_ids
            )

        messages.error(request, 'Paiement impossible pour le moment !!')
        return redirect('tontine:detail_tontine', tontineCollective.uid)


def unblock_user_after_payment(request, tontine_uid, user_id):
    tontine = get_object_or_404(TontineCollective, uid=tontine_uid)
    user = get_object_or_404(User, pk=user_id)
    blocked_user = Blocked_user.objects.filter(user=user).first()

    if not blocked_user:
        messages.info(
            request, "l'utilisateur n'est pas sur la liste des utilisateurs bloqués.")
        return redirect('tontine:detail_tontine', tontine.uid)

    # Vérifier si l'utilisateur a payé la totalité du montant dû
    amount_due = blocked_user.amount_due
    if request.method == "POST":
        amount_paid = request.POST.get("amount_paid")

        amount_paid = int(amount_paid)

        if amount_paid < amount_due:
            messages.error(
                request, f"Le montant payé est insuffisant. Vous devez payer {amount_due} GNF.")
            return redirect('tontine:detail_tontine', tontine.uid)

        # Si tout est bon, procéder au paiement et débloquer l'utilisateur
        with transaction.atomic():
            Acquitement.objects.create(
                tontine=tontine,
                user=user,
                amount=amount_paid,
                moyen='cash'
            )

            # Supprimer l'utilisateur de la liste des bloqués
            blocked_user.delete()

        messages.success(
            request, "Votre paiement a été effectué avec succès, vous êtes maintenant débloqué.")
        return redirect('tontine:detail_tontine', tontine.uid)

    return redirect('tontine:detail_tontine', tontine.uid)


class AcquitementIndividuelleAdmin(View):
    def post(self, request, uid):
        tontine = get_object_or_404(TontineIndividuelle, uid=uid)
        amount = request.POST.get('amount')
        moyen = request.POST.get('moyen')
        amount = int(amount)
        if amount > tontine.objectif or (amount + tontine.balance) > tontine.objectif:
            messages.error(
                request=request, message='le montant saisie est superieur a l objectif de la tontine')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)
        if not amount < tontine.amount:
            with transaction.atomic():
                AcquitementIndividuelle.objects.create(
                    user=tontine.user, amount=amount, moyen=moyen, tontine=tontine)
                tontine.balance += amount
                tontine.save()
                sender_mail_for_info.apply_async(
                    args=[
                        tontine.user.email,
                        'paiement effectuer',
                        f'votre paiement a bien ete effectuer pour la tontine {tontine.name}']
                )

            messages.success(
                request=request, message='le paiement a bien ete effectuer')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)
        else:
            messages.error(
                request=request, message='le montant saisie est inferieur au montant a deposer chaque jours')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)


class AcquitementIndividuelleUserView(View):
    def post(self, request, uid):
        tontine = get_object_or_404(TontineIndividuelle, uid=uid)
        amount = request.POST.get('amount')
        moyen = request.POST.get('moyen')
        amount = int(amount)
        if amount > tontine.objectif or (amount + tontine.balance) > tontine.objectif:
            messages.error(
                request=request, message='le montant saisie est superieur a l objectif de la tontine')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)
        if not amount < tontine.amount:
            with transaction.atomic():
                AcquitementIndividuelle.objects.create(
                    user=request.user, amount=amount, moyen=moyen, tontine=tontine)
                tontine.balance += amount
                tontine.save()
                sender_mail_for_info.apply_async(
                    args=[tontine.user.email,
                          'paiement effectuer',
                          f'votre paiement de {amount} GNF a bien ete effectuer pour la tontine {tontine.name}'])
            messages.success(
                request=request, message='le paiement a bien ete effectuer')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)
        else:
            messages.error(
                request=request, message='le montant saisie est inferieur au montant a deposer chaque jours')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)


class PayementIndividuelleView(View):
    def get(self, request, uid):
        tontine = get_object_or_404(TontineIndividuelle, uid=uid)
        if not tontine.objectif == tontine.balance:
            messages.error(request, 'vous ne pouvez pas effectuer le payement')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)
        with transaction.atomic():
            PaymentIndividuelle.objects.create(
                tontine=tontine, recipient=tontine.user, amount=tontine.balance)
            tontine.balance = 0
            tontine.paid = True
            tontine.save()
            sender_mail_for_info.apply_async(
                args=[
                    tontine.user.email,
                    'Payement de la tontine',
                    f'Cher(e) {tontine.user.first_name} vous avez reçu virement de {tontine.balance - tontine.amount} GNF pour votre participation a la tontine individuelle {tontine.name}'])
        messages.success(request, 'le payement a ete effectuer avec success ')
        return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)


class HistoriqueView(View):
    def get(self, request, user, tontine):
        payement = Payment.objects.filter(tontine=tontine, recipient=user)
        acquitement = Acquitement.objects.filter(tontine=tontine, user=user)
        context = {
            'payement': payement,
            'acquitement': acquitement
        }
        return render(request=request, temeplate_name='payement/historique.html', context=context)


class HistoriqueView(View):
    def get(self, request, user, tontine):
        users = get_object_or_404(User, pk=user)
        tontines = get_object_or_404(TontineCollective, uid=tontine)

        payement = Payment.objects.filter(tontine=tontines, recipient=users)
        acquitement = Acquitement.objects.filter(tontine=tontines, user=users)

        context = {
            'payement': payement,
            'acquitement': acquitement,
            'user': user,
            'tontine': tontines
        }
        return render(request, 'payement/historique.html', context)

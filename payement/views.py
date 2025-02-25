from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView,ListView,DetailView,UpdateView
from django.views import View
from django.db import transaction
from django.contrib import messages
from django.utils import timezone
from config.settings import DEFAULT_FROM_EMAIL
from tontine.models import TontineCollective
from account.models import User
from .tasks import send_mail_acquitement,sender_mail_for_info
from .forms import AcquitementForm
from tontine_individuelle.models import TontineIndividuelle
from .models import Acquitement,Payment, AcquitementIndividuelle,PaymentIndividuelle

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
                    send_mail_acquitement.apply_async(args=[user.pk,acquitement.amount])
                messages.success(request, 'Acquittement effectué avec succès.')
                return redirect('tontine:detail_tontine', tontine.uid)
                
            messages.error(request, 'Erreur dans le formulaire. Veuillez réessayer.')
            return render(request, 'tontine/acquitement_form.html', {'form': form, 'tontine': tontine})
       

class PayementCollective(View):
    def paiement(self,tontine,recipient,amount, bloked_list):
        if not recipient in bloked_list:
            with transaction.atomic():
                paiement = Payment()
                paiement.tontine = tontine
                paiement.recipient = recipient
                paiement.amount = amount
                paiement.save()
                tontine.periode_amount = tontine.periode_amount - int(tontine.objectif)
                tontine.save()
                sender_mail_for_info.apply_async(args=[recipient.email,
                                                    'Payement de la tontine',
                                                    f'Vous avez reçu votre paiement de la tontine {tontine.name}'
                                                        ' d\'une somme de {tontine.periode_amount} GNF'])
            messages.success(request=self.request,message='Paiement effectuer avec success')
            context = {'context': 'le paiement effectuer avec success',
                       'confirm': False
                        }
            return render(request=self.request,template_name='payement/confirme_paiement', context=context)
        
        else:
            messages.error(request=self.request, message='ce membre est deja sur la liste noire et peut pas recevoire sa paye')
            tontine.recipient()
            tontine.save()
            return redirect('tontine:detail_tontine', tontine.uid)


    def get(self,uid):
        tontineCollective = get_object_or_404(TontineCollective,uid=uid)
        recipient = get_object_or_404(User,pk= TontineCollective.recipient_tontine_id)
        blocked_user = tontineCollective.blocked_members

        if tontineCollective.objectif <= tontineCollective.periode_amount:
            self.paiement(tontine=tontineCollective,
                          recipient=recipient,
                          amount=tontineCollective.periode_amount,
                          bloked_list= blocked_user)
        
        if blocked_user:
            context = {
                'context': 'Tous les membres de cette tontine n\'ont '
                            'pas effectuer l\'integraliter de leurs acquitements '
                            'vous voulez passer au payement du preneur?',
                'confirm': True
            }
            return render(request=self.request,template_name='payement/confirme_paiement', context=context)
        else:
            messages.error(self.request,'paiement impossible pour le moment !!')
            return redirect('tontine:detail_tontine', tontineCollective.uid)
        


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
                sender_mail_for_info.apply_async(
                    args=[
                        tontine.user.email,
                        'paiement effectuer',
                        f'votre paiement a bien ete effectuer pour la tontine {tontine.name}']
                        )
                        
            messages.success(request=request, message='le paiement a bien ete effectuer')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)
        else:
            messages.error(request=request, message='le montant saisie est inferieur au montant a deposer chaque jours')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)


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
                sender_mail_for_info.apply_async(
                    args= [tontine.user.email,
                           'paiement effectuer',
                           f'votre paiement de {amount} GNF a bien ete effectuer pour la tontine {tontine.name}'])
            messages.success(request=request, message='le paiement a bien ete effectuer')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)
        else:
            messages.error(request=request, message='le montant saisie est inferieur au montant a deposer chaque jours')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)



class PayementIndividuelleView(View):
    def get(self,request,uid):
        tontine = get_object_or_404(TontineIndividuelle,uid=uid)
        if not tontine.objectif  == tontine.balance:
            messages.error(request,'vous ne pouvez pas effectuer le payement')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)
        with transaction.atomic():
            PaymentIndividuelle.objects.create(tontine= tontine,recipient=tontine.user,amount= tontine.balance )
            tontine.balance = 0
            tontine.paid = True
            tontine.save()
            sender_mail_for_info.apply_async(
                args=[
                    tontine.user.email,
                    'Payement de la tontine',
                    f'Cher(e) {tontine.user.first_name} vous avez reçu virement de {tontine.balance - tontine.amount} GNF pour votre participation a la tontine individuelle {tontine.name}'])
        messages.success(request,'le payement a ete effectuer avec success ')
        return redirect('tontine_individuelle:datail_tontine_individuelle', tontine.uid)

    

class HistoriqueView(View):
    def get(self, request, user, tontine):
        payement = Payment.objects.filter(tontine = tontine, recipient = user)
        acquitement = Acquitement.objects.filter(tontine = tontine, user = user)
        context = {
            'payement': payement,
            'acquitement': acquitement
        }
        return render(request= request, temeplate_name = 'payement/historique.html', context= context)
    

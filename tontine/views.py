from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

from .models import TontineCollective, TontineIndividuelle
from .forms import TontineCollectiveForm, TontineIndeviduelleForm
from .utils.qr_generator import qr_code_generator
from config.settings import DOMAINE
from payement.forms import AcquitementForm  # Correction : 'froms' -> 'forms'


def generate_link(uid):
    """ Génère un lien vers la tontine en fonction de l'UID """
    return f"http://{DOMAINE}{reverse_lazy('tontine:joined_tontine', args=[uid])}"


class CreateTontineView(LoginRequiredMixin, View):
    def post(self, request):
        form = TontineCollectiveForm(request.POST)
        if form.is_valid():
            tontine = form.save(commit=False)
            tontine.admin = request.user
            tontine.save()
            tontine.members.add(request.user)  # L'admin est membre par défaut

            # Générer le lien et le QR code
            link = generate_link(uid=tontine.uid)
            try:
                tontine.qr_code = qr_code_generator(link)
                tontine.save()
            except Exception as e:
                return HttpResponseBadRequest(f"Erreur lors de la génération du QR code : {e}")

            messages.success(request, "Tontine créée avec succès !")
            return render(request, 'tontine/link_tontine.html', {'tontine': tontine, 'link': link})
        
        messages.error(request, "Le formulaire est invalide. Veuillez corriger les erreurs.")
        return render(request, 'tontine/form_tontine.html', {'form': form})


class JoingedTontineView(LoginRequiredMixin, View):
    def get(self, request, uid):
        tontine = get_object_or_404(TontineCollective, uid=uid)
        return render(request, 'tontine/join_confirmation.html', {'tontine': tontine})

    def post(self, request, uid):
        tontine = get_object_or_404(TontineCollective, uid=uid)
        
        if tontine.members.count() < tontine.limite_member and not tontine.members.filter(pk=request.user.pk).exists():
            tontine.members.add(request.user)
            tontine.save()
            messages.success(request, "Vous avez rejoint la tontine avec succès.")
            return redirect('tontine:detail_tontine', uid=tontine.uid)
        else:
            messages.error(request, "Impossible de rejoindre : La tontine est complète ou vous êtes déjà membre.")
            return redirect('tontine:joined_tontine', uid=tontine.uid)


class DetailTontineView(LoginRequiredMixin, DetailView):
    model = TontineCollective
    template_name = 'tontine/detail_tontine.html'
    context_object_name = 'tontine'

    def get_object(self):
        return get_object_or_404(TontineCollective, uid=self.kwargs.get('uid'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tontine = context['tontine']
        context.update({
            'is_full': tontine.is_full,
            'payers': tontine.payers,
            'non_payers': tontine.non_payers,
            'members_due_amounts': tontine.members_due_amounts,
            'non_payers_count': tontine.non_payers_count(),
            'payers_count': tontine.payers_count,
            'acquitement': AcquitementForm(),
        })
        return context    


class PageLinkTontineView(LoginRequiredMixin, View):
    def get(self, request, uid):
        tontine = get_object_or_404(TontineCollective, uid=uid)
        link = generate_link(tontine.uid)
        return render(request, 'tontine/link_tontine.html', {'tontine': tontine, 'link': link})


class DeleteTontineView(LoginRequiredMixin, View):
    def post(self, request, uid):
        tontine = get_object_or_404(TontineCollective, uid=uid)

        if not tontine.is_full and not tontine.is_finished:
            tontine.delete()
            messages.success(request, "Tontine supprimée avec succès.")
            return redirect('admin_tontine:dashboard')
        else:
            messages.error(request, "Suppression impossible : une tontine en cours ne peut pas être supprimée.")
            return redirect('tontine:detail_tontine', uid=tontine.uid)


class UpdateTontineView(LoginRequiredMixin, UpdateView):
    model = TontineCollective
    form_class = TontineCollectiveForm
    template_name = 'tontine/update_tontine.html'
    context_object_name = 'form'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_success_url(self):
        messages.success(self.request, "Tontine mise à jour avec succès.")
        return reverse('tontine:detail_tontine', kwargs={'uid': self.object.uid})


@login_required
def demarrer_tontine(request, uid):
    tontine = get_object_or_404(TontineCollective, uid=uid)
    tontine.start_tontine()
    messages.success(request, "Tontine démarrée avec succès.")
    return redirect('tontine:detail_tontine', uid=tontine.uid)

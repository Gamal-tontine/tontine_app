from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import CreateView,DetailView,ListView,DeleteView,UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.urls import reverse

from .models import TontineCollective,TontineIndividuelle
from .forms import TontineCollectiveForm,TontineIndeviduelleForm
from .utils.qr_generator import qr_code_generator
from config.settings import DOMAINE
from payement.froms import AcquitementForm



def generate_link(uid):
    url='tontine:joined_tontine'
    return f"http://{DOMAINE}/{reverse_lazy(url, args=[uid]).lstrip('/')}"

class CreateTontineView(LoginRequiredMixin,View):
    def post(self, request):
        form = TontineCollectiveForm(request.POST)
        if form.is_valid():
            tontine = form.save(commit=False)
            tontine.admin = request.user
            tontine.save()
            tontine.members.add(request.user) 

            # Générer le lien et le QR code
            link = generate_link(uid=tontine.uid)  
            try:
                code_qr = qr_code_generator(link)  
                tontine.qr_code = code_qr
                tontine.save()
            except Exception as e:
                return HttpResponseBadRequest(f"Erreur lors de la génération du QR code : {e}")

            return render(
                request,
                'tontine/link_tontine.html',
                {'tontine': tontine, 'link': link}
            )
        else:
            messages.error(request, "Le formulaire est invalide.")
            return HttpResponseBadRequest("Formulaire invalide.")

        
class JoingedTontineView(LoginRequiredMixin,View):
    def get(self, request, uid):
        try:
            tontine = TontineCollective.objects.get(uid=uid)
            return render(request, 'tontine/join_confirmation.html', context={'tontine': tontine})
        except TontineCollective.DoesNotExist:
            return HttpResponseBadRequest("Tontine non trouvée.")

    def post(self, request, uid):
        try:
            tontine = TontineCollective.objects.get(uid=uid)
            tontine.members.add(request.user)
            tontine.save()
            return redirect('tontine:detail_tontine', tontine.uid)
        except TontineCollective.DoesNotExist:
            return HttpResponseBadRequest("Tontine non trouvée.")


class DetailTontineView(LoginRequiredMixin,DetailView):
    model = TontineCollective
    template_name = 'tontine/detail_tontine.html'
    context_object_name = 'tontine'

    def get_object(self):
        uid = self.kwargs.get('uid')
        return get_object_or_404(TontineCollective, uid=uid)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tontine = context['tontine']
        context['is_full'] = tontine.is_full  # Vérifier si la tontine est complète
        context['payers'] = tontine.payers  # Membres qui ont payé
        context['non_payers'] = tontine.non_payers  # Membres qui n'ont pas payé
        context['non_payers_amounts'] = tontine.non_payers_amounts()  # Montants dus par les non-payeurs
        context['non_payers_count'] = tontine.non_payers_count()  # Nombre de non-payeurs
        context['payers_count'] = tontine.payers_count  # Nombre de payeurs
        context['acquitement'] = AcquitementForm()
        return context    
    

class PageLinkTontineView(LoginRequiredMixin,View):
    def get(self,request,uid):
        tontine = get_object_or_404(TontineCollective,uid=uid)
        link = generate_link(tontine.uid)
        return render(request=request,template_name='tontine/link_tontine.html', context={'tontine': tontine,'link':link})


class DeleteTontineView(View):
    def post(self,request,uid):
        tontine = get_object_or_404(TontineCollective,uid=uid)

        if not tontine.is_full or not tontine.is_finished:
            tontine.delete()
            messages.success(request=request,message='tontine supprimer avec success')
            return redirect('admin_tontine:dashboard')
        else:
            messages.success(request,'Suppression impossible une tontine en cours ne peut pas etre supprimer')
            return redirect('tontine:detail_tontine', tontine.uid)
        

class UpdateTontineView(UpdateView):
    model = TontineCollective
    form_class = TontineCollectiveForm
    template_name = 'tontine/update_tontine.html'
    context_object_name = 'form'
    slug_field = 'uid' 
    slug_url_kwarg = 'uid'

    def get_success_url(self):
        return reverse('tontine:detail_tontine', kwargs={'uid': self.object.uid})
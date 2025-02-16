from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from tontine.models import TontineCollective
from payement.models import Acquitement,AcquitementIndividuelle
from tontine_individuelle.models import TontineIndividuelle

class TontineView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  

        tontine_collectives = TontineCollective.objects.filter(members=request.user)
        tontine_individuelles = TontineIndividuelle.objects.filter(user=request.user)

        return render(request, 'user_tontine/index.html', {
            'tontine_collectives': tontine_collectives,
            'tontine_individuelles': tontine_individuelles
        })
        
class TontineCollectiveView(DetailView):
    model = TontineCollective
    template_name = 'user_tontine/collective/detail.html'
    context_object_name = 'tontine'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class TontineIndividuelleView(DetailView):
    model = TontineIndividuelle
    template_name = 'user_tontine/individuelle/detail.html'
    context_object_name = 'tontine'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        acquitements = AcquitementIndividuelle.objects.filter(user=self.request.user, tontine=context['tontine'])
        context['acquitements'] = acquitements
        return context

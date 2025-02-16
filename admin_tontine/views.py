from django.shortcuts import render
from tontine.forms import TontineCollectiveForm
from tontine.models import TontineCollective
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from tontine_individuelle.models import TontineIndividuelle
from tontine_individuelle.forms import TontineIndividuelleForm

class DashboardView(TemplateView):
    template_name = 'admin_tontine/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Formulaires
        context['form'] = TontineCollectiveForm()
        context['tontine_individuelle_form'] = TontineIndividuelleForm()

        # Pagination des tontines collectives
        tontines = TontineCollective.objects.filter(admin=self.request.user).order_by('-id')
        paginator = Paginator(tontines, 5)  # Affiche 10 éléments par page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['tontines'] = page_obj

        # Pagination des tontines individuelles
        tontine_individuelle = TontineIndividuelle.objects.filter(admin=self.request.user).order_by('-id')
        paginator_individuelle = Paginator(tontine_individuelle, 5)  # Affiche 10 éléments par page
        page_number_individuelle = self.request.GET.get('page_individuelle')
        page_obj_individuelle = paginator_individuelle.get_page(page_number_individuelle)
        context['tontine_individuelles'] = page_obj_individuelle
        
        # Variables supplémentaires si nécessaire
        context['admin'] = ''  # Remplacer selon votre besoin
        context['user'] = ''   # Remplacer selon votre besoin

        return context

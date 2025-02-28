from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView

from tontine.forms import TontineCollectiveForm
from tontine.models import TontineCollective
from tontine_individuelle.forms import TontineIndividuelleForm
from tontine_individuelle.models import TontineIndividuelle


class DashboardView(TemplateView):
    template_name = 'admin_tontine/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = TontineCollectiveForm()
        context['tontine_individuelle_form'] = TontineIndividuelleForm()

        # Pagination des tontines collectives
        tontines = TontineCollective.objects.filter(
            admin=self.request.user).order_by('-id')
        paginator = Paginator(tontines, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['tontines'] = page_obj

        # Pagination des tontines individuelles
        tontine_individuelle = TontineIndividuelle.objects.filter(
            admin=self.request.user).order_by('-id')
        paginator_individuelle = Paginator(tontine_individuelle, 5)
        page_number_individuelle = self.request.GET.get('page_individuelle')
        page_obj_individuelle = paginator_individuelle.get_page(
            page_number_individuelle)
        context['tontine_individuelles'] = page_obj_individuelle

        # Variables supplémentaires si nécessaire
        context['active'] = 0
        context['inactive'] = 0
        context['individuelle'] = tontine_individuelle.count()
        context['collective'] = tontines.count()

        for tontine in tontines:
            if tontine.start_at:
                context['active'] += 1
            else:
                context['inactive'] += 1

        for indivi in tontine_individuelle:
            if indivi.statue:
                context['inactive'] += 1
            else:
                context['active'] += 1

        return context

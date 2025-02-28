from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView

from account.models import User
from payement.forms import AcquitementForm
from payement.forms import AcquitementIndividuelleForm
from payement.models import Acquitement
from payement.models import AcquitementIndividuelle
from tontine.models import Blocked_user
from tontine.models import TontineCollective
from tontine_individuelle.models import TontineIndividuelle


class TontineView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('account:login')

        tontine_collectives = TontineCollective.objects.filter(
            members=request.user).order_by('-create_at')
        tontine_individuelles = TontineIndividuelle.objects.filter(
            user=request.user).order_by('-create_at')
        active = 0
        inactive = 0
        individuelle = tontine_individuelles.count()
        collective = tontine_collectives.count()

        for tontine in tontine_collectives:
            if tontine.start_at:
                active += 1
            else:
                inactive += 1

        for indivi in tontine_individuelles:
            if indivi.statue:
                inactive += 1
            else:
                active += 1
        context = {
            'tontine_collectives': tontine_collectives,
            'tontine_individuelles': tontine_individuelles,
            'active': active,
            'inactive': inactive,
            'individuelle': individuelle,
            'collective': collective,
        }
        return render(request, 'user_tontine/index.html', context)


class TontineCollectiveView(LoginRequiredMixin, DetailView):
    model = TontineCollective
    template_name = 'user_tontine/collective/detail.html'
    context_object_name = 'tontine'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tontine = context['tontine']
        user = User.objects.get(pk=tontine.recipient_tontine_id)
        username = f'{user.first_name} {user.last_name} '
        is_blocked = Blocked_user.objects.filter(
            user=self.request.user, tontine=tontine).exists()
        acquitement = AcquitementForm()
        context.update({
            'is_blocked': is_blocked,
            'non_payers': tontine.unpaid_members,
            'recipient_periode': username,
            'non_payers_count': tontine.unpaid_members_count,
            'payers_count': tontine.paid_members_count,
            'acquitement': acquitement
        })
        return context


class TontineIndividuelleView(LoginRequiredMixin, DetailView):
    model = TontineIndividuelle
    template_name = 'user_tontine/individuelle/detail.html'
    context_object_name = 'tontine'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_context_data(self, **kwargs):
        acquitementform = AcquitementIndividuelleForm()
        context = super().get_context_data(**kwargs)
        acquitements = AcquitementIndividuelle.objects.filter(
            user=self.request.user, tontine=context['tontine'])
        context['acquitements'] = acquitements
        context['acquitementform'] = acquitementform
        return context

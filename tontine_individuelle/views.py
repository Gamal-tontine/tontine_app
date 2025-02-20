from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views import View
from django.urls import reverse
from django.db import transaction
from django.views.generic import CreateView, DetailView,DeleteView,ListView,UpdateView
from payement.models import Payment
from payement.forms import AcquitementIndividuelleForm
from .utils.send_mail_info import sender_mail_for_info
from .models import TontineIndividuelle
from payement.models import AcquitementIndividuelle
from .forms import TontineIndividuelleForm,TontineIndividuelleUpdateForm
from account.models import User



class DetailTontineIndividuelleView(View):
    def get(self, request, uid):
        try:
            tontine = TontineIndividuelle.objects.select_related('user','admin').get(uid = uid)
            acquitements = AcquitementIndividuelle.objects.filter(user = tontine.user, tontine= tontine)
            acquitementform = AcquitementIndividuelleForm()
            context = {
                'tontine': tontine,
                'admin' : tontine.admin,
                'user' : tontine.user,
                'acquitements': acquitements,
                'acquitementform': acquitementform
            }
        except TontineIndividuelle.DoesNotExist:
            return ValueError("la tontine n'existe pas ")
        return render(request=request, template_name='tontine_individuelle/index.html', context=context)
    
class CreateTontineIndividuelleView(View):
    def post(self,request):
        form = TontineIndividuelleForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']            
            try:
                user = User.objects.get(email= email)
            except User.DoesNotExist:
                messages.error(request=request, message='le mail saisie est incorect')
                return redirect('admin_tontine:dashboard')
            with transaction.atomic():
                tontine_idividuelle = form.save(commit=False)
                tontine_idividuelle.admin = request.user
                tontine_idividuelle.user = user
                tontine_idividuelle.save()
            messages.success(request=request,message='tontine creer avec succes')
            return redirect('tontine_individuelle:datail_tontine_individuelle', tontine_idividuelle.uid)
        else:
            messages.error(request, message='le formulaire est invalide veillez verifier le mail de utilisateur')
            return redirect('admin_tontine:dashboard')
        
class UpdateTontineView(UpdateView):
    form_class = TontineIndividuelleUpdateForm
    model = TontineIndividuelle
    template_name = 'tontine_individuelle/update_tontine_individuelle.html' 
    context_object_name = 'form'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    
    def get_success_url(self):
        messages.success(self.request, "Tontine mise à jour avec succès.")
        return reverse('tontine_individuelle:datail_tontine_individuelle', kwargs={'uid': self.object.uid})
     

def delete_tontine_individuelle(request,uid):
    tontine = get_object_or_404(TontineIndividuelle,uid= uid)
    tontine.delete()
    return redirect('admin_tontine:dashboard')


class CategoryTontineIndividuelle(ListView):
    model = TontineIndividuelle
    template_name = 'tontine_individuelle/tontine_liste.html'
    context_object_name = 'tontines'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_value = self.request.GET.get('search_value', '')

        if self.request.user.statue == 'admin':
            queryset = queryset.filter(admin=self.request.user)
        else:
            queryset = queryset.filter(user=self.request.user)

        if search_value:
            queryset = queryset.filter(name__icontains=search_value) 

        return queryset

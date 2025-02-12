from django.shortcuts import render
from tontine.forms import TontineCollectiveForm
from tontine.models import TontineCollective
from django.contrib.auth.decorators import login_required

from tontine_individuelle.models import TontineIndividuelle

@login_required
def dashboard(request):
    tontine = TontineCollective.objects.filter(admin=request.user).order_by('-id')
    tontine_individuelle = TontineCollective.objects.select_related('user','admin').all()
    form = TontineCollectiveForm()
    
    context = {
        'form':form,
        'tontines':tontine,
        'tontine_individuelles': tontine_individuelle,
        'admin':tontine_individuelle.admin,
        'user': tontine_individuelle.user,
    }
    return render(request, template_name='admin_tontine/index.html',context=context)


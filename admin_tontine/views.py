from django.shortcuts import render
from tontine.forms import TontineCollectiveForm
from tontine.models import TontineCollective
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    tontine = TontineCollective.objects.filter(admin=request.user).order_by('-id')
    form = TontineCollectiveForm()
    context = {
        'form':form,
        'tontines':tontine,
    }
    return render(request, template_name='admin_tontine/index.html',context=context)
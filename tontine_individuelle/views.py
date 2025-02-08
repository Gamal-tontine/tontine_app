from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Owner, Deposit, Reminder
from .forms import DepositForm
from django.utils import timezone

@login_required
def home(request):
    owner = get_object_or_404(Owner, user=request.user)
    deposits = Deposit.objects.filter(owner=owner)
    reminders = Reminder.objects.filter(owner=owner)

    today = timezone.now().date()
    today_reminder = reminders.filter(date=today).first()

    if not today_reminder:
        Reminder.objects.create(
            owner=owner,
            message="N'oubliez pas de faire votre dépôt quotidien.",
            is_paid=False
        )
        today_reminder = Reminder.objects.filter(owner=owner, date=today).first()

    context = {
        'owner': owner,
        'deposits': deposits,
        'today_reminder': today_reminder,
    }
    return render(request, 'tontine/home.html', context)

@login_required
def deposit(request):
    owner = get_object_or_404(Owner, user=request.user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            Deposit.objects.create(owner=owner, amount=amount)
            owner.balance += amount
            owner.save()

            today = timezone.now().date()
            reminder = Reminder.objects.filter(owner=owner, date=today).first()
            if reminder:
                reminder.is_paid = True
                reminder.save()

            messages.success(request, 'Dépôt effectué avec succès !')
            return redirect('home')
    else:
        form = DepositForm()
    return render(request, 'tontine/deposit.html', {'form': form})


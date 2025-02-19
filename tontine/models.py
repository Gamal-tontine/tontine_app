import uuid
import calendar
from django.db import models
from django.db.models import Count, Sum, OuterRef, Exists
from django.utils.timezone import localdate, timedelta
from django.utils import timezone
from datetime import datetime, date
from payement.models import Acquitement, Payment
from random import randint

FREQUENCY_CHOICES = [
    ('jour', 'Chaque jour'),
    ('semaine', 'Chaque semaine'),
    ('mois', 'Une fois par mois'),
]

PAYMENT_ORDER_CHOICES = [
    (1, 'Aléatoire'),
    (2, "Par ordre d'adhésion"),
]

class TontineCollective(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    limite_member = models.IntegerField()
    amount = models.BigIntegerField()
    frequence = models.CharField(choices=FREQUENCY_CHOICES, default='jour', max_length=12)
    order_paiemement = models.IntegerField(choices=PAYMENT_ORDER_CHOICES, default=1)
    create_at = models.DateField(auto_now_add=True)
    start_at = models.DateField(null=True, blank=True)
    admin = models.ForeignKey('account.User', on_delete=models.PROTECT, related_name='admin_tontine_collective')
    members = models.ManyToManyField('account.User', related_name='member_tontines_collective')
    qr_code = models.ImageField(upload_to='tontine_qrcode/', blank=True, null=True)
    periode_amount = models.IntegerField(default=0)
    recipient_tontine_id = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def total_members(self):
        return self.members.count()

    def total_revenu(self):
        return self.total_members * self.amount

    @property
    def is_full(self):
        return self.members.count() >= self.limite_member
    
    def start_tontine(self):
        if self.total_members == self.limite_member:
            self.start_at = timezone.now()
        
    def end_date_tontine(self):
        if self.start_tontine:
            month = self.start_at.day + timedelta(days=29)
            return month * self.total_members
        else:
            return None
        
    def recipient(self):
        """Retourne le prochain membre qui recevra l'argent."""
        if self.order_paiemement == 1:
            members = list(self.members.all())
            random = randint(0, len(members) - 1)
            while Payment.objects.filter(recipient=members[random]).exists():
                random = randint(0, len(members) - 1)
            self.recipient_tontine_id = members[random].pk
        else:
            members = list(self.members.all().order_by('id'))
            for member in members:
                if not Payment.objects.filter(recipient=member).exists():
                    self.recipient_tontine_id = member.pk
                    break
    
    @property
    def unpaid_members(self):
        """Retourne les membres qui n'ont pas encore payé et combien ils doivent payer."""
        unpaid_members = []
        for member in self.members.all():
            last_payment = Payment.objects.filter(tontine=self, recipient=member).order_by('-date').first()
            if not last_payment or not last_payment.is_paid:
                unpaid_members.append({
                    "user": member,
                    "amount_due": self.amount,
                    "days_overdue": (timezone.now().date() - (last_payment.date if last_payment else self.start_at)).days,
                })
        return unpaid_members

    @property
    def blocked_members(self):
        """Retourne les membres qui sont bloqués à cause de paiement en retard de plus de 2 jours."""
        blocked = []
        for member in self.unpaid_members:
            if member['days_overdue'] > 2:
                blocked.append(member['user'])
        return blocked

    @property
    def paid_members(self):
        """Retourne la liste des membres ayant payé et combien ils ont payé."""
        paid_members = []
        for member in self.members.all():
            payments = Payment.objects.filter(tontine=self, recipient=member, is_paid=True)
            total_paid = sum(payment.amount for payment in payments)
            if total_paid > 0:
                paid_members.append({
                    "user": member,
                    "total_paid": total_paid
                })
        return paid_members

    @property
    def mois_actuel(self):
        today = localdate()
        return (today.year - self.create_at.year) * 12 + today.month - self.create_at.month + 1

    def all_members_paid_for_month(self):
        mois_actuel = self.mois_actuel
        for member in self.members.all():
            total_paid = Acquitement.objects.filter(
                tontine=self, user=member
            ).aggregate(total=Sum('amount'))['total'] or 0
            montant_attendu = self.amount * mois_actuel
            if total_paid < montant_attendu:
                return False
        return True

    def is_eligible_to_receive(self, user):
        return self.all_members_paid_for_month() and user in self.members.all()

    @property
    def is_finished(self):
        if not self.is_full:
            return False
        return localdate() > self.end_date

    @property
    def period_end_date(self):
        if not self.is_full:
            return None
        today = localdate()
        if self.frequence == 'jour':
            return today
        elif self.frequence == 'semaine':
            start_week = today - timedelta(days=today.weekday())
            return start_week + timedelta(days=6)
        elif self.frequence == 'mois':
            last_day = calendar.monthrange(today.year, today.month)[1]
            return today.replace(day=last_day)
        return None

    @property
    def end_date(self):
        if not self.is_full:
            return None
        total_rounds = self.limite_member
        if self.frequence == 'jour':
            return self.create_at + timedelta(days=total_rounds - 1)
        elif self.frequence == 'semaine':
            return self.create_at + timedelta(weeks=total_rounds - 1)
        elif self.frequence == 'mois':
            month = self.create_at.month - 1 + total_rounds
            year = self.create_at.year + month // 12
            month = month % 12 + 1
            day = min(self.create_at.day, calendar.monthrange(year, month)[1])
            return date(year, month, day)
        return None

    @property
    def current_round(self):
        if not self.is_full:
            return 0
        today = localdate()
        if self.frequence == 'jour':
            delta = (today - self.create_at).days
        elif self.frequence == 'semaine':
            delta = (today - self.create_at).days // 7
        elif self.frequence == 'mois':
            delta = (today.year - self.create_at.year) * 12 + today.month - self.create_at.month
        else:
            delta = 0
        return delta + 1

    @property
    def next_recipient(self):
        current_round = self.current_round
        return self.members.order_by('id')[(current_round - 1) % self.members.count()]

    def amount_due(self, user):
        today = localdate()
        if self.frequence == 'jour':
            periods_due = (today - self.create_at).days + 1
        elif self.frequence == 'semaine':
            periods_due = (today - self.create_at).days // 7 + 1
        elif self.frequence == 'mois':
            periods_due = (today.year - self.create_at.year) * 12 + today.month - self.create_at.month + 1
        else:
            return 0
        paid_periods = Acquitement.objects.filter(tontine=self, user=user).count()
        missed_periods = periods_due - paid_periods
        return missed_periods * self.amount if missed_periods >= 2 else (self.amount if missed_periods > 0 else 0)

    @property
    def members_due_amounts(self):
        dues = {}
        today = localdate()
        created_at_date = self.create_at.date() if isinstance(self.create_at, datetime) else self.create_at
        if self.frequence == 'jour':
            periods_due = (today - created_at_date).days + 1
        elif self.frequence == 'semaine':
            periods_due = (today - created_at_date).days // 7 + 1
        elif self.frequence == 'mois':
            periods_due = (today.year - created_at_date.year) * 12 + today.month - created_at_date.month + 1
        else:
            return {}
        total_due_per_member = periods_due * self.amount
        payments = self.acquitement.values('user').annotate(total_paid=Sum('amount'))
        payments_dict = {p['user']: p['total_paid'] or 0 for p in payments}
        for member in self.members.all():
            total_paid = payments_dict.get(member.id, 0)
            dues[member] = max(total_due_per_member - total_paid, 0)
        return dues
    

    @property
    def payers(self):
        """Retourne la liste des membres ayant payé."""
        return self.members.filter(acquitement__tontine=self).distinct()

    @property
    def non_payers(self):
        """Retourne la liste des membres n'ayant pas encore payé."""
        return self.members.exclude(id__in=self.payers.values_list('id', flat=True))

    @property
    def non_payers_count(self):
        """Retourne le nombre de membres qui n'ont pas encore payé."""
        return self.non_payers.count()

    @property
    def payers_count(self):
        """Retourne le nombre de membres ayant payé."""
        return self.payers.count()

    def non_payers_amounts(self):
        return {user: self.amount_due(user) for user in self.non_payers}

    def non_payers_count(self):
        return self.non_payers.count()

    def finished_tontines_count(self):
        return self.member_tontines_collective.filter(tontinecollective__is_finished=True).count()

    def unfinished_tontines_count(self):
        return self.member_tontines_collective.filter(tontinecollective__is_finished=False).count()

    def total_tontines_count(self):
        return self.member_tontines_collective.count()

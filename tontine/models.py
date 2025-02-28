import calendar
import uuid
from datetime import date
from datetime import datetime
from random import randint

from django.db import models
from django.db.models import Count
from django.db.models import Exists
from django.db.models import OuterRef
from django.db.models import Sum
from django.utils import timezone
from django.utils.timezone import localdate
from django.utils.timezone import timedelta

from payement.models import Acquitement
from payement.models import Payment

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
    frequence = models.CharField(
        choices=FREQUENCY_CHOICES, default='jour', max_length=12)
    order_paiemement = models.IntegerField(
        choices=PAYMENT_ORDER_CHOICES, default=1)
    create_at = models.DateField(auto_now_add=True)
    start_at = models.DateField(null=True, blank=True)
    admin = models.ForeignKey(
        'account.User', on_delete=models.PROTECT, related_name='admin_tontine_collective')
    members = models.ManyToManyField(
        'account.User', related_name='member_tontines_collective')
    qr_code = models.ImageField(
        upload_to='tontine_qrcode/', blank=True, null=True)
    periode_amount = models.IntegerField(default=0)
    recipient_tontine_id = models.IntegerField(default=0)
    periode_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def total_members(self):
        return self.members.count()

    def total_revenu(self):
        return self.total_members * self.amount * 30

    @property
    def is_full(self):
        return self.members.count() >= self.limite_member

    def is_finish(self):
        recept_paiement = Payment.objects.filter(tontine=self).count()
        if self.total_members == recept_paiement:
            return True
        else:
            return False

    def start_tontine(self):
        if self.is_full:
            self.start_at = timezone.now()

    def end_date_tontine(self):
        if self.start_at:
            return self.start_at + timedelta(days=29 * self.total_members)
        else:
            return None

    @property
    def objectif(self):
        return self.total_members * self.amount

    def recipient(self):
        if self.order_paiemement == 1:
            members = list(self.members.all())
            random = randint(0, len(members) - 1)
            while Payment.objects.filter(recipient=members[random], tontine=self).exists():
                random = randint(0, len(members) - 1)
            self.recipient_tontine_id = int(members[random].pk)
        else:
            members = list(self.members.all().order_by('id'))
            for member in members:
                if not Payment.objects.filter(recipient=member, tontine=self).exists():
                    self.recipient_tontine_id = member.pk
                    break

    @property
    def unpaid_members(self):
        if self.start_at:
            unpaid_members = []
            today = timezone.now().date()
            for member in self.members.all():
                last_payment = Acquitement.objects.filter(
                    tontine=self, user=member, date__date=today).select_related('user')
                if not last_payment:
                    days_overdue = (timezone.now().date(
                    ) - (last_payment.date if last_payment else self.start_at)).days
                    unpaid_members.append({
                        "user": member,
                        "amount_due": self.amount * days_overdue,
                        "days_overdue": days_overdue,
                    })
            return unpaid_members
        else:
            return None

    @property
    def unpaid_members_count(self):
        return len(self.unpaid_members) if self.unpaid_members else 0

    @property
    def blocked_members(self):
        blocked = []
        for member in self.unpaid_members:
            if member['days_overdue'] >= 1:
                blocked.append(member)
        return blocked

    @property
    def paid_members(self):
        if self.start_at:
            paid_members = []
            for member in self.members.all():
                payments = Acquitement.objects.filter(
                    tontine=self, user=member)
                total_paid = sum(payment.amount for payment in payments)
                if total_paid > 0:
                    paid_members.append({
                        "user": member,
                        "total_paid": total_paid
                    })
            return paid_members
        else:
            return None

    @property
    def paid_members_count(self):
        return len(self.paid_members) if self.paid_members else 0


class Blocked_user(models.Model):
    tontine = models.ForeignKey(TontineCollective, on_delete=models.CASCADE)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    amount_due = models.IntegerField(default=0)
    days_overdue = models.IntegerField(default=0)

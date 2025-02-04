import uuid
import calendar
from django.db import models
from django.db.models import Count
from django.utils.timezone import localdate, timedelta
from datetime import date, timedelta

FREQUENCY_CHOICES = [
    ('jour', 'Chaque jour'),
    ('semaine', 'Chaque semaine'),
    ('mois', 'Une fois par mois'),
]

PAYMENT_ORDER_CHOICES = [
    (1, 'Aléatoire'),
    (2, 'Par ordre d\'adhésion'),
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
    admin = models.ForeignKey('account.User', on_delete=models.PROTECT, related_name='admin_tontine_collective')
    members = models.ManyToManyField('account.User', related_name='member_tontines_collective')
    qr_code = models.ImageField(upload_to='tontine_qrcode/', blank=True, null=True)

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
        if self.is_full:
            self.create_at = localdate()  # Réinitialiser la date de création à la date de début réelle
            self.save()
            # Logique pour démarrer la tontine, ex : initialiser le premier paiement
        else:
            raise ValueError("La tontine ne peut pas commencer car tous les membres ne sont pas encore inscrits.")

    @property
    def is_finished(self):
        if not self.is_full:
            return False
        return localdate() > self.end_date
    

    @property
    def period_end_date(self):
        if not self.is_full:
            return None  # Retourne None si la tontine n'a pas encore commencé
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
            return None  # La tontine n'a pas encore commencé
        total_rounds = self.limite_member  # Chaque membre reçoit une fois
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
            return 0  # Retourne 0 si la tontine n'a pas encore commencé
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
        all_members = list(self.members.all().order_by('id'))  # Ordre d'adhésion
        index = (current_round - 1) % len(all_members)
        return all_members[index]

    @property
    def payers(self):
        today = localdate()
        if self.frequence == 'jour':
            paid_members = self.members.filter(acquitement__date__date=today)
        elif self.frequence == 'semaine':
            start_week = today - timedelta(days=today.weekday())
            end_week = start_week + timedelta(days=6)
            paid_members = self.members.filter(acquitement__date__range=(start_week, end_week))
        elif self.frequence == 'mois':
            start_of_month = today.replace(day=1)
            last_day_of_month = calendar.monthrange(today.year, today.month)[1]
            end_of_month = today.replace(day=last_day_of_month)
            paid_members = self.members.filter(acquitement__date__range=(start_of_month, end_of_month))
        else:
            paid_members = self.members.none()
        return paid_members
    
    @property
    def payers_count(self):
        return self.payers.count()

    @property
    def non_payers(self):
        paid_members = self.payers
        non_payers = self.members.exclude(id__in=paid_members)
        return non_payers
    

    def amount_due(self, user):
        return self.amount if user in self.non_payers else 0

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


class TontineIndividuelle(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    amount = models.BigIntegerField()
    create_at = models.DateField(auto_now_add=True)
    admin = models.ForeignKey('account.User', on_delete=models.PROTECT, related_name='admin_tontine_individuelle')
    members = models.ForeignKey("account.User", verbose_name="", related_name='memeber_tontine_individuelle' , on_delete=models.CASCADE)

    def __str__(self):
        return self.name

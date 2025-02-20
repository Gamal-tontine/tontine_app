from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Définir le module de paramètres Django par défaut pour le programme 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Utiliser une chaîne de caractères ici signifie que le worker n'a pas besoin de sérialiser
# l'objet de configuration pour les processus enfants.
# - namespace='CELERY' signifie que toutes les clés de configuration liées à celery
#   doivent avoir un préfixe `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger les modules de tâches de toutes les applications Django enregistrées.
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Configurer le planning des tâches périodiques
app.conf.beat_schedule = {
    # Tâche qui s'exécute toutes les 24 heures
    'task-every-24-hours': {
        'task': 'tontine.tasks.reminder_paiement_for_day',
        'schedule': crontab(hour=7, minute=0),  
    },
    # Tâche qui s'exécute chaque semaine
    'task-every-week': {
        'task': 'myapp.tasks.reminder_paiement_for_week',
        'schedule': crontab(hour=0, minute=0, day_of_week=0),  
    },
    # Tâche qui s'exécute chaque mois
    'task-every-month': {
        'task': 'myapp.tasks.reminder_paiement_for_month',
        'schedule': crontab(hour=0, minute=0, day_of_month=1),  
    },
    # tache qui s'execute chaque jour 17
    # "tache-a-17h": {
    #     "task": "tontine.tasks.reminder_paiement_for_day",  # Remplace par le nom de ta tâche
    #     "schedule": crontab(hour=17, minute=0),  # Exécution tous les jours à 17h
    # },
}


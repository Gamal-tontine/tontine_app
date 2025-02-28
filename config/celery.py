import os

from celery import Celery
from celery.schedules import crontab  # Assure-toi que cette ligne est présente

# Définir la variable d'environnement Django si elle n'est pas déjà définie
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialiser Celery
app = Celery('config')

# Charger les paramètres Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger automatiquement les tâches des applications Django
app.autodiscover_tasks()

# Planification des tâches périodiques
app.conf.beat_schedule = {
    'task-every-24-hours': {
        'task': 'tontine.tasks.reminder_paiement_for_day',
        'schedule': crontab(hour=7, minute=0),
    },
    'task-every-week': {
        'task': 'tontine.tasks.reminder_paiement_for_week',
        'schedule': crontab(hour=0, minute=0, day_of_week=0),
    },
    'task-every-month': {
        'task': 'tontine.tasks.reminder_paiement_for_month',
        'schedule': crontab(hour=0, minute=0, day_of_month=1),
    },
    'task-at-17h': {
        'task': 'tontine.tasks.reminder_paiement_for_day',
        'schedule': crontab(hour=17, minute=0),
    },
    'block-defaulting-members': {
        'task': 'tontine.tasks.bloked_worker',
        'schedule': crontab(hour=23, minute=50),
    },
}

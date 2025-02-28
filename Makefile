.PHONY: celery_beat
celery_beat:
    celery -A config beat --loglevel=info

.PHONY: celery_run
celery_run:
	celery -A config worker --loglevel=info --pool=solo

.PHONY: remember
remember:
    celery -A config call tontine.tasks.reminder_paiement_for_day

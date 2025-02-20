.PHONY: celery_run
celery_run:
    celery -A config worker --loglevel=info
    celery -A config beat --loglevel=info

.PHONY: celery
celery:
	celery -A config worker --loglevel=info --pool=solo
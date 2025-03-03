
```markdown
# Guide de Configuration et de Lancement du Projet

## Cloner le projet :
```bash
git clone <url_repot>
cd tontine_app
git checkout new-versions-1
```

## Ouvrir le code dans un éditeur :
- Utilisez l'éditeur de code de votre choix (par exemple, VS Code, PyCharm).

## Créer et activer votre environnement virtuel :
```bash
python -m venv env
source env/bin/activate  # Pour Linux/MacOS
.\env\Scripts\activate  # Pour Windows
```

## Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Effectuer les migrations de base de données :
```bash
python manage.py migrate
```

## Lancer le serveur de développement :
```bash
python manage.py runserver
```

## Lancer les workers Celery pour exécuter les tâches asynchrones :

1. **Ouvrir Docker Desktop :**
   - Téléchargez et installez Docker Desktop depuis [ici](https://www.docker.com/products/docker-desktop).
   - Assurez-vous que Docker Desktop est en cours d'exécution.

2. **Lancer RabbitMQ (le message broker) :**
```bash
cd config
docker-compose up -d
```

## Lancer Celery et Celery Beat :

1. **Lancer Celery :**
```bash
celery -A config worker --pool=solo --loglevel=info
```

2. **Lancer Celery Beat :**
```bash
celery -A config beat --loglevel=info
```

Vous êtes maintenant prêt à utiliser l'application.
```





services:
  - type: web
    name: jornadamaternal
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn jornadam_maternal.wsgi:application
    preDeployCommand: python manage.py migrate

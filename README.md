## Создание суперпользователя

Для создания административного аккаунта выполните:

```
python manage.py csu
```
## Запуск задач Celery

Для корректной работы рассылки необходимо запустить Celery worker и beat:

```
celery -A config worker -l INFO
celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
import os
from celery import Celery

# 1. Указываем файл настроек Django по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 2. Создаем экземпляр Celery
app = Celery('core')

# 3. Загружаем конфигурацию из settings.py с префиксом 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4. Автоматически находим файлы tasks.py во всех установленных приложениях (apps)
app.autodiscover_tasks()

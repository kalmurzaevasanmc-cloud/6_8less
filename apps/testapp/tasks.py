import time
import logging 
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__) 

# 💥 ПРИМЕР 1: Фоновая задача (Worker)
# Реальный кейс: При регистрации отправляем приветственное письмо.
# Запрос к почтовому серверу занимает 2-4 секунды. Если делать синхронно — фронт зависнет.
@shared_task
def send_welcome_email_task(user_email: str):
    """Отправка приветственного письма в фоновом режиме."""
    # Имитируем задержку сети
    time.sleep(5) 
    
    # Реальная отправка (требует настроек EMAIL_HOST в settings.py)
    # send_mail(
    #     subject="Добро пожаловать!",
    #     message="Спасибо за регистрацию на нашей платформе!",
    #     from_email="noreply@myproject.com",
    #     recipient_list=[user_email],
    # )
    
    print(f"[Celery Worker] Успешно отправлено письмо для {user_email}")
    return f"Email sent to {user_email}"


# ⏰ ПРИМЕР 2: Периодическая задача (Beat)
# Реальный кейс: Каждую ночь очищать inactive/unverified пользователей или собирать статистику.
@shared_task
def monthly_user_stats_task():
    """Считает общее количество пользователей и выводит статистику."""
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    
    report = f"[Celery Beat Report] Всего юзеров: {total_users}, Активных: {active_users}"
    print(report)
    return report

@shared_task
def clear_expired_cache_task():
    """Периодическая задача для имитации очистки устаревших элементов."""
    message = "Beat Task: Cleaning expired items..."
    
    # Вывод в консоль (STDOUT)
    print(message)
    
    # Логирование через стандартный модуль logging
    logger.info(message)
    
    return message 
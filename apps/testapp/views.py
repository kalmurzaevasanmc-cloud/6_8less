from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from apps.testapp.models import CustomUser 
from apps.testapp.tasks import send_welcome_email_task
from django.core.cache import cache 

class DemoCacheView(APIView):
    """Пример использования Redis для кэширования ответов."""
    def get(self, request):
        cached_data = cache.get("demo_timestamp")
        if cached_data:
            return Response({"data": cached_data, "source": "Redis Cache"})
        
        import datetime
        new_data = f"Создано в {datetime.datetime.now().isoformat()}"
        cache.set("demo_timestamp", new_data, timeout=30)
        return Response({"data": new_data, "source": "Database / Calculations"})

class TriggerAsyncTaskView(APIView):
    """Запуск фоновой асинхронной задачи через Celery."""
    def post(self, request):
        data_id = request.data.get("id", 1)
        task = process_heavy_task.delay(data_id)
        return Response({
            "message": "Задача успешно отправлена в Celery Worker",
            "task_id": task.id
        }, status=status.HTTP_202_ACCEPTED)

class StatsView(APIView):
    def get(self, request):
        cache_key = 'stats_data'
        
        # 1. Пытаемся получить данные из Redis
        cached_stats = cache.get(cache_key)
        
        if cached_stats is not None:
            # Возвращаем данные из кэша
            return Response(cached_stats)
        
        # 2. Если в кэше пусто — формируем тяжелую статистику
        stats_data = {
            "users_count": 1000,
            "active_orders": 42
        }
        
        # 3. Сохраняем в Redis на 60 секунд (TTL = 60)
        cache.set(cache_key, stats_data, timeout=60)
        
        return Response(stats_data) 
  
# 🧠 А ВОТ ПРИМЕР С REDIS KЭШЕМ (Кэширование списка юзеров для Админа)
class AdminUsersListView(APIView):
    """Пример ручки с простым и понятным кэшированием через Redis."""
    
    def get(self, request):
        cache_key = "all_users_list"
        
        # 1. Проверяем, есть ли готовый список в Redis
        cached_data = cache.get(cache_key)
        if cached_data:
            print("--- ОТДАЕМ ДАННЫЕ ИЗ REDIS КЭША ---")
            return Response(cached_data)

        # 2. Если в Redis пусто — запрашиваем из базы PostgreSQL
        print("--- ДЕЛАЕМ ЗАПРОС К БАЗЕ ДАННЫХ PostgreSQL ---")
        users = User.objects.all().values("id", "email", "role", "is_active")
        data = list(users)

        # 3. Кладем результат в Redis на 60 секунд
        cache.set(cache_key, data, timeout=60)

        return Response(data)

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get("email")
        
        if not email:
            return Response(
                {"error": "Поле email обязательно"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Запуск задачи в фоновом режиме (асинхронно)
        task = send_welcome_email_task.delay(email)
        
        # Возвращаем 201 Created немедленно
        return Response(
            {
                "message": "Пользователь зарегистрирован. Приветственное письмо обрабатывается.",
                "task_id": task.id
            },
            status=status.HTTP_201_CREATED
        )
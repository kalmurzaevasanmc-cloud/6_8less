from django.urls import path
from .views import DemoCacheView, TriggerAsyncTaskView, StatsView, RegisterView 

urlpatterns = [
    path('cache-demo/', DemoCacheView.as_view(), name='cache-demo'),
    path('trigger-task/', TriggerAsyncTaskView.as_view(), name='trigger-task'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('v1/register/', RegisterView.as_view(), name='register-v1'), 
]
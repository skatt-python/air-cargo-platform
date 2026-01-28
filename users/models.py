from django.db import models
from django.contrib.auth.models import User

# ВРЕМЕННАЯ УПРОЩЕННАЯ МОДЕЛЬ ДЛЯ ЗАПУСКА
class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('customer', 'Грузовладелец'),
        ('agent', 'Агент перевозок'),
        ('developer', 'Разработчик'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    company_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.email})"

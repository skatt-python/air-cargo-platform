from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    # Временный простой тест
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>AirCargo - Главная</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h1>🏠 ГЛАВНАЯ СТРАНИЦА</h1>
        <p>Это простая главная страница для теста</p>
        <h2>Тестовые ссылки:</h2>
        <ul>
            <li><a href="/register/">Регистрация (простая)</a></li>
            <li><a href="/login/">Вход (простая)</a></li>
            <li><a href="/shipments/">Грузы (простая)</a></li>
            <li><a href="/admin/">Админка</a></li>
        </ul>
    </body>
    </html>
    """)
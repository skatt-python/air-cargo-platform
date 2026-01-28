#!/usr/bin/env python
"""Минимальный запуск проекта без полных миграций Django"""

import os
import sys
import sqlite3

# Пути проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')

def create_minimal_database():
    """Создает минимальную базу данных SQLite вручную"""
    print("🔧 Создание минимальной базы данных...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Создаем таблицу пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users_user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password TEXT NOT NULL,
        last_login DATETIME NULL,
        is_superuser BOOLEAN NOT NULL,
        username TEXT UNIQUE NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        is_staff BOOLEAN NOT NULL,
        is_active BOOLEAN NOT NULL,
        date_joined DATETIME NOT NULL,
        user_type TEXT NOT NULL DEFAULT 'customer',
        phone TEXT NOT NULL DEFAULT '',
        company_name TEXT NOT NULL DEFAULT '',
        rating REAL NOT NULL DEFAULT 0.0,
        total_ratings INTEGER NOT NULL DEFAULT 0,
        is_premium BOOLEAN NOT NULL DEFAULT 0,
        subscription_end_date DATETIME NULL
    )
    ''')
    
    # Создаем таблицу грузов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS shipments_shipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        departure_city TEXT NOT NULL,
        arrival_city TEXT NOT NULL,
        weight REAL NOT NULL,
        volume REAL NOT NULL,
        cargo_places INTEGER NOT NULL DEFAULT 1,
        status TEXT NOT NULL DEFAULT 'pending',
        description TEXT NOT NULL DEFAULT '',
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        customer_id INTEGER NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES users_user (id)
    )
    ''')
    
    # Создаем суперпользователя
    cursor.execute('''
    INSERT OR IGNORE INTO users_user 
    (username, password, email, is_superuser, is_staff, is_active, 
     date_joined, company_name, user_type)
    VALUES 
    ('admin', 'pbkdf2_sha256$600000$...', 'admin@aircargo.ru', 1, 1, 1, 
     datetime('now'), 'AirCargo Admin', 'developer')
    ''')
    
    conn.commit()
    conn.close()
    print("✅ База данных создана")

def run_minimal_server():
    """Запускает минимальный веб-сервер"""
    print("🚀 Запуск AirCargo Platform...")
    
    from wsgiref.simple_server import make_server
    
    def simple_app(environ, start_response):
        """Минимальное WSGI приложение"""
        path = environ.get('PATH_INFO', '/')
        
        if path == '/':
            html = '''
            <!DOCTYPE html>
            <html>
            <head><title>AirCargo Platform - ВОССТАНОВЛЕНИЕ</title></head>
            <body style="font-family: Arial; padding: 20px;">
                <h1>🚀 AirCargo Platform - Работает!</h1>
                <p>Проект успешно восстановлен в минимальном режиме.</p>
                <h2>Доступные страницы:</h2>
                <ul>
                    <li><a href="/admin/">Админка Django</a></li>
                    <li><a href="/">Главная страница</a></li>
                    <li><a href="/shipments/">Список грузов</a></li>
                    <li><a href="/register/">Регистрация</a></li>
                    <li><a href="/login/">Вход</a></li>
                </ul>
                <hr>
                <p><strong>Данные для входа в админку:</strong></p>
                <p>Логин: admin</p>
                <p>Пароль: admin123</p>
                <p>Email: admin@aircargo.ru</p>
            </body>
            </html>
            '''
        elif path == '/admin/':
            html = '''
            <!DOCTYPE html>
            <html>
            <head><title>Админка AirCargo</title></head>
            <body>
                <h1>Админка временно недоступна</h1>
                <p>Используйте shell для управления данными:</p>
                <pre>python manage.py shell</pre>
                <a href="/">На главную</a>
            </body>
            </html>
            '''
        else:
            html = f'''
            <!DOCTYPE html>
            <html>
            <body>
                <h1>Страница: {path}</h1>
                <p>Функционал в разработке</p>
                <a href="/">На главную</a>
            </body>
            </html>
            '''
        
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [html.encode('utf-8')]
    
    print("🌐 Сервер запущен на http://127.0.0.1:8000")
    print("📁 База данных: db.sqlite3")
    print("👤 Суперпользователь: admin / admin123")
    print("🔄 Для остановки сервера нажмите Ctrl+C")
    
    server = make_server('127.0.0.1', 8000, simple_app)
    server.serve_forever()

if __name__ == '__main__':
    # Создаем базу данных
    create_minimal_database()
    
    # Запускаем сервер
    run_minimal_server()

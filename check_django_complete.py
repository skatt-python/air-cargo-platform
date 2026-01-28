import os
import sys
import django

print("=== Полная проверка установки Django ===")

# Основной путь Django
django_path = django.__path__[0]
print(f"Django путь: {django_path}")

# Критические файлы для проверки
critical_files = [
    # migrations
    ('db/migrations/__init__.py', 'Основной модуль миграций'),
    ('db/migrations/migration.py', 'Класс Migration'),
    ('db/migrations/utils/__init__.py', 'Утилиты миграций'),
    ('db/migrations/utils/utils.py', 'Функции утилит'),
    ('db/migrations/operations/__init__.py', 'Операции миграций'),
    ('db/migrations/operations/base.py', 'Базовые операции'),
    ('db/migrations/operations/fields.py', 'Операции с полями'),
    ('db/migrations/operations/models.py', 'Операции с моделями'),
    ('db/migrations/operations/special.py', 'Специальные операции (RunPython)'),
    
    # core
    ('core/__init__.py', 'Ядро Django'),
    ('core/management/__init__.py', 'Управление'),
    
    # contrib
    ('contrib/auth/__init__.py', 'Аутентификация'),
    ('contrib/contenttypes/__init__.py', 'Типы контента'),
]

print("\nПроверка критических файлов:")
print("-" * 80)

all_ok = True
for rel_path, description in critical_files:
    full_path = os.path.join(django_path, rel_path)
    exists = os.path.exists(full_path)
    status = "✓" if exists else "✗"
    print(f"{status} {description:30} {rel_path}")
    if not exists:
        all_ok = False

print("-" * 80)

# Проверка импортов
print("\nПроверка критических импортов:")
try:
    from django.db.migrations import RunPython, RunSQL
    print("✓ RunPython и RunSQL импортируются")
except ImportError as e:
    print(f"✗ Ошибка импорта: {e}")

try:
    from django.db.migrations.operations import *
    print("✓ Все операции миграций импортируются")
except ImportError as e:
    print(f"✗ Ошибка импорта операций: {e}")

try:
    from django.core.management import execute_from_command_line
    print("✓ Модуль управления импортируется")
except ImportError as e:
    print(f"✗ Ошибка импорта управления: {e}")

if all_ok:
    print("\n✅ Все критически важные файлы Django на месте!")
else:
    print("\n❌ Отсутствуют некоторые файлы Django!")

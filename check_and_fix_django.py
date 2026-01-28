#!/usr/bin/env python
import os
import sys
import subprocess
import shutil

def check_django_files():
    """Проверить все необходимые файлы Django"""
    try:
        import django
    except ImportError:
        print("✗ Django не установлен!")
        return False
    
    django_path = django.__path__[0]
    migrations_path = os.path.join(django_path, 'db', 'migrations')
    
    required_files = {
        'migrations/migration.py': os.path.join(migrations_path, 'migration.py'),
        'migrations/__init__.py': os.path.join(migrations_path, '__init__.py'),
        'migrations/utils/__init__.py': os.path.join(migrations_path, 'utils', '__init__.py'),
        'migrations/utils/utils.py': os.path.join(migrations_path, 'utils', 'utils.py'),
        'migrations/operations/__init__.py': os.path.join(migrations_path, 'operations', '__init__.py'),
        'migrations/operations/base.py': os.path.join(migrations_path, 'operations', 'base.py'),
    }
    
    print("Проверка файлов Django:")
    print("-" * 60)
    
    missing_files = []
    for name, path in required_files.items():
        if os.path.exists(path):
            print(f"✓ {name}")
        else:
            print(f"✗ {name}")
            missing_files.append((name, path))
    
    print("-" * 60)
    
    if missing_files:
        print(f"Найдено {len(missing_files)} отсутствующих файлов")
        return False
    else:
        print("Все файлы на месте!")
        return True

def reinstall_django():
    """Полная переустановка Django"""
    print("\nПереустановка Django...")
    
    # 1. Удаляем старый Django
    print("1. Удаляем старый Django...")
    subprocess.run([sys.executable, '-m', 'pip', 'uninstall', 'django', '-y'], 
                   capture_output=True)
    
    # 2. Очищаем кэш pip
    print("2. Очищаем кэш pip...")
    subprocess.run([sys.executable, '-m', 'pip', 'cache', 'purge'], 
                   capture_output=True)
    
    # 3. Устанавливаем заново
    print("3. Устанавливаем Django 4.2.7...")
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', 'django==4.2.7', '--no-cache-dir'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Ошибка при установке: {result.stderr}")
        return False
    
    print("4. Проверяем установку...")
    return check_django_files()

def main():
    print("=== Проверка и восстановление Django ===")
    
    if not check_django_files():
        print("\nОбнаружены проблемы с установкой Django!")
        response = input("Выполнить полную переустановку? (y/n): ")
        if response.lower() == 'y':
            if reinstall_django():
                print("\n✓ Django успешно переустановлен!")
            else:
                print("\n✗ Не удалось переустановить Django")
                print("\nРекомендации:")
                print("1. Попробуйте другую версию Python")
                print("2. Используйте: pip install django==4.1.13")
                print("3. Скачайте Django с GitHub: https://github.com/django/django")
        else:
            print("\nПродолжайте с текущей установкой")
    else:
        print("\n✓ Установка Django в порядке!")

if __name__ == "__main__":
    main()

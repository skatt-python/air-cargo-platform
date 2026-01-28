import os
import django
from django.conf import settings

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.template.loader import get_template

templates_to_check = [
    'users/register.html',
    'users/login.html',
    'shipments/list.html',
    'shipments/create.html',
]

print("🔍 ПРОВЕРКА ШАБЛОНОВ:")
print("=" * 50)

for template_name in templates_to_check:
    try:
        template = get_template(template_name)
        print(f"✅ {template_name}: НАЙДЕН")
        print(f"   Путь: {template.origin.name}")
        print(f"   Размер: {os.path.getsize(template.origin.name)} байт")
        print(f"   Время изменения: {os.path.getmtime(template.origin.name)}")
    except Exception as e:
        print(f"❌ {template_name}: ОШИБКА - {e}")
    
    print("-" * 50)


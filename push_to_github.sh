#!/bin/bash
echo "=== Загрузка AirCargo Platform на GitHub ==="

# Переходим в папку проекта
cd /Users/vladudin/Documents/air_cargo_final
echo "Текущая директория: $(pwd)"

# Удаляем старый .git если есть
if [ -d ".git" ]; then
    echo "Удаляем старый .git..."
    rm -rf .git
fi

# Инициализируем git
echo "Инициализируем Git..."
git init

# Создаем .gitignore
echo "Создаем .gitignore..."
cat > .gitignore << 'GITIGNORE'
# Django
*.log
*.pot
*.pyc
__pycache__/
local_settings.py
db.sqlite3
media/
staticfiles/

# Virtual Environment
.venv/
venv/
env/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Python
*.pyc
*.pyo
*.pyd
.Python

# Backup files
*.bak
*.backup

# Large files
*.zip
*.tar.gz
*.rar
GITIGNORE

# Создаем requirements.txt если нет
if [ ! -f "requirements.txt" ]; then
    echo "Создаем requirements.txt..."
    echo "Django==4.2.7" > requirements.txt
    echo "Pillow==10.0.0" >> requirements.txt
fi

# Добавляем файлы
echo "Добавляем файлы в Git..."
git add .

# Коммит
echo "Создаем коммит..."
git commit -m "Initial commit: AirCargo Platform with bids system"

# Подключаем к GitHub
echo "Подключаем к GitHub..."
git remote add origin https://github.com/skatt-python/air-cargo-platform.git

# Пушим
echo "Загружаем на GitHub..."
git branch -M main

# Пробуем обычный push, если не получится - force push
if git push -u origin main 2>/dev/null; then
    echo "Успешно загружено!"
else
    echo "Делаем force push..."
    git push -u origin main --force
fi

echo "=== Готово! ==="
echo "Ссылка: https://github.com/skatt-python/air-cargo-platform"

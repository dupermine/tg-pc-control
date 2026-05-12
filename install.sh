#!/bin/bash
echo "🚀 Установка tg-pc-control (Arch Linux)"

# Системные пакеты
sudo pacman -S --needed python python-pip xclip wl-clipboard

# Python зависимости
pip install -r requirements.txt --break-system-packages

# Создание .env
if [ ! -f .env ]; then
    echo "📝 Создаём .env файл..."
    cat > .env << EOF
TOKEN=ТОКЕН_БОТА_СЮДА
ALLOWED_USER_ID=123456789
USE_WAYLAND=False
EOF
    echo "✅ .env создан → ОБЯЗАТЕЛЬНО отредактируй его!"
fi

# Автозапуск
mkdir -p ~/.config/systemd/user
cp service/tg-pc-bot.service ~/.config/systemd/user/

systemctl --user daemon-reload
systemctl --user enable --now tg-pc-bot.service

echo ""
echo "========================================"
echo "✅ Установка завершена!"
echo "========================================"
echo "Отредактируй .env и готово."

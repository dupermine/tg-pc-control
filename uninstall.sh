#!/bin/bash
echo "🗑 Удаление tg-pc-control"

systemctl --user stop tg-pc-bot.service 2>/dev/null
systemctl --user disable tg-pc-bot.service 2>/dev/null
rm -f ~/.config/systemd/user/tg-pc-bot.service
systemctl --user daemon-reload

echo "✅ Сервис удалён."

# Происхождение

Подготовлено 23.10.2026 из локального опыта настройки persistent terminals.
Из исходного окружения изучены документы:

- `ANTIGRAVITY_PERSISTENT_TERMINALS.md` — reconnect, orphan sessions, grouped
  tabs, OSC spam, clean input, bracketed paste, truecolor;
- `ANTIGRAVITY_CLAUDE_RIGHTCLICK_PASTE_FIX_20260706.md` — tmux pane menu и
  позднейший owner-selected профиль клиентского меню;
- `check_persistent_terminals.sh` и `antigravity-terminal-stability/SKILL.md` —
  безопасные проверки и история расхождений слоёв терминального стека.

Серверные файлы не скопированы целиком: они содержат специфичные пути,
интеграции и исторические настройки CLI. Код wrapper/installer/smoke написан
заново для этого комплекта. Нет ключей, учётных данных, сетевой топологии,
shell history, конфигов AI-провайдеров или Telegram-интеграций.

Для воспроизводимости выбран простой explicit named-session workflow вместо
эвристического автоматического выбора detached-сессии по IDE nonce/размеру.

Первичные источники:

- [tmux README](https://github.com/tmux/tmux/blob/master/README)
- [tmux manual](https://github.com/tmux/tmux/blob/master/tmux.1)
- [tmux wiki](https://github.com/tmux/tmux/wiki)

Проверка 23.10.2026: локальный tmux 3.4; runtime smoke в отдельном socket.
Проверка физического reconnect конкретной IDE выполняется пользователем.

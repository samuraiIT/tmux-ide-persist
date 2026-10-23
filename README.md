# tmux IDE Persist

Терминал и запущенные в нём CLI продолжают работать на Linux-сервере после
закрытия IDE, обрыва SSH или отключения ноутбука. При возвращении подключитесь
к той же именованной сессии. Основа — [tmux](https://github.com/tmux/tmux).

Работает с SSH-терминалами VS Code, Cursor, Antigravity и обычным SSH.
На Windows tmux запускается **на удалённом Linux**, либо внутри WSL.
Перезагрузку сервера tmux не переживает. Долгоживущие службы запускайте через
systemd; tmux предназначен для интерактивной работы.

## Установка на Linux-сервере

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install tmux git
git clone https://github.com/samuraiIT/tmux-ide-persist.git
cd tmux-ide-persist
bash install.sh
~/.local/bin/ide-tmux attach work
```

Fedora: `sudo dnf install tmux git`. macOS: `brew install tmux git`.
Проверено автоматически на Linux с tmux 3.4; macOS/WSL и конкретные IDE требуют
ручной проверки. Installer создаёт только symlink в `~/.local/bin`, отказывается
перезаписывать чужой файл и не редактирует `.bashrc` или настройки IDE.
Каталог репозитория после установки оставьте на месте.

После появления tmux запустите ваш CLI обычной командой. Закройте IDE,
подключитесь снова и выполните:

```bash
~/.local/bin/ide-tmux attach work
```

Вы вернётесь к прежнему процессу. `Ctrl+b`, затем `d` — отсоединиться и оставить
процесс работать. `exit` завершает shell; это не способ безопасно отсоединиться.

## Подключение к IDE

В Remote SSH настройках Linux-терминала добавьте профиль вручную, указав своё
имя пользователя. Существующие настройки объедините, не заменяйте целиком:

```json
{
  "terminal.integrated.profiles.linux": {
    "Persistent tmux": {
      "path": "/home/YOUR_USER/.local/bin/ide-tmux",
      "args": ["attach", "work"]
    }
  },
  "terminal.integrated.defaultProfile.linux": "Persistent tmux",
  "terminal.integrated.persistentSessionReviveProcess": "never",
  "terminal.integrated.scrollback": 50000,
  "terminal.integrated.rightClickBehavior": "default"
}
```

Затем `Developer: Reload Window`. Профиль использует явное имя `work`:
несколько вкладок с этим именем показывают одну сессию. Для независимых задач
используйте `ide-tmux attach coding`, `ide-tmux attach logs` и отдельные профили
IDE с соответствующими именами. Автоматически угадывать потерянную сессию по
размеру окна или IDE nonce намеренно не требуется.

`Ctrl+b c` — новое окно; `Ctrl+b n` / `p` — следующее / предыдущее;
`Ctrl+b [` — просмотр истории; `q` — выйти из просмотра.

## Восстановление и диагностика

```bash
~/.local/bin/ide-tmux list
~/.local/bin/ide-tmux attach work
```

Комплект использует отдельный socket `ide-persist`. Обычный `tmux ls` его не
покажет: используйте wrapper или `tmux -L ide-persist list-sessions`.
Имена сессий принимают только буквы, цифры, `_` и `-`.

Решения обнаруженных на исходном сервере багов:
[TROUBLESHOOTING_RU.md](docs/TROUBLESHOOTING_RU.md).
Происхождение и границы переноса: [PROVENANCE.md](docs/PROVENANCE.md).

## Проверка и удаление

```bash
python3 tests/smoke.py
```

Smoke создаёт собственный временный socket, проверяет настоящий attach/detach
и сохранение PID процесса. Пользовательские tmux-сессии не затрагиваются.
В IDE вручную проверьте отключение/возврат, вставку и прокрутку.

Чтобы отменить установку, удалите только symlink `~/.local/bin/ide-tmux`
после проверки `readlink ~/.local/bin/ide-tmux`. Настройки профиля IDE удалите
вручную. Уже запущенные сессии продолжат работать. Не выполняйте `kill-server`
или массовое закрытие окон для удаления программы.

Это переносимый комплект конфигурации и документации, а не копия tmux.
Исходный tmux устанавливается из пакетного менеджера вашей ОС.

#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
command -v tmux >/dev/null || { echo 'Install tmux first; see README.md.' >&2; exit 1; }
target_dir="${HOME}/.local/bin"
mkdir -p -- "$target_dir"
target="$target_dir/ide-tmux"
if [[ -e "$target" || -L "$target" ]]; then
  [[ -L "$target" && "$(readlink -- "$target")" == "$project_dir/bin/ide-tmux" ]] || {
    echo "Refusing to overwrite existing $target" >&2; exit 1;
  }
else
  ln -s -- "$project_dir/bin/ide-tmux" "$target"
fi
printf 'Installed: %s\nRun: %s attach work\nKeep this repository at: %s\n' "$target" "$target" "$project_dir"

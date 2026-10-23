#!/usr/bin/env python3
"""Exercise a disposable socket; never touches ordinary tmux sessions."""
import os
from pathlib import Path
import pty
import subprocess
import tempfile
import time

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='ide-tmux-test-') as temporary:
    base = ['tmux', '-S', str(Path(temporary) / 'socket'), '-f', str(root / 'config/tmux.conf')]
    def run(*args):
        return subprocess.check_output(base + list(args), text=True).strip()
    try:
        run('new-session', '-d', '-s', 'test', 'sleep 120')
        pane_pid = run('display-message', '-p', '-t', 'test', '#{pane_pid}')
        assert run('show-options', '-gv', 'destroy-unattached') == 'off'
        assert run('show-options', '-gv', 'mouse') == 'on'
        master, slave = pty.openpty()
        try:
            client = subprocess.Popen(base + ['attach-session', '-t', 'test'],
                                      stdin=slave, stdout=slave, stderr=slave,
                                      env={**os.environ, 'TERM': 'xterm-256color'})
            deadline = time.monotonic() + 5
            while run('display-message', '-p', '-t', 'test', '#{session_attached}') == '0':
                assert client.poll() is None, 'attach failed'
                assert time.monotonic() < deadline, 'attach timeout'
                time.sleep(.05)
            run('detach-client', '-s', 'test')
            assert client.wait(timeout=5) == 0
            assert run('display-message', '-p', '-t', 'test', '#{pane_pid}') == pane_pid
            os.kill(int(pane_pid), 0)
            run('has-session', '-t', 'test')
            assert 'run-shell -b true' in run('list-keys', '-T', 'root', 'MouseDown3Pane')
            print('PASS: attach/detach preserves process; mouse, persistence, right-click guard')
        finally:
            if 'client' in locals() and client.poll() is None:
                client.terminate()
                client.wait(timeout=5)
            os.close(master)
            os.close(slave)
    finally:
        subprocess.run(base + ['kill-server'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

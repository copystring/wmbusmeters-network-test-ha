#!/usr/bin/env python3
# Copyright (C) 2026 Felix Gohringer (gpl-3.0-or-later)
"""Persist timestamped receiver output while retaining Home Assistant logs."""

from datetime import datetime, timezone
import signal
import subprocess
import sys


def main():
    log_path, command = sys.argv[1], sys.argv[2:]
    with open(log_path, "a", encoding="utf-8", buffering=1) as log:
        child = subprocess.Popen(command, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, text=True,
                                 encoding="utf-8", errors="replace", bufsize=1)

        def forward_signal(number, _frame):
            if child.poll() is None:
                child.send_signal(number)

        signal.signal(signal.SIGTERM, forward_signal)
        signal.signal(signal.SIGINT, forward_signal)
        try:
            for line in child.stdout:
                timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
                entry = f"{timestamp} {line}"
                log.write(entry)
                print(entry, end="", flush=True)
            result = child.wait()
            return result if result >= 0 else 128 - result
        finally:
            child.stdout.close()
            if child.poll() is None:
                child.terminate()
                try:
                    child.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait()


if __name__ == "__main__":
    sys.exit(main())

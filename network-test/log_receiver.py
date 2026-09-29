#!/usr/bin/env python3
# Copyright (C) 2026 Felix Gohringer (gpl-3.0-or-later)
"""Persist timestamped receiver output while retaining Home Assistant logs."""

from datetime import datetime, timezone
import json
import signal
import subprocess
import sys


def readable_reading(line):
    try:
        reading = json.loads(line)
    except json.JSONDecodeError:
        return None
    if not isinstance(reading, dict) or reading.get("media") != "water":
        return None
    parts = [f"Wasserzähler {reading.get('id', '?')}"]
    volume = reading.get("total_m3")
    if isinstance(volume, (int, float)):
        parts.append(f"Zählerstand: {volume:g} m³ ({volume * 1000:g} Liter)")
    translations = {"OK": "OK", "DRY": "Trockenlauf / kein Wasser",
                    "REVERSE": "Rückwärtsfluss", "LEAK": "Leckage",
                    "BURST": "Rohrbruchalarm"}
    status = reading.get("status")
    if isinstance(status, str):
        parts.append("Status: " + ", ".join(
            translations.get(flag, flag) for flag in status.split()))
    return " | ".join(parts) + "\n"


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
                summary = readable_reading(line)
                if summary is not None:
                    entry = f"{timestamp} {summary}"
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

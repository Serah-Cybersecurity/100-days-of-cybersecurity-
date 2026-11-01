#!/usr/bin/env bash
# Day 10: Basic Linux triage snapshot
# Purpose: Read-only system inspection for a learning lab.
# Scope: Local machine only.
# Note: Output can contain private system information.
set -u

section() {
    printf '\n===== %s =====\n' "$1"
}

section "COLLECTION METADATA"

date -Is 2>/dev/null || date
uname -srmo
id

section "PROCESS SNAPSHOT"
if command -v ps >/dev/null 2>&1; then
    ps -eo pid,ppid,user,stat,etime,comm --sort=ppid | head -n 26
else
    printf 'The ps command is unavailable.\n'
fi

section "RUNNING SYSTEMD SERVICES"
if command -v systemctl >/dev/null 2>&1; then
    systemctl list-units \
        --type=service \
        --state=running \
        --no-pager 2>&1 | sed -n '1,30p'
else
    printf 'systemctl is unavailable in this environment.\n'
fi

section "LISTENING TCP SOCKETS"
if command -v ss >/dev/null 2>&1; then
    ss -lnt 2>&1
else
    printf 'The ss command is unavailable.\n'
fi

section "SYSTEMD TIMERS"
if command -v systemctl >/dev/null 2>&1; then
    systemctl list-timers \
        --all \
        --no-pager 2>&1 | sed -n '1,25p'
else
    printf 'systemctl is unavailable; timer inspection skipped.\n'
fi

section "CURRENT USER CRONTAB STATUS"
if command -v crontab >/dev/null 2>&1; then
    if crontab -l >/dev/null 2>&1; then
        printf 'A current-user crontab is present or readable.\n'
        printf 'Contents were intentionally not collected.\n'
    else
        printf 'No readable current-user crontab was detected.\n'
        printf 'It may be absent or access may be restricted.\n'
    fi
else
    printf 'The crontab command is unavailable.\n'
fi

section "SYSTEM-WIDE CRON FILE NAMES"
for dir in \
    /etc/cron.d \
    /etc/cron.hourly \
    /etc/cron.daily \
    /etc/cron.weekly \
    /etc/cron.monthly
do
    if [ -d "$dir" ]; then
        printf '\n--- %s ---\n' "$dir"

        find "$dir" \
            -maxdepth 1 \
            -type f \
            -printf '%p\n' 2>/dev/null
    fi
done

section "COLLECTION COMPLETE"

printf 'This script gathered a limited system snapshot.\n'
printf 'Its output is not a malware verdict or full forensic record.\n'

# RDV ANCT Monitor (Android)

Simple Android script that monitors an ANCT appointment page and notifies you when a slot becomes available.

## Features

- Runs locally on your phone with Termux
- Android notifications and vibration
- Timestamped logs

## Requirements

Install from F-Droid:

- Termux
- Termux:API

Install dependencies:

```bash
pkg update
pkg install python termux-api cronie
pip install requests
```

## Configuration

Edit the URL in `check_rdv.py`:

```python
URL = "YOUR_ANCT_APPOINTMENT_URL"
```

## Run Manually

```bash
python check_rdv.py
```

## Run Automatically

Edit your crontab:

```bash
crontab -e
```

Add:

```cron
*/3 7-18 * * 1-5 python ~/scripts/check_rdv.py >> ~/rdv.log 2>&1
```

This runs:

- Every 3 minutes
- Monday to Friday
- From 07:00 to 18:59

Start cron:

```bash
crond
```

## Logs

View logs:

```bash
tail -f ~/rdv.log
```

Example:

```text
[2026-06-24 07:00:00] ❌ Aucun créneau
[2026-06-24 07:03:00] ❌ Aucun créneau
[2026-06-24 09:42:00] ✅ RDV DISPONIBLE
```

## Notification

When a slot is detected, your phone will:

- Display a notification
- Vibrate
- Show the appointment URL

## Disclaimer

This project may stop working if the ANCT website changes.

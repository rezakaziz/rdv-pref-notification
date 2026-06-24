import requests
import subprocess
from pathlib import Path

URL = "https://rdv.anct.gouv.fr/prendre_rdv?motif_name_with_location_type=renouvellement_de_recepisses_arrives_a_echeance_-public_office&public_link_organisation_id=2458"

NO_SLOT_MESSAGE = (
    "Malheureusement, aucun créneau correspondant à votre recherche n'a été trouvé."
)

STATE_FILE = Path.home() / ".rdv_anct_state"


def notify(title, content):
    subprocess.run(
        [
            "termux-notification",
            "--title",
            title,
            "--content",
            content,
            "--priority",
            "high",
            "--sound",
            "--vibrate",
            "1000",
        ]
    )


def vibrate():
    subprocess.run(["termux-vibrate", "-d", "1500"])


def alert_slot_found():
    notify("🚨 RDV ANCT disponible", f"Un créneau semble disponible.\n{URL}")
    for _ in range(3):
        vibrate()


def check_slots():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    r.raise_for_status()
    return NO_SLOT_MESSAGE not in r.text


def main():
    try:
        available = check_slots()
        previous = STATE_FILE.read_text().strip() if STATE_FILE.exists() else "0"

        if available and previous != "1":
            print("✅ RDV DISPONIBLE")
            alert_slot_found()
        elif available:
            print("✅ RDV toujours disponible, notification déjà envoyée")
        else:
            print("❌ Aucun créneau")
            alert_slot_found()

        STATE_FILE.write_text("1" if available else "0")

    except Exception as e:
        print("Erreur:", e)


if __name__ == "__main__":
    main()

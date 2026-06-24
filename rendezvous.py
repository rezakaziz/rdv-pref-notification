import os
import requests

URL = "https://rdv.anct.gouv.fr/prendre_rdv?motif_name_with_location_type=renouvellement_de_recepisses_arrives_a_echeance_-public_office&public_link_organisation_id=2458"

NTFY_TOPIC = os.environ["NTFY_TOPIC"]

NO_SLOT_MESSAGE = (
    "Malheureusement, aucun créneau correspondant à votre recherche n'a été trouvé."
)


def send_notification():
    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=f"✅ RDV disponible !\n\n{URL}".encode("utf-8"),
        headers={
            "Title": "RDV ANCT disponible",
            "Priority": "urgent",
            "Tags": "warning",
        },
        timeout=10,
    )


def check_slots():
    r = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    r.raise_for_status()
    return NO_SLOT_MESSAGE not in r.text


print("🔍 Vérification RDV...")

if check_slots():
    print("✅ RDV DISPONIBLE !!!")
    send_notification()
else:
    print("❌ Aucun créneau")

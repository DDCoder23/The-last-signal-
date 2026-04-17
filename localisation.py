import requests
from typing import Dict, Optional


async def obtenir_localisation_par_ip(ip: Optional[str] = None) -> Dict:
    url = f"http://ip-api.com/json/{ip}" if ip else "http://ip-api.com/json"
    try:
        reponse = requests.get(url, timeout=5)
        reponse.raise_for_status()  # Vérifie les erreurs HTTP

        donnees = reponse.json()
        if donnees["status"] == "success":
            return {
                "statut": "success",
                "pays": donnees.get("country", "Inconnu"),
                "ville": donnees.get("city", "Inconnu"),
                "fuseau_horaire": donnees.get("timezone", "Inconnu"),
                "latitude": donnees.get("lat", 0.0),
                "longitude": donnees.get("lon", 0.0),
                "isp": donnees.get("isp", "Inconnu"),
                **donnees,
            }
        else:
            return {
                "statut": "fail",
                "message": donnees.get("message", "Échec de la requête."),
            }
    except requests.exceptions.RequestException as e:
        return {"statut": "fail", "message": f"Erreur lors de la requête : {str(e)}"}

import datetime
import pytz
from typing import Tuple, Optional
import localisation

# Fuseau horaire par défaut : Europe/Paris (GMT+1/GMT+2)
FUSEAU_PAR_DEFAUT = pytz.timezone("Europe/Paris")


async def obtenir_heure_actuelle(fuseau: Optional[str] = None) -> datetime.datetime:
    """
    Retourne l'heure actuelle locale pour un fuseau horaire donné.
    Si aucun fuseau n'est spécifié, utilise Europe/Paris (GMT+1/GMT+2).

    Args:
        fuseau (str, optional): Nom du fuseau horaire (ex: "Europe/London", "America/New_York").
                                Defaults to None (utilise FUSEAU_PAR_DEFAUT).

    Returns:
        datetime.datetime: L'heure actuelle locale pour le fuseau spécifié.
    """
    if fuseau:
        return datetime.datetime.now(pytz.timezone(fuseau))
    return datetime.datetime.now(FUSEAU_PAR_DEFAUT)


async def convertir_heure_vers_local(
    heure_utc: datetime.datetime, fuseau: Optional[str] = None
) -> datetime.datetime:
    """
    Convertit une heure UTC en heure locale pour un fuseau horaire donné.

    Args:
        heure_utc (datetime.datetime): Une heure au format UTC.
        fuseau (str, optional): Nom du fuseau horaire cible. Defaults to None (utilise FUSEAU_PAR_DEFAUT).

    Returns:
        datetime.datetime: L'heure convertie en heure locale.
    """
    if fuseau:
        return heure_utc.astimezone(pytz.timezone(fuseau))
    return heure_utc.astimezone(FUSEAU_PAR_DEFAUT)


async def formater_heure(heure: datetime.datetime, format: str = "%H:%M:%S") -> str:
    """
    Formate une heure selon un format personnalisé.
    Par défaut, le format est "HH:MM:SS".

    Args:
        heure (datetime.datetime): L'heure à formater.
        format (str, optional): Le format de sortie. Defaults to "%H:MM:SS".

    Returns:
        str: L'heure formatée en chaîne de caractères.
    """
    return heure.strftime(format)


async def obtenir_heure_et_saison(fuseau: Optional[str] = None) -> Tuple[str, str]:
    """
    Retourne l'heure actuelle et la saison (été/hiver) pour un fuseau horaire donné.
    Utile pour adapter des éléments du jeu (ex: durée du jour, événements spéciaux).

    Args:
        fuseau (str, optional): Nom du fuseau horaire. Defaults to None (utilise FUSEAU_PAR_DEFAUT).

    Returns:
        Tuple[str, str]: Un tuple contenant (heure_formatée, saison).
    """
    maintenant = await obtenir_heure_actuelle(fuseau)
    heure_formattee = await formater_heure(maintenant)
    saison = "été" if maintenant.dst() != datetime.timedelta(0) else "hiver"
    return heure_formattee, saison


async def est_il_jour(
    fuseau: Optional[str] = None, heure_debut_jour: int = 6, heure_fin_jour: int = 18
) -> bool:
    """
    Détermine si c'est le jour ou la nuit pour un fuseau horaire donné.
    Par défaut, le jour dure de 6h à 18h.

    Args:
        fuseau (str, optional): Nom du fuseau horaire. Defaults to None (utilise FUSEAU_PAR_DEFAUT).
        heure_debut_jour (int, optional): Heure de début du jour. Defaults to 6.
        heure_fin_jour (int, optional): Heure de fin du jour. Defaults to 18.

    Returns:
        bool: True si c'est le jour, False si c'est la nuit.
    """
    maintenant = await obtenir_heure_actuelle(fuseau)
    heure = maintenant.hour
    return heure_debut_jour <= heure < heure_fin_jour


async def trouver_fuseau():
    local = await localisation.obtenir_localisation_par_ip()
    if local["statut"] == "success":
        print(f"Fuseau horaire local: {local['fuseau_horaire']}")
        heure = await formater_heure(
            await obtenir_heure_actuelle(local["fuseau_horaire"])
        )
    else:
        heure = await formater_heure(await obtenir_heure_actuelle())

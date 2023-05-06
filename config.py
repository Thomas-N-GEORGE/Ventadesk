"""Settings and other vars."""


# Order state choices:
NON_TRAITEE = "NT"
EN_COURS_DE_TRAITEMENT = "CT"
EN_ATTENTE_APPROVISIONNEMENT = "AA"
PREPARATION_EXPEDITION = "PE"
EN_ATTENTE_PAIEMENT ="AP"
EXPEDIEE = "EX"
TRAITEE_ARCHIVEE = "TA"
ANNULEE = "AN"

STATUS_CHOICES = [
    (NON_TRAITEE, "Non traitée"),
    (EN_COURS_DE_TRAITEMENT, "En cours de traitement"),
    (EN_ATTENTE_APPROVISIONNEMENT, "En attente d'approvisionnement"),
    (PREPARATION_EXPEDITION, "En préparation à l'expédition"),
    (EN_ATTENTE_PAIEMENT, "En attente de paiement"),
    (EXPEDIEE, "Expédiée"),
    (TRAITEE_ARCHIVEE, "Traitée"),
    (ANNULEE, "Annulée"),
]
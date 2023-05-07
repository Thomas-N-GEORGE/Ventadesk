"""Settings and other vars."""


# API URLs
API_URL = "http://127.0.0.1:8000/api/"
API_TOKEN_URL = "http://127.0.0.1:8000/api/api-token-auth/"

# Choices for order status :
STATUS_CHOICES = {
    "CR": "Créée",
    "CT": "En cours de traitement",
    "AA": "En attente d'approvisionnement",
    "PE": "En préparation à l'expédition",
    "AP": "En attente de paiement",
    "EX": "Expédiée",
    "TA": "Traitée",
    "AN": "Annulée",
}

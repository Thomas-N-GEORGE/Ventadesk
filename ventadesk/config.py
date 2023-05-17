"""Settings and other vars."""


# API URLs
# DEV
# API_URL = "http://127.0.0.1:8000/api/"
# API_TOKEN_URL = "http://127.0.0.1:8000/api/api-token-auth/"

# PROD
API_URL = "https://ventalis.herokuapp.com/api/"
API_TOKEN_URL = "https://ventalis.herokuapp.com/api/api-token-auth/"


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

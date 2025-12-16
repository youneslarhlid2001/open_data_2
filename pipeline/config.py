"""
Configuration centralisée du pipeline.
"""

from pathlib import Path

# Chemins du projet
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Création des dossiers si nécessaire
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Configuration API OpenFoodFacts
API_BASE_URL = "https://world.openfoodfacts.org/api/v2"
API_ENDPOINT = "/search"

# Paramètres de récupération
API_PARAMS = {
    "categories_tags": "en:beverages",
    "page_size": 100,
    "fields": "code,product_name,brands,categories,nutriscore_grade,nova_group,energy_100g,fat_100g,sugars_100g,salt_100g,proteins_100g"
}

# Pagination
MAX_PAGES = 10
PAGE_SIZE = 100

# Configuration réseau
REQUEST_TIMEOUT = 30  # secondes
MAX_RETRIES = 3
RETRY_DELAY = 2  # secondes entre les tentatives
RATE_LIMIT_DELAY = 0.5  # secondes entre les requêtes

# Champs attendus dans les données
EXPECTED_FIELDS = [
    "code",
    "product_name",
    "brands",
    "categories",
    "nutriscore_grade",
    "nova_group",
    "energy_100g",
    "fat_100g",
    "sugars_100g",
    "salt_100g",
    "proteins_100g"
]


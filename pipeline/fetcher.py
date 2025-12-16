"""
Module de récupération des données depuis l'API OpenFoodFacts.
Gère la pagination, les retries et les erreurs réseau.
"""

import time
import logging
from typing import List, Dict, Optional

import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from tqdm import tqdm

from pipeline.config import (
    API_BASE_URL,
    API_ENDPOINT,
    API_PARAMS,
    MAX_PAGES,
    PAGE_SIZE,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    RATE_LIMIT_DELAY
)

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=RETRY_DELAY, min=1, max=10),
    retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
    reraise=True
)
def fetch_page(page: int, client: Optional[httpx.Client] = None) -> Dict:
    """
    Récupère une page de données depuis l'API.
    
    Args:
        page: Numéro de la page à récupérer (commence à 1)
        client: Client HTTP réutilisable (optionnel)
    
    Returns:
        Dictionnaire contenant la réponse JSON de l'API
    
    Raises:
        httpx.RequestError: En cas d'erreur réseau
        httpx.HTTPStatusError: En cas d'erreur HTTP
    """
    params = {**API_PARAMS, "page": page}
    url = f"{API_BASE_URL}{API_ENDPOINT}"
    
    try:
        if client:
            response = client.get(url, params=params, timeout=REQUEST_TIMEOUT)
        else:
            with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
                response = client.get(url, params=params)
        
        response.raise_for_status()
        return response.json()
    
    except httpx.RequestError as e:
        logger.error(f"Erreur réseau lors de la récupération de la page {page}: {e}")
        raise
    except httpx.HTTPStatusError as e:
        logger.error(f"Erreur HTTP {e.response.status_code} pour la page {page}: {e}")
        raise


def fetch_all_data() -> List[Dict]:
    """
    Récupère toutes les données paginées depuis l'API.
    Gère la pagination automatique et le rate limiting.
    
    Returns:
        Liste de tous les produits récupérés
    """
    all_products = []
    
    logger.info(f"Début de la récupération des données (max {MAX_PAGES} pages)")
    
    # Utilisation d'un client HTTP réutilisable pour de meilleures performances
    with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
        for page in tqdm(range(1, MAX_PAGES + 1), desc="Récupération des pages"):
            try:
                response_data = fetch_page(page, client)
                
                # Vérification de la structure de la réponse
                if "products" not in response_data:
                    logger.warning(f"Page {page}: structure de réponse inattendue")
                    break
                
                products = response_data["products"]
                
                # Si aucune donnée, on arrête
                if not products:
                    logger.info(f"Page {page} vide, arrêt de la récupération")
                    break
                
                all_products.extend(products)
                logger.debug(f"Page {page}: {len(products)} produits récupérés")
                
                # Rate limiting entre les requêtes
                if page < MAX_PAGES:
                    time.sleep(RATE_LIMIT_DELAY)
            
            except Exception as e:
                logger.error(f"Erreur lors de la récupération de la page {page}: {e}")
                # On continue avec la page suivante au lieu de tout arrêter
                continue
    
    logger.info(f"Récupération terminée: {len(all_products)} produits au total")
    return all_products


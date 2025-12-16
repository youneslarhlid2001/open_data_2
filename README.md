# Pipeline Open Data - TP2

Pipeline complet d'acquisition, transformation et stockage de données Open Data depuis l'API OpenFoodFacts.

## 📋 Présentation du projet

Ce projet implémente un pipeline ETL (Extract, Transform, Load) pour récupérer des données nutritionnelles depuis l'API OpenFoodFacts, les nettoyer et les stocker au format Parquet.

### Choix de l'API

**OpenFoodFacts** est une base de données collaborative sur les produits alimentaires :
- API REST publique sans authentification
- Données riches : informations nutritionnelles, Nutri-Score, NOVA, etc.
- Documentation complète : https://world.openfoodfacts.org/api/v2
- Endpoint utilisé : `/search` avec pagination

## 🏗️ Structure du projet

```
tp2-pipeline/
├── pipeline/
│   ├── __init__.py
│   ├── config.py          # Configuration centralisée
│   ├── fetcher.py         # Récupération des données (API)
│   ├── transformer.py     # Transformation et nettoyage
│   ├── storage.py         # Stockage Parquet
│   └── main.py            # Orchestration du pipeline
├── data/
│   ├── raw/               # Données brutes JSON
│   └── processed/         # Données nettoyées Parquet
└── README.md
```

## 📦 Installation (backend)

Prérequis : Python 3.11+, pip.

```bash
pip install -r requirements.txt
```

## 🚀 Démarrage rapide (recommandé pour la soutenance)

1) Lancer l’API FastAPI (backend)  
```bash
uvicorn api:app --reload --port 8000
```

2) Lancer le frontend React (Vite)  
```bash
cd frontend
npm install      # première fois
npm run dev -- --host --port 5174 --strictPort
```

3) Ouvrir l’UI : http://localhost:5174  
   - Cliquer “Lancer le pipeline” → collecte, nettoyage, stockage  
   - Cliquer “Rafraîchir l’aperçu” → tableau (50 lignes) + KPI + graphes  
   - “Télécharger le Parquet” → récupère le dernier fichier traité

## 🚀 Utilisation

### État actuel du projet

**Modules disponibles :**
- ✅ `config.py` : Configuration centralisée
- ✅ `fetcher.py` : Récupération des données avec pagination et retry
- ✅ `transformer.py` : Transformation et nettoyage (pandas)
- ✅ `storage.py` : Stockage JSON/Parquet
- ✅ `main.py` : Orchestration du pipeline
- ✅ `api.py` : API FastAPI (lancement pipeline, preview, stats, download)
- ✅ Tests unitaires (pytest)
- ✅ Dockerfile pour l’API/pipeline

### Tester rapidement (fetch + pipeline)

#### Fetcher seul

```python
import logging
from pipeline.fetcher import fetch_page, fetch_all_data

logging.basicConfig(level=logging.INFO)

data = fetch_page(1)
print(f"Page 1 : {len(data.get('products', []))} produits")

all_products = fetch_all_data()
print(f"Total : {len(all_products)} produits")
```

#### Exécution du pipeline complet

```bash
python -m pipeline.main
```

Sorties :
- JSON brut horodaté dans `data/raw/`
- Parquet nettoyé dans `data/processed/`

#### API FastAPI (pilotage / visualisation)

```bash
uvicorn api:app --reload --port 8000
```

Endpoints principaux :
- `POST /run` : lance le pipeline complet (fetch → transform → save)
- `GET /preview?limit=50` : aperçu des données nettoyées
- `GET /stats` : agrégats Nutri-Score / NOVA + total de lignes
- `GET /download` : télécharge le dernier Parquet
- `GET /health` : ping de santé

#### Frontend React (Vite)

```bash
cd frontend
npm install
npm run dev -- --host --port 5174 --strictPort
```

Configuration :
- API cible via `VITE_API_URL` (défaut `http://localhost:8000`)
- Timeout UI via `VITE_API_TIMEOUT_MS` (défaut 180000 ms pour laisser finir le pipeline)
- Table (TanStack) + graphes (Recharts)

### 🧪 Tests

```bash
pytest
```

Les tests couvrent notamment la transformation / nettoyage (normalisation, déduplication, cast numériques).

### 🐳 Docker (API + pipeline)

Build :
```bash
docker build -t openfoodfacts-pipeline .
```

Run :
```bash
docker run -p 8000:8000 openfoodfacts-pipeline
```

Endpoints disponibles comme en local : `/run`, `/preview`, `/stats`, `/download`, `/health`.

## 📊 Données récupérées

Le pipeline récupère les champs suivants pour chaque produit :

- `code` : Code-barres du produit
- `product_name` : Nom du produit
- `brands` : Marques
- `categories` : Catégories
- `nutriscore_grade` : Note Nutri-Score (A à E)
- `nova_group` : Groupe NOVA (1 à 4)
- `energy_100g` : Énergie pour 100g (kcal)
- `fat_100g` : Matières grasses pour 100g (g)
- `sugars_100g` : Sucres pour 100g (g)
- `salt_100g` : Sel pour 100g (g)
- `proteins_100g` : Protéines pour 100g (g)

## ⚙️ Configuration

Les paramètres sont centralisés dans `pipeline/config.py` :

- **Pagination** : 100 produits par page, maximum 10 pages
- **Catégorie** : `en:beverages` (boissons)
- **Retry** : 3 tentatives avec backoff exponentiel
- **Rate limiting** : 0.5 seconde entre les requêtes
- **Timeout** : 30 secondes par requête

## 🔧 Fonctionnalités

### Module fetcher.py

- ✅ Récupération paginée automatique
- ✅ Gestion des erreurs réseau avec retry (tenacity)
- ✅ Rate limiting pour respecter l'API
- ✅ Client HTTP réutilisable pour performance
- ✅ Logging structuré
- ✅ Barre de progression (tqdm)

### Module transformer.py

- Nettoyage pandas (textes normalisés, minuscules, espaces)
- Cast des types numériques (coerce -> NaN)
- Suppression des doublons sur le code produit
- Suppression des lignes vides (nom/marque manquants)

### Module storage.py

- Sauvegarde JSON brut horodaté dans `data/raw/`
- Sauvegarde Parquet compressé (snappy) dans `data/processed/`
- Chargement du dernier Parquet disponible

### Module main.py

- Orchestration complète (fetch → transform → store)
- Logging lisible
- Exécutable via `python -m pipeline.main`

### API FastAPI (api.py)

- Routes `POST /run`, `GET /preview`, `GET /stats`, `GET /download`, `GET /health`
- CORS ouvert pour le frontend

### Frontend React (frontend/)

- Vite + React 18
- Table TanStack + graphiques Recharts
- Consomme l’API (config via `VITE_API_URL`)

## 📝 Exemple de sortie

Une fois le pipeline complet exécuté, vous obtiendrez :

```
data/
├── raw/
│   └── products_2025-12-16_21-30-45.json
└── processed/
    └── products_2025-12-16_21-30-45.parquet
```

## 🐛 Dépannage

### Erreur d'import

Assurez-vous d'être à la racine du projet et que Python trouve le module :

```bash
# Vérifier la structure
ls pipeline/

# Tester l'import
python -c "import pipeline.config; print('OK')"
```

### Erreur réseau

Le module `fetcher.py` gère automatiquement les erreurs réseau avec retry. Si les erreurs persistent :
- Vérifiez votre connexion Internet
- Augmentez `REQUEST_TIMEOUT` dans `config.py`
- Vérifiez que l'API OpenFoodFacts est accessible

### Pipeline trop long / timeout côté UI
- Le frontend utilise un timeout long (180 s). Si besoin, réduisez temporairement le volume pour un test rapide dans `pipeline/config.py` (ex. `MAX_PAGES=3`, `PAGE_SIZE=50`), puis remettez `10` / `100` pour la version finale notée.
- Sur réseau lent ou API lente, laissez le temps au `/run` d’aboutir ; les retries sont gérés par `tenacity`.

## 📚 Documentation

- API OpenFoodFacts : https://world.openfoodfacts.org/api/v2
- Documentation httpx : https://www.python-httpx.org/
- Documentation pandas : https://pandas.pydata.org/
- Documentation pyarrow : https://arrow.apache.org/docs/python/

## 👤 Auteur

Projet réalisé dans le cadre du TP2 - Open Data


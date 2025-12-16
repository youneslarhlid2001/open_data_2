"""
Gestion du stockage des données (JSON brut et Parquet nettoyé).
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

import pandas as pd

from pipeline.config import RAW_DATA_DIR, PROCESSED_DATA_DIR

logger = logging.getLogger(__name__)


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_raw_json(data: List[Dict], filename: Optional[str] = None) -> Path:
    """
    Sauvegarde les données brutes en JSON dans data/raw/ avec horodatage.
    """
    fname = filename or f"products_{_timestamp()}.json"
    path = RAW_DATA_DIR / fname
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info("JSON brut sauvegardé", extra={"path": str(path), "rows": len(data)})
    return path


def save_parquet(df: pd.DataFrame, filename: Optional[str] = None, compression: str = "snappy") -> Path:
    """
    Sauvegarde le DataFrame nettoyé en Parquet compressé dans data/processed/.
    """
    fname = filename or f"products_{_timestamp()}.parquet"
    path = PROCESSED_DATA_DIR / fname
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False, compression=compression)
    logger.info("Parquet sauvegardé", extra={"path": str(path), "rows": len(df), "compression": compression})
    return path


def _latest_file(directory: Path, pattern: str) -> Optional[Path]:
    files = sorted(directory.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def load_parquet(path: Optional[Path] = None) -> pd.DataFrame:
    """
    Charge un fichier Parquet. Si aucun chemin n'est donné, charge le plus récent.
    """
    target = path or _latest_file(PROCESSED_DATA_DIR, "*.parquet")
    if not target or not target.exists():
        raise FileNotFoundError("Aucun fichier Parquet trouvé dans data/processed/")
    logger.info("Chargement Parquet", extra={"path": str(target)})
    return pd.read_parquet(target)


def latest_parquet_path() -> Optional[Path]:
    """Retourne le chemin du dernier Parquet généré."""
    return _latest_file(PROCESSED_DATA_DIR, "*.parquet")


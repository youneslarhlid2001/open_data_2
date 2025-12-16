"""
Orchestration du pipeline OpenFoodFacts.
Exécution : python -m pipeline.main
"""

import logging
from typing import Dict, Any

from pipeline.fetcher import fetch_all_data
from pipeline.transformer import json_to_dataframe, clean_dataframe
from pipeline.storage import save_raw_json, save_parquet


logger = logging.getLogger(__name__)


def run_pipeline() -> Dict[str, Any]:
    """
    Chaîne complète : fetch -> transform -> stockage.
    Retourne les chemins générés et le nombre de lignes.
    """
    raw_data = fetch_all_data()
    if not raw_data:
        logger.warning("Aucune donnée récupérée, pipeline interrompu.")
        return {"raw_path": None, "parquet_path": None, "rows": 0}

    raw_path = save_raw_json(raw_data)
    df = json_to_dataframe(raw_data)
    df_clean = clean_dataframe(df)
    parquet_path = save_parquet(df_clean)

    logger.info(
        "Pipeline terminé : %s lignes | brut=%s | parquet=%s",
        len(df_clean),
        raw_path,
        parquet_path,
    )

    return {
        "raw_path": str(raw_path),
        "parquet_path": str(parquet_path),
        "rows": int(len(df_clean)),
    }


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    run_pipeline()


if __name__ == "__main__":
    main()


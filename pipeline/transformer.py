"""
Transformation et nettoyage des données OpenFoodFacts.
"""

from typing import List, Dict

import pandas as pd

from pipeline.config import EXPECTED_FIELDS


def json_to_dataframe(products: List[Dict]) -> pd.DataFrame:
    """
    Convertit la liste de produits JSON en DataFrame avec les champs attendus.
    Les colonnes manquantes sont ajoutées avec des valeurs nulles pour garantir
    une table cohérente.
    """
    df = pd.DataFrame(products or [])

    # S'assure que toutes les colonnes attendues existent
    for col in EXPECTED_FIELDS:
        if col not in df.columns:
            df[col] = pd.NA

    # Reordonne et filtre les colonnes
    df = df[EXPECTED_FIELDS]
    return df


def _normalize_text(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Nettoie les colonnes texte : trim, normalisation des espaces, minuscules."""
    for col in columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
            )
            df[col] = df[col].apply(lambda x: x.lower() if x else pd.NA)
    return df


def _cast_numeric(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Convertit les colonnes numériques en float et force les valeurs non valides à NA."""
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applique les règles de nettoyage :
    - normalisation texte (minuscules, espaces)
    - conversion numérique
    - suppression des doublons sur le code produit
    - suppression des lignes entièrement vides sur les colonnes clés
    """
    cleaned = df.copy()

    text_cols = ["product_name", "brands", "categories", "nutriscore_grade"]
    numeric_cols = [
        "nova_group",
        "energy_100g",
        "fat_100g",
        "sugars_100g",
        "salt_100g",
        "proteins_100g",
    ]

    cleaned = _normalize_text(cleaned, text_cols)
    cleaned = _cast_numeric(cleaned, numeric_cols)

    # Supprime les doublons sur le code produit
    if "code" in cleaned.columns:
        cleaned = cleaned.drop_duplicates(subset=["code"])

    # Supprime les lignes sans informations produit ni marque
    cleaned = cleaned.dropna(
        subset=["product_name", "brands"], how="all"
    ).reset_index(drop=True)

    return cleaned


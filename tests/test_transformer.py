import pandas as pd

from pipeline.transformer import json_to_dataframe, clean_dataframe


def test_json_to_dataframe_adds_missing_columns():
    products = [{"code": "1", "product_name": "Test"}]
    df = json_to_dataframe(products)
    # Toutes les colonnes attendues doivent exister
    assert "brands" in df.columns
    assert df.loc[0, "product_name"] == "Test"


def test_clean_dataframe_normalizes_and_dedupes():
    products = [
        {
            "code": "123",
            "product_name": "  Cola ",
            "brands": "Brand A",
            "energy_100g": "42",
            "fat_100g": "0.1",
        },
        {
            "code": "123",  # doublon
            "product_name": "cola",
            "brands": None,
            "energy_100g": "not_a_number",
        },
        {
            "code": "456",
            "product_name": None,
            "brands": None,  # sera drop car infos vides
        },
    ]

    df = json_to_dataframe(products)
    cleaned = clean_dataframe(df)

    # Le doublon doit être supprimé
    assert len(cleaned) == 1
    # Normalisation en minuscules + trim
    assert cleaned.iloc[0]["product_name"] == "cola"
    # Cast numérique -> float
    assert cleaned.iloc[0]["energy_100g"] == 42.0
import pandas as pd

from pipeline.config import EXPECTED_FIELDS
from pipeline.transformer import json_to_dataframe, clean_dataframe


def test_json_to_dataframe_adds_missing_columns():
    products = [{"code": "1", "product_name": "Test"}]
    df = json_to_dataframe(products)

    # toutes les colonnes attendues doivent être présentes
    assert set(EXPECTED_FIELDS) == set(df.columns)
    assert df.loc[0, "code"] == "1"
    assert df.loc[0, "product_name"] == "Test"


def test_clean_dataframe_normalizes_and_casts():
    raw = [
        {
            "code": "42",
            "product_name": "  Cola Light  ",
            "brands": " BRAND  ",
            "categories": " Drinks ",
            "nutriscore_grade": "A",
            "nova_group": "2",
            "energy_100g": "10",
            "fat_100g": "0",
            "sugars_100g": "5.5",
            "salt_100g": "0.1",
            "proteins_100g": "0",
        }
    ]
    df = json_to_dataframe(raw)
    cleaned = clean_dataframe(df)

    assert len(cleaned) == 1
    assert cleaned.loc[0, "product_name"] == "cola light"
    assert cleaned.loc[0, "brands"] == "brand"
    assert cleaned.loc[0, "nova_group"] == 2
    assert cleaned.loc[0, "sugars_100g"] == 5.5


def test_clean_dataframe_drops_empty_rows():
    raw = [{"code": "x", "product_name": None, "brands": None}]
    df = json_to_dataframe(raw)
    cleaned = clean_dataframe(df)
    assert cleaned.empty


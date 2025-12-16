"""
API FastAPI pour piloter le pipeline et exposer les données nettoyées.
"""

from pathlib import Path
from typing import Any, Dict

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from pipeline.main import run_pipeline
from pipeline.storage import load_parquet, latest_parquet_path


app = FastAPI(title="OpenFoodFacts Pipeline API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/run")
def trigger_pipeline() -> Dict[str, Any]:
    result = run_pipeline()
    if result.get("rows", 0) == 0:
        raise HTTPException(status_code=500, detail="Aucune donnée récupérée.")
    return result


@app.get("/preview")
def preview(limit: int = 50) -> Dict[str, Any]:
    try:
        df = load_parquet()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    limited = df.head(limit)
    return {
        "total_rows": int(len(df)),
        "preview": limited.to_dict(orient="records"),
    }


@app.get("/stats")
def stats() -> Dict[str, Any]:
    try:
        df = load_parquet()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    def _counts(series: pd.Series) -> Dict[str, int]:
        counts = series.dropna().value_counts().to_dict()
        # Convertit les clés en str pour la sérialisation JSON
        return {str(k): int(v) for k, v in counts.items()}

    return {
        "total_rows": int(len(df)),
        "nutriscore": _counts(df["nutriscore_grade"]) if "nutriscore_grade" in df else {},
        "nova_group": _counts(df["nova_group"]) if "nova_group" in df else {},
    }


@app.get("/download")
def download() -> FileResponse:
    path: Path | None = latest_parquet_path()
    if not path:
        raise HTTPException(status_code=404, detail="Aucun fichier Parquet disponible.")
    return FileResponse(
        path,
        media_type="application/octet-stream",
        filename=path.name,
    )


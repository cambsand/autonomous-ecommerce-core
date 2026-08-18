import sqlite3
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from database import DB_PATH
from logger import get_logger
from main import run_pipeline

logger = get_logger("APIModule")

app = FastAPI(
    title="Autonomous E-Commerce Core API",
    description="Dashboard e API per il controllo del sistema autonomo e-commerce",
    version="1.0.0"
)

def get_db_connection():
    if not DB_PATH.exists():
        raise HTTPException(status_code=404, detail="Database non ancora inizializzato.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/", summary="Stato del Sistema")
def root():
    return {
        "status": "online",
        "system": "Autonomous E-Commerce Core Engine",
        "endpoints": {
            "docs": "/docs",
            "products": "/api/products",
            "stats": "/api/stats"
        }
    }

@app.get("/api/products", summary="Lista Prodotti Approvati")
def get_approved_products() -> List[Dict[str, Any]]:
    """Restituisce tutti i prodotti vincenti approvati e salvati nel database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM winning_products ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

@app.get("/api/stats", summary="Statistiche e Metriche")
def get_pipeline_stats():
    """Calcola le metriche aggregate di redditivita e margine dal DB."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), AVG(net_margin_pct), SUM(net_profit_per_unit) FROM winning_products")
        count, avg_margin, total_profit = cursor.fetchone()
        
        return {
            "total_winning_products": count or 0,
            "average_net_margin_pct": round(avg_margin, 2) if avg_margin else 0.0,
            "total_unit_profit_pool": round(total_profit, 2) if total_profit else 0.0
        }

@app.post("/api/run-pipeline", summary="Avvio Manuale Pipeline")
def trigger_pipeline():
    """Forza l'esecuzione immediata di un ciclo completo di scansione."""
    try:
        logger.info("Avvio manuale della pipeline richiesto tramite API.")
        run_pipeline()
        return {"status": "success", "message": "Pipeline eseguita con successo."}
    except Exception as e:
        logger.error(f"Errore durante l'esecuzione API della pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))
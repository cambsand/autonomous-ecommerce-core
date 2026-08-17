import json
import csv
import sqlite3
from pathlib import Path
from typing import List, Dict, Any
from logger import get_logger
from database import DB_PATH

logger = get_logger("StoreExporter")
EXPORT_DIR = Path("exports")

class StoreExporterEngine:
    """Modulo enterprise per l'esportazione automatica delle schede prodotto dal DB ai feed e-commerce."""

    def __init__(self):
        EXPORT_DIR.mkdir(exist_ok=True)

    def _fetch_all_winning_products(self) -> List[Dict[str, Any]]:
        if not DB_PATH.exists():
            logger.error("Database non trovato per l'esportazione.")
            return []
            
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM winning_products ORDER BY id DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def export_to_json(self, filename: str = "shopify_import.json") -> Path:
        """Esporta i prodotti approvati in formato JSON standard per API e-commerce."""
        products = self._fetch_all_winning_products()
        output_path = EXPORT_DIR / filename
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(products, f, indent=4, ensure_ascii=False)
            
        logger.info(f"Esportati {len(products)} prodotti in formato JSON: {output_path}")
        return output_path

    def export_to_csv(self, filename: str = "catalog_export.csv") -> Path:
        """Esporta i prodotti in formato CSV compatibile con Shopify e WooCommerce."""
        products = self._fetch_all_winning_products()
        output_path = EXPORT_DIR / filename
        
        if not products:
            logger.warning("Nessun prodotto presente a DB per l'esportazione CSV.")
            return output_path

        fieldnames = list(products[0].keys())
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(products)
            
        logger.info(f"Esportati {len(products)} prodotti in formato CSV: {output_path}")
        return output_path

if __name__ == "__main__":
    exporter = StoreExporterEngine()
    json_file = exporter.export_to_json()
    csv_file = exporter.export_to_csv()
    print(f"\n--- TEST ESPORTAZIONE COMPLETATO ---")
    print(f"File generati in: {EXPORT_DIR.resolve()}")
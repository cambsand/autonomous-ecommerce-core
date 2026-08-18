import json
import csv
from pathlib import Path
from typing import List, Dict, Any
from logger import get_logger

logger = get_logger("StoreExporter")

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "exports"

class StoreExporterEngine:
    """
    Modulo per l'esportazione dei cataloghi prodotti in formato JSON (Shopify) e CSV.
    """
    def __init__(self):
        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    def export_to_shopify_json(self, products: List[Dict[str, Any]]) -> str:
        filepath = EXPORTS_DIR / "shopify_import.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(products, f, indent=4, ensure_ascii=False)
        logger.info(f"Esportati {len(products)} prodotti in formato JSON: {filepath}")
        return str(filepath)

    def export_to_csv(self, products: List[Dict[str, Any]]) -> str:
        filepath = EXPORTS_DIR / "catalog_export.csv"
        if not products:
            return str(filepath)
            
        fieldnames = list(products[0].keys())
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(products)
        logger.info(f"Esportati {len(products)} prodotti in formato CSV: {filepath}")
        return str(filepath)

if __name__ == "__main__":
    exporter = StoreExporterEngine()
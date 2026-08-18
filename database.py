import sqlite3
from pathlib import Path
from typing import Dict, Any
from logger import get_logger

logger = get_logger("DatabaseManager")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "ecommerce_core.db"

class DatabaseManager:
    """
    Gestore del database SQLite per l'archiviazione e persistenza dei prodotti vincenti.
    """
    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(DB_PATH)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS winning_products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT NOT NULL,
                    category TEXT,
                    selling_price REAL,
                    cogs REAL,
                    markup_factor REAL,
                    net_margin_pct REAL,
                    net_profit_per_unit REAL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        logger.info("Database SQLite inizializzato e tabelle verificate.")

    def save_winning_product(self, product: Dict[str, Any]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO winning_products 
                (product_name, category, selling_price, cogs, markup_factor, net_margin_pct, net_profit_per_unit, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product["product_name"],
                product.get("category", ""),
                product["selling_price"],
                product["cogs"],
                product["markup_factor"],
                product["net_margin_pct"],
                product["net_profit_per_unit"],
                product.get("description", "")
            ))
            conn.commit()
        logger.info(f"Prodotto salvato a database: {product['product_name']}")

if __name__ == "__main__":
    db = DatabaseManager()
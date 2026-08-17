import sqlite3
from pathlib import Path
from typing import Dict, Any, List
from logger import get_logger

logger = get_logger("DatabaseManager")
DB_PATH = Path("data/ecommerce.db")

class DatabaseEngine:
    def __init__(self):
        DB_PATH.parent.mkdir(exist_ok=True)
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(DB_PATH)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS winning_products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT UNIQUE NOT NULL,
                    selling_price REAL NOT NULL,
                    net_profit REAL NOT NULL,
                    net_margin_pct REAL NOT NULL,
                    description TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        logger.info("Database SQLite inizializzato e tabelle verificate.")

    def save_product(self, product_data: Dict[str, Any]) -> bool:
        query = """
            INSERT INTO winning_products (product_name, selling_price, net_profit, net_margin_pct, description)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(product_name) DO UPDATE SET
                selling_price=excluded.selling_price,
                net_profit=excluded.net_profit,
                net_margin_pct=excluded.net_margin_pct,
                description=excluded.description
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (
                    product_data["product_name"],
                    product_data.get("selling_price", 0.0),
                    product_data["net_profit_per_unit"],
                    product_data["net_margin_pct"],
                    product_data["description"]
                ))
                conn.commit()
            logger.info(f"Prodotto salvato a DB: {product_data['product_name']}")
            return True
        except Exception as e:
            logger.error(f"Errore durante il salvataggio a DB del prodotto {product_data['product_name']}: {e}")
            return False

# Test rapido di inizializzazione
db = DatabaseEngine()
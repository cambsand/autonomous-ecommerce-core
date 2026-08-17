import os
from pathlib import Path
from dotenv import load_dotenv
from logger import get_logger

logger = get_logger("ConfigModule")

# Carica il file .env se presente
load_dotenv()

class AppConfig:
    MIN_NET_MARGIN_PCT: float = float(os.getenv("MIN_NET_MARGIN_PCT", 35.0))
    MIN_MARKUP_FACTOR: float = float(os.getenv("MIN_MARKUP_FACTOR", 4.0))
    DEFAULT_SHIPPING_COST: float = float(os.getenv("DEFAULT_SHIPPING_COST", 5.00))
    DEFAULT_CAC: float = float(os.getenv("DEFAULT_CAC", 15.00))
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    SERPAPI_KEY: str = os.getenv("SERPAPI_KEY", "")

config = AppConfig()
logger.info("Configurazioni di sistema caricate con successo.")
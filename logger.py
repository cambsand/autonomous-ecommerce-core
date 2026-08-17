import logging
import sys
from pathlib import Path

# Creazione cartella log se non presente
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configurazione formattatore log
LOG_FILE = LOG_DIR / "ecommerce_core.log"
log_format = "%(asctime)s | [%(levelname)s] | %(name)s | %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

def get_logger(module_name: str) -> logging.Logger:
    """Restituisce un'istanza del logger dedicata al modulo richiedente."""
    return logging.getLogger(module_name)

# Test rapido di funzionamento
if True:
    logger = get_logger("SystemInit")
    logger.info("Modulo di Logging Enterprise configurato correttamente.")
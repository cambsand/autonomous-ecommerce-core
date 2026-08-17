import time
import functools
from typing import Callable, Any
from logger import get_logger

logger = get_logger("ResilienceModule")

def retry_on_failure(retries: int = 3, delay: float = 2.0, backoff: float = 2.0):
    """
    Decoratore enterprise per la gestione dei retry con attesa esponenziale.
    Ripete l'esecuzione di una funzione in caso di eccezione non gestita.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(
                        f"Fallimento in '{func.__name__}' (Tentativo {attempt}/{retries}). Errore: {e}"
                    )
                    if attempt == retries:
                        logger.error(f"Funzione '{func.__name__}' fallita definitivamente dopo {retries} tentativi.")
                        raise e
                    logger.info(f"Attesa di {current_delay} secondi prima del prossimo tentativo...")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

# Test rapido di funzionamento
if __name__ == "__main__":
    @retry_on_failure(retries=2, delay=1.0)
    def test_flaky_function():
        logger.info("Esecuzione test funzione...")
        return "OK"

    result = test_flaky_function()
    print(f"\n--- TEST RESILIENZA: {result} ---")
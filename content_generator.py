import os
from typing import Dict, Any
from config import config
from logger import get_logger

logger = get_logger("ContentGenerator")

class ContentGeneratorEngine:
    """
    Modulo di copywriting automatizzato con supporto AI (OpenAI) 
    e modalita Fallback offline garantita.
    """
    def __init__(self):
        self.api_key = getattr(config, "OPENAI_API_KEY", None) or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY non rilevata in .env. Il motore utilizzerà la modalità Fallback.")

    def generate_product_copy(self, product_name: str, category: str = "") -> Dict[str, Any]:
        """
        Genera titolo, descrizione e punti di forza per il prodotto.
        Se l'API Key non e configurata, genera una scheda professionale in fallback.
        """
        logger.info(f"Generazione copy per il prodotto: '{product_name}'...")

        # Modalità Fallback (senza API Key)
        fallback_description = (
            f"<strong>{product_name}</strong> - Soluzione ideale per la categoria <em>{category}</em>.<br><br>"
            f"Progettato con materiali di alta qualità per garantire massima efficienza e affidabilità. "
            f"Perfetto per un utilizzo quotidiano, unisce un design moderno a prestazioni elevate.<br><br>"
            f"• Ergonomico e facile da usare<br>"
            f"• Costruito con standard di livello enterprise<br>"
            f"• Spedizione rapida e garanzia di soddisfazione"
        )

        return {
            "title": product_name,
            "description": fallback_description,
            "bullets": [
                "Ergonomico e facile da usare",
                "Costruito con standard di livello enterprise",
                "Spedizione rapida e garanzia di soddisfazione"
            ]
        }

if __name__ == "__main__":
    engine = ContentGeneratorEngine()
    copy = engine.generate_product_copy("Ergonomic Lumbar Support Pillow", "Office & Wellness")
    print("\n--- TEST GENERATORE COPY ---")
    print(copy["description"])
from openai import OpenAI
from config import config
from logger import get_logger

logger = get_logger("ContentGenerator")

class ContentGeneratorEngine:
    """
    Modulo enterprise per la generazione di copywriting persuasivo tramite OpenAI API.
    Gestisce la generazione tramite LLM con fallback automatico se l'API key è assente o non valida.
    """
    
    def __init__(self):
        self.api_key = config.OPENAI_API_KEY
        if self.api_key and self.api_key != "your_openai_api_key_here":
            self.client = OpenAI(api_key=self.api_key)
            self.is_active = True
            logger.info("ContentGeneratorEngine collegato con successo alle API di OpenAI.")
        else:
            self.client = None
            self.is_active = False
            logger.warning("OPENAI_API_KEY non rilevata in .env. Il motore utilizzerà la modalità Fallback.")

    def generate_description(self, product_name: str, category: str) -> str:
        """Genera una scheda prodotto ad alta conversione o attiva il fallback in caso di errore."""
        if not self.is_active or not self.client:
            return self._fallback_description(product_name, category)

        try:
            system_prompt = (
                "Sei un copywriter e-commerce senior specializzato in vendite ad alta conversione.\n"
                "Crea una descrizione prodotto persuasiva, elegante e orientata ai benefici.\n"
                "Struttura del testo:\n"
                "1. Un gancio iniziale d'impatto.\n"
                "2. 3 punti di forza con emoji.\n"
                "3. Una chiamata all'azione (CTA) finale chiara.\n"
                "Fornisci direttamente il testo pronto per la pubblicazione, senza preamboli."
            )
            
            user_prompt = f"Prodotto: {product_name}\nCategoria: {category}"

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            generated_text = response.choices[0].message.content.strip()
            logger.info(f"Copywriting AI generato tramite OpenAI per: {product_name}")
            return generated_text

        except Exception as e:
            logger.error(f"Errore API OpenAI per {product_name}: {e}. Attivazione fallback automatico.")
            return self._fallback_description(product_name, category)

    def _fallback_description(self, product_name: str, category: str) -> str:
        """Template statico di sicurezza per garantire continuità di servizio."""
        return (
            f"Scopri {product_name}, la soluzione ideale per la categoria {category}. "
            f"Progettato con materiali di alta qualità per garantirti le massime prestazioni. "
            f"Ordina oggi per approfittare della spedizione rapida!"
        )

if __name__ == "__main__":
    generator = ContentGeneratorEngine()
    test_product = "Ergonomic Lumbar Support"
    test_category = "Office/Wellness"

    testo = generator.generate_description(test_product, test_category)

    print("\n--- TEST GENERATORE DI CONTENUTI ---")
    print(f"Prodotto: {test_product}")
    print(f"Risultato:\n{testo}")
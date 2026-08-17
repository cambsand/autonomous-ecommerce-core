import random

class ContentGeneratorEngine:
    """
    Modulo per la generazione automatica di testi persuasivi per l'e-commerce.
    In produzione, questo modulo si collegherà alle API di OpenAI (es. ChatGPT).
    Attualmente simula la generazione scegliendo tra template pre-strutturati.
    """

    @staticmethod
    def generate_description(product_name: str, category: str) -> str:
        # Template di copywriting persuasivo simulati
        templates = [
            f"Scopri {product_name}, la soluzione definitiva per la categoria {category}. Progettato con materiali premium per massimizzare i tuoi risultati e garantirti il massimo comfort.",
            f"Stanco dei soliti prodotti scadenti? {product_name} è qui per rivoluzionare la tua esperienza nel settore {category}. Affidabilità e qualità senza compromessi.",
            f"Migliora le tue giornate con {product_name}. Il best-seller assoluto nella nicchia {category}, scelto da migliaia di clienti soddisfatti. Acquistalo ora prima che finiscano le scorte!"
        ]
        
        # Simula il tempo di "pensiero" dell'AI e restituisce un testo
        return random.choice(templates)

# Esecuzione diretta per testare il modulo
generator = ContentGeneratorEngine()
test_product = "Ergonomic Lumbar Support"
test_category = "Office/Wellness"

testo_generato = generator.generate_description(test_product, test_category)

print("--- TEST GENERAZIONE COPYWRITING ---")
print(f"Prodotto: {test_product}")
print(f"Descrizione AI:\n{testo_generato}")
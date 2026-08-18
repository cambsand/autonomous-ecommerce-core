import requests
from typing import Dict, Any
from config import config
from logger import get_logger
from resilience import retry_on_failure

logger = get_logger("StorePublisher")

class StorePublisherEngine:
    """
    Modulo per la pubblicazione automatica diretta via API REST 
    verso store Shopify / WooCommerce.
    """

    def __init__(self):
        self.shopify_store_url = getattr(config, "SHOPIFY_STORE_URL", None)
        self.shopify_access_token = getattr(config, "SHOPIFY_ACCESS_TOKEN", None)

    @retry_on_failure(retries=3, delay=2.0)
    def publish_to_shopify(self, product_data: Dict[str, Any]) -> bool:
        """
        Pubblica un prodotto approvato direttamente nello store Shopify via REST API.
        Senza credenziali attive, simula la pubblicazione e logga lo stato.
        """
        if not self.shopify_store_url or not self.shopify_access_token:
            logger.warning(
                f"Credenziali Shopify non configurate in .env. "
                f"Prodotto '{product_data['product_name']}' salvato come bozza locale."
            )
            return False

        url = f"https://{self.shopify_store_url}/admin/api/2024-01/products.json"
        headers = {
            "X-Shopify-Access-Token": self.shopify_access_token,
            "Content-Type": "application/json"
        }

        payload = {
            "product": {
                "title": product_data["product_name"],
                "body_html": product_data.get("description", ""),
                "vendor": "Autonomous Engine",
                "status": "draft",  # Imposta 'active' per pubblicare direttamente live
                "variants": [
                    {
                        "price": str(product_data["selling_price"]),
                        "sku": f"AUTO-{product_data['product_name'][:3].upper()}"
                    }
                ]
            }
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code in (200, 201):
            logger.info(f"Prodotto '{product_data['product_name']}' pubblicato con successo su Shopify!")
            return True
        else:
            logger.error(f"Errore durante la pubblicazione su Shopify ({response.status_code}): {response.text}")
            return False

if __name__ == "__main__":
    publisher = StorePublisherEngine()
    test_product = {
        "product_name": "Ergonomic Lumbar Support Pillow",
        "selling_price": 80.00,
        "description": "<p>Supporto lombare ergonomico ad alta densita per postura e ufficio.</p>"
    }
    publisher.publish_to_shopify(test_product)
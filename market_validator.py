from dataclasses import dataclass
from typing import Dict, Any, List
from config import config
from logger import get_logger

logger = get_logger("MarketValidator")

@dataclass
class OpportunityMetrics:
    product_name: str
    selling_price: float
    cogs: float
    estimated_shipping_cost: float
    estimated_cac: float

class MarketValidationEngine:
    """
    Modulo per la validazione economico-finanziaria delle opportunita e-commerce.
    """
    def __init__(self):
        logger.info("MarketValidationEngine inizializzato.")

    def evaluate_opportunity(self, metrics: OpportunityMetrics) -> Dict[str, Any]:
        rejection_reasons: List[str] = []

        # Arrotondamento a 2 decimali per evitare problemi con numeri come 3.9995x
        markup_factor = round(metrics.selling_price / metrics.cogs, 2)
        
        gross_profit = metrics.selling_price - metrics.cogs
        total_unit_cost = metrics.cogs + metrics.estimated_shipping_cost + metrics.estimated_cac
        net_profit_per_unit = round(metrics.selling_price - total_unit_cost, 2)
        net_margin_pct = round((net_profit_per_unit / metrics.selling_price) * 100, 2) if metrics.selling_price > 0 else 0.0

        # Verifiche criteri minimi di sostenibilita
        if markup_factor < config.MIN_MARKUP_FACTOR:
            rejection_reasons.append(f"Markup insufficiente ({markup_factor:.2f}x < {config.MIN_MARKUP_FACTOR}x)")

        if net_margin_pct < config.MIN_NET_MARGIN_PCT:
            rejection_reasons.append(f"Margine netto insufficiente ({net_margin_pct}% < {config.MIN_NET_MARGIN_PCT}%)")

        is_viable = len(rejection_reasons) == 0

        return {
            "product_name": metrics.product_name,
            "selling_price": metrics.selling_price,
            "cogs": metrics.cogs,
            "markup_factor": markup_factor,
            "gross_profit": gross_profit,
            "net_profit_per_unit": net_profit_per_unit,
            "net_margin_pct": net_margin_pct,
            "is_viable": is_viable,
            "rejection_reasons": rejection_reasons
        }

if __name__ == "__main__":
    engine = MarketValidationEngine()
    test_metrics = OpportunityMetrics(
        product_name="Ergonomic Lumbar Support",
        selling_price=80.00,
        cogs=20.00,
        estimated_shipping_cost=8.00,
        estimated_cac=15.13
    )
    res = engine.evaluate_opportunity(test_metrics)
    print("\n--- ESITO VALIDAZIONE OPPORTUNITA ---")
    print(f"Prodotto: {res['product_name']}")
    print(f"Approvato: {res['is_viable']}")
    print(f"Profitto Netto: EUR {res['net_profit_per_unit']}")
    print(f"Margine Netto: {res['net_margin_pct']}%")
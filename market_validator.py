import dataclasses
from typing import Dict, Any

@dataclasses.dataclass(frozen=True)
class OpportunityMetrics:
    product_name: str
    selling_price: float
    cogs: float
    estimated_shipping_cost: float
    estimated_cac: float
    payment_gateway_fee_pct: float = 0.029
    payment_gateway_fee_fixed: float = 0.30
    target_min_margin_pct: float = 0.35
    target_min_markup: float = 4.0

class MarketValidationEngine:
    """
    Motore di validazione finanziaria per l'infrastruttura e-commerce autonoma.
    Esegue lo screening matematico delle opportunità prima di qualsiasi allocazione di risorse.
    """

    @staticmethod
    def evaluate_opportunity(metrics: OpportunityMetrics) -> Dict[str, Any]:
        actual_markup = metrics.selling_price / metrics.cogs if metrics.cogs > 0 else 0.0
        gateway_fee = (metrics.selling_price * metrics.payment_gateway_fee_pct) + metrics.payment_gateway_fee_fixed
        total_unit_cost = metrics.cogs + metrics.estimated_shipping_cost + metrics.estimated_cac + gateway_fee
        net_profit = metrics.selling_price - total_unit_cost
        net_margin_pct = net_profit / metrics.selling_price if metrics.selling_price > 0 else 0.0

        passed_markup = actual_markup >= metrics.target_min_markup
        passed_margin = net_margin_pct >= metrics.target_min_margin_pct
        is_viable = passed_markup and passed_margin

        return {
            "product_name": metrics.product_name,
            "is_viable": is_viable,
            "net_profit_per_unit": round(net_profit, 2),
            "net_margin_pct": round(net_margin_pct * 100, 2),
            "actual_markup": round(actual_markup, 2),
            "rejection_reasons": [
                reason for reason, passed in [
                    (f"Markup insufficiente ({actual_markup:.2f}x < {metrics.target_min_markup}x)", passed_markup),
                    (f"Margine netto insufficiente ({net_margin_pct*100:.2f}% < {metrics.target_min_margin_pct*100}%)", passed_margin)
                ] if not passed
            ]
        }

if __name__ == "__main__":
    test_product = OpportunityMetrics(
        product_name="Ergonomic Lumbar Support",
        selling_price=79.99,
        cogs=12.50,
        estimated_shipping_cost=6.00,
        estimated_cac=22.00
    )

    engine = MarketValidationEngine()
    result = engine.evaluate_opportunity(test_product)
    
    print("--- ESITO VALIDAZIONE OPPORTUNITÀ ---")
    print(f"Prodotto: {result['product_name']}")
    print(f"Approvato: {result['is_viable']}")
    print(f"Profitto Netto: €{result['net_profit_per_unit']}")
    print(f"Margine Netto: {result['net_margin_pct']}%")
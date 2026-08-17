from trend_analyzer import TrendAnalyzerEngine
from market_validator import MarketValidationEngine, OpportunityMetrics

# 1. Inizializza i due motori
trend_engine = TrendAnalyzerEngine()
validator_engine = MarketValidationEngine()

# 2. Scansione dei trend
print("=== 1. SCANSIONE TREND ===")
trends = trend_engine.fetch_trending_opportunities()

winning_products = []

# 3. Validazione finanziaria automatica per i soli prodotti HOT
print("\n=== 2. ANALISI DI REDDITIVITA (SOLO PRODOTTI HOT) ===")
for item in trends:
    if item["is_hot"]:
        metrics = OpportunityMetrics(
            product_name=item["product_name"],
            selling_price=item["suggested_price"],
            cogs=item["cogs"],
            estimated_shipping_cost=5.00,
            estimated_cac=15.00
        )
        
        evaluation = validator_engine.evaluate_opportunity(metrics)
        
        if evaluation["is_viable"]:
            winning_products.append(evaluation)
            print(f"[APPROVATO] {evaluation['product_name']} | Margine: {evaluation['net_margin_pct']}% | Profitto: EUR {evaluation['net_profit_per_unit']}")
        else:
            print(f"[SCARTATO]  {evaluation['product_name']} | Motivo: {evaluation['rejection_reasons']}")

print(f"\n=== RISULTATO: {len(winning_products)} PRODOTTI PRONTI AL LANCIO ===")
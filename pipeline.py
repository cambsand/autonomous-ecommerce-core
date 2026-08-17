from trend_analyzer import TrendAnalyzerEngine
from market_validator import MarketValidationEngine, OpportunityMetrics
from content_generator import ContentGeneratorEngine

# 1. Inizializzazione di tutti i motori dell'infrastruttura
trend_engine = TrendAnalyzerEngine()
validator_engine = MarketValidationEngine()
generator_engine = ContentGeneratorEngine()

print("=== 1. SCANSIONE TREND E ANALISI MERCATO ===")
trends = trend_engine.fetch_trending_opportunities()

winning_products = []

print("\n=== 2. SCREENING FINANZIARIO E GENERAZIONE COPYWRITING ===")
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
            # Generazione automatica del copy per i soli prodotti promossi
            copy = generator_engine.generate_description(
                product_name=evaluation["product_name"], 
                category=item["category"]
            )
            
            evaluation["description"] = copy
            winning_products.append(evaluation)
            
            print(f"\n[APPROVATO] {evaluation['product_name']}")
            print(f"  └ Margine Netto: {evaluation['net_margin_pct']}% | Profitto Unitario: EUR {evaluation['net_profit_per_unit']}")
            print(f"  └ Descrizione Generata:\n    \"{copy}\"")
        else:
            print(f"\n[SCARTATO]  {evaluation['product_name']}")
            print(f"  └ Motivo: {evaluation['rejection_reasons']}")

print(f"\n=== REPORT FINALE: {len(winning_products)} SCHEDE PRODOTTO COMPLETE E PRONTE ===")
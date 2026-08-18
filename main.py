from database import DatabaseManager
from trend_analyzer import TrendAnalyzerEngine
from market_validator import MarketValidationEngine, OpportunityMetrics
from content_generator import ContentGeneratorEngine
from store_exporter import StoreExporterEngine
from store_publisher import StorePublisherEngine
from logger import get_logger

logger = get_logger("AutonomousCore")

def run_pipeline():
    logger.info("==================================================")
    logger.info("   AVVIO CICLO OPERATIVO E-COMMERCE AUTONOMO       ")
    logger.info("==================================================")

    db = DatabaseManager()
    trend_engine = TrendAnalyzerEngine()
    validator = MarketValidationEngine()
    copywriter = ContentGeneratorEngine()
    exporter = StoreExporterEngine()
    publisher = StorePublisherEngine()

    # FASE 1: Estrazione Trend Live
    logger.info("[FASE 1] Estrazione trend di mercato...")
    opportunities = trend_engine.fetch_trending_opportunities()

    approved_products = []

    # FASE 2: Validazione & Copywriting
    logger.info("[FASE 2] Valutazione economico-finanziaria e copywriting...")
    for opp in opportunities:
        metrics = OpportunityMetrics(
            product_name=opp["product_name"],
            selling_price=opp["suggested_price"],
            cogs=opp["cogs"],
            estimated_shipping_cost=8.00,
            estimated_cac=15.13
        )
        res = validator.evaluate_opportunity(metrics)

        if res["is_viable"]:
            copy_data = copywriter.generate_product_copy(opp["product_name"], opp["category"])
            product_record = {
                "product_name": opp["product_name"],
                "category": opp["category"],
                "selling_price": res["selling_price"],
                "cogs": res["cogs"],
                "markup_factor": res["markup_factor"],
                "net_margin_pct": res["net_margin_pct"],
                "net_profit_per_unit": res["net_profit_per_unit"],
                "description": copy_data.get("description", "")
            }
            db.save_winning_product(product_record)
            approved_products.append(product_record)
        else:
            logger.warning(f"-> PRODOTTO SCARTATO: {opp['product_name']} | Motivi: {res['rejection_reasons']}")

    # FASE 3: Esportazione Cataloghi
    logger.info("[FASE 3] Esportazione automatica cataloghi...")
    if approved_products:
        exporter.export_to_shopify_json(approved_products)
        exporter.export_to_csv(approved_products)

    # FASE 4: Pubblicazione API Diretta
    logger.info("[FASE 4] Pubblicazione API verso lo Store...")
    for prod in approved_products:
        publisher.publish_to_shopify(prod)

    logger.info("==================================================")
    logger.info(f"   CICLO COMPLETATO | Approvati: {len(approved_products)} | Feed & API pronti")
    logger.info("==================================================")

if __name__ == "__main__":
    run_pipeline()
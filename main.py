import sys
from config import config
from logger import get_logger
from trend_analyzer import TrendAnalyzerEngine
from market_validator import MarketValidationEngine, OpportunityMetrics
from content_generator import ContentGeneratorEngine
from database import DatabaseEngine
from store_exporter import StoreExporterEngine

logger = get_logger("AutonomousCore")

def run_pipeline():
    logger.info("==================================================")
    logger.info("  AVVIO CICLO OPERATIVO E-COMMERCE AUTONOMO       ")
    logger.info("==================================================")

    # Inizializzazione motori
    trend_engine = TrendAnalyzerEngine()
    validator_engine = MarketValidationEngine()
    generator_engine = ContentGeneratorEngine()
    db_engine = DatabaseEngine()
    exporter_engine = StoreExporterEngine()

    # 1. Scansione Opportunità
    logger.info("[FASE 1] Estrazione trend di mercato...")
    trends = trend_engine.fetch_trending_opportunities()

    approved_count = 0

    # 2. Screening & Generazione
    logger.info("[FASE 2] Valutazione economico-finanziaria e copywriting...")
    for item in trends:
        if not item.get("is_hot", False):
            continue

        metrics = OpportunityMetrics(
            product_name=item["product_name"],
            selling_price=item["suggested_price"],
            cogs=item["cogs"],
            estimated_shipping_cost=config.DEFAULT_SHIPPING_COST,
            estimated_cac=config.DEFAULT_CAC
        )

        evaluation = validator_engine.evaluate_opportunity(metrics)

        if evaluation["is_viable"]:
            copy = generator_engine.generate_description(
                product_name=evaluation["product_name"],
                category=item.get("category", "Generico")
            )

            evaluation["selling_price"] = item["suggested_price"]
            evaluation["description"] = copy

            db_engine.save_product(evaluation)
            approved_count += 1
            logger.info(f"-> PRODOTTO APPROVATO: {evaluation['product_name']}")
        else:
            logger.warning(f"-> PRODOTTO SCARTATO: {evaluation['product_name']} | Motivi: {evaluation['rejection_reasons']}")

    # 3. Esportazione Feed
    logger.info("[FASE 3] Esportazione automatica cataloghi...")
    json_path = exporter_engine.export_to_json()
    csv_path = exporter_engine.export_to_csv()

    logger.info("==================================================")
    logger.info(f"  CICLO COMPLETATO | Approvati: {approved_count} | Feed pronti")
    logger.info("==================================================")

if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        logger.critical(f"Errore fatale durante l'esecuzione dell'orchestratore: {e}", exc_info=True)
        sys.exit(1)
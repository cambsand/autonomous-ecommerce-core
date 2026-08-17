from logger import get_logger
from trend_analyzer import TrendAnalyzerEngine
from market_validator import MarketValidationEngine, OpportunityMetrics
from content_generator import ContentGeneratorEngine
from database import DatabaseEngine

logger = get_logger("MainPipeline")

logger.info("Avvio della pipeline autonoma e-commerce...")

# Inizializzazione di tutti i motori, incluso il database
trend_engine = TrendAnalyzerEngine()
validator_engine = MarketValidationEngine()
generator_engine = ContentGeneratorEngine()
db_engine = DatabaseEngine()

logger.info("Inizio scansione prodotti di tendenza...")
trends = trend_engine.fetch_trending_opportunities()

winning_products = []

for item in trends:
    if item["is_hot"]:
        logger.info(f"Analisi redditivita per candidato HOT: {item['product_name']}")
        
        metrics = OpportunityMetrics(
            product_name=item["product_name"],
            selling_price=item["suggested_price"],
            cogs=item["cogs"],
            estimated_shipping_cost=5.00,
            estimated_cac=15.00
        )
        
        evaluation = validator_engine.evaluate_opportunity(metrics)
        
        if evaluation["is_viable"]:
            copy = generator_engine.generate_description(
                product_name=evaluation["product_name"], 
                category=item["category"]
            )
            
            evaluation["selling_price"] = item["suggested_price"]
            evaluation["description"] = copy
            
            # Salvataggio automatico su DB SQLite
            db_engine.save_product(evaluation)
            winning_products.append(evaluation)
            
            logger.info(f"PRODOTTO APPROVATO E SALVATO: {evaluation['product_name']} | Margine: {evaluation['net_margin_pct']}% | Profitto: EUR {evaluation['net_profit_per_unit']}")
        else:
            logger.warning(f"PRODOTTO SCARTATO: {evaluation['product_name']} | Motivo: {evaluation['rejection_reasons']}")

logger.info(f"Esecuzione completata. Salvati {len(winning_products)} prodotti idonei nel database.")
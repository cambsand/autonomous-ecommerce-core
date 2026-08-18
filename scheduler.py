import time
from apscheduler.schedulers.background import BackgroundScheduler
from main import run_pipeline
from logger import get_logger

logger = get_logger("SchedulerModule")

def start_automated_pipeline(interval_hours: int = 6):
    """
    Inizializza lo scheduler in background.
    Esegue immediatamente la pipeline e la pianifica a intervalli regolari.
    """
    scheduler = BackgroundScheduler()
    
    # Pianificazione del lavoro
    scheduler.add_job(
        run_pipeline, 
        trigger='interval', 
        hours=interval_hours,
        id='ecommerce_pipeline_job',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info(f"Scheduler attivo: la pipeline eseguira una scansione ogni {interval_hours} ore.")

    # Esecuzione immediata al primo avvio
    logger.info("Esecuzione del primo ciclo di scansione immediato...")
    run_pipeline()

    try:
        # Mantiene attivo il processo principale
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler arrestato correttamente dall'utente.")

if __name__ == "__main__":
    # Configurato per girare ogni 6 ore (modificabile in base alle esigenze)
    start_automated_pipeline(interval_hours=6)
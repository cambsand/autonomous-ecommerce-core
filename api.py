import sqlite3
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from database import DB_PATH
from logger import get_logger
from main import run_pipeline

logger = get_logger("APIModule")

app = FastAPI(
    title="Autonomous E-Commerce Core API",
    description="Dashboard e API per il controllo del sistema autonomo e-commerce",
    version="1.0.0"
)

def get_db_connection():
    if not DB_PATH.exists():
        raise HTTPException(status_code=404, detail="Database non ancora inizializzato.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/products", summary="Lista Prodotti Approvati")
def get_approved_products() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM winning_products ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

@app.get("/api/stats", summary="Statistiche e Metriche")
def get_pipeline_stats():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), AVG(net_margin_pct), SUM(net_profit_per_unit) FROM winning_products")
        count, avg_margin, total_profit = cursor.fetchone()
        return {
            "total_winning_products": count or 0,
            "average_net_margin_pct": round(avg_margin, 2) if avg_margin else 0.0,
            "total_unit_profit_pool": round(total_profit, 2) if total_profit else 0.0
        }

@app.post("/api/run-pipeline", summary="Avvio Manuale Pipeline")
def trigger_pipeline():
    try:
        logger.info("Avvio manuale della pipeline richiesto tramite API.")
        run_pipeline()
        return {"status": "success", "message": "Pipeline eseguita con successo."}
    except Exception as e:
        logger.error(f"Errore durante l'esecuzione API della pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard", response_class=HTMLResponse, summary="Vetrina E-Commerce Dashboard")
def render_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Autonomous E-Commerce Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-slate-100 min-h-screen p-8">
        <div class="max-w-6xl mx-auto">
            <!-- Header -->
            <div class="flex justify-between items-center mb-8 border-b border-slate-800 pb-5">
                <div>
                    <h1 class="text-3xl font-bold text-indigo-400">Autonomous Core</h1>
                    <p class="text-slate-400 text-sm">Dashboard di controllo e vetrina prodotti approvati</p>
                </div>
                <button onclick="runPipeline()" id="runBtn" class="bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-5 py-2.5 rounded-lg shadow-lg transition duration-200">
                    ⚡ Avvia Scansione
                </button>
            </div>

            <!-- Stats Bar -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8" id="statsContainer">
                <div class="bg-slate-800 p-5 rounded-xl border border-slate-700">
                    <p class="text-slate-400 text-xs font-semibold uppercase">Prodotti Approvati</p>
                    <p class="text-3xl font-bold text-white mt-1" id="statCount">-</p>
                </div>
                <div class="bg-slate-800 p-5 rounded-xl border border-slate-700">
                    <p class="text-slate-400 text-xs font-semibold uppercase">Margine Netto Medio</p>
                    <p class="text-3xl font-bold text-emerald-400 mt-1" id="statMargin">-</p>
                </div>
                <div class="bg-slate-800 p-5 rounded-xl border border-slate-700">
                    <p class="text-slate-400 text-xs font-semibold uppercase">Profitto Unitario Accumulato</p>
                    <p class="text-3xl font-bold text-indigo-400 mt-1" id="statProfit">-</p>
                </div>
            </div>

            <!-- Catalog Section -->
            <h2 class="text-xl font-semibold mb-4 text-slate-200">Catalog Winners</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="productsGrid">
                <!-- Cards collegate dinamicamente -->
            </div>
        </div>

        <script>
            async function loadDashboard() {
                // Carica statistiche
                const statsRes = await fetch('/api/stats');
                const stats = await statsRes.json();
                document.getElementById('statCount').innerText = stats.total_winning_products;
                document.getElementById('statMargin').innerText = stats.average_net_margin_pct + '%';
                document.getElementById('statProfit').innerText = '€ ' + stats.total_unit_profit_pool;

                // Carica prodotti
                const prodRes = await fetch('/api/products');
                const products = await prodRes.json();
                const grid = document.getElementById('productsGrid');
                grid.innerHTML = '';

                if (products.length === 0) {
                    grid.innerHTML = '<p class="text-slate-500 col-span-3 text-center py-12">Nessun prodotto approvato a database. Lancia una scansione.</p>';
                    return;
                }

                products.forEach(p => {
                    grid.innerHTML += `
                        <div class="bg-slate-800 rounded-xl p-6 border border-slate-700 flex flex-col justify-between">
                            <div>
                                <div class="flex justify-between items-start mb-3">
                                    <h3 class="font-bold text-lg text-white">${p.product_name}</h3>
                                    <span class="bg-emerald-500/10 text-emerald-400 text-xs font-bold px-2.5 py-1 rounded-full border border-emerald-500/20">
                                        +${p.net_margin_pct}%
                                    </span>
                                </div>
                                <p class="text-slate-300 text-sm mb-4 line-clamp-4 whitespace-pre-line">${p.description || 'Nessuna descrizione'}</p>
                            </div>
                            <div class="pt-4 border-t border-slate-700/60 flex justify-between items-center text-sm">
                                <div>
                                    <span class="text-slate-400 text-xs block">Prezzo Vendita</span>
                                    <span class="font-bold text-white">€ ${p.selling_price}</span>
                                </div>
                                <div class="text-right">
                                    <span class="text-slate-400 text-xs block">Profitto/Unità</span>
                                    <span class="font-bold text-indigo-400">€ ${p.net_profit_per_unit}</span>
                                </div>
                            </div>
                        </div>
                    `;
                });
            }

            async function runPipeline() {
                const btn = document.getElementById('runBtn');
                btn.disabled = true;
                btn.innerText = '⏳ Scansione in corso...';
                try {
                    await fetch('/api/run-pipeline', { method: 'POST' });
                    await loadDashboard();
                } catch (e) {
                    alert('Errore durante l\'esecuzione della pipeline');
                } finally {
                    btn.disabled = false;
                    btn.innerText = '⚡ Avvia Scansione';
                }
            }

            loadDashboard();
        </script>
    </body>
    </html>
    """
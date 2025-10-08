from flask import Flask, render_template, jsonify
import psycopg2
import json
import os
import threading
import time
from datetime import datetime, timedelta
from threading import Semaphore

app = Flask(__name__)

# Límite de conexiones concurrentes para evitar sobrecarga
db_semaphore = Semaphore(3)

# Configuración de PostgreSQL Read DB
def get_read_db_connection():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_READ_HOST', 'postgres_read'),
        database=os.getenv('POSTGRES_READ_DB', 'products_read'),
        user=os.getenv('POSTGRES_READ_USER', 'admin'),
        password=os.getenv('POSTGRES_READ_PASSWORD', 'admin123')
    )

# Cache para datos en tiempo real
dashboard_cache = {
    'stats': {},
    'products': [],
    'metrics': [],
    'last_update': None
}

def update_dashboard_data():
    """Actualizar datos del dashboard cada 10 segundos"""
    while True:
        try:
            with db_semaphore:  # Limitar conexiones concurrentes
                conn = get_read_db_connection()
                cursor = conn.cursor()
            
            # Obtener estadísticas generales
            cursor.execute("SELECT * FROM dashboard_stats")
            stats = cursor.fetchone()
            
            # Obtener productos recientes (limitado a 5 para mejor rendimiento)
            cursor.execute("""
                SELECT id, name, price, stock, created_at 
                FROM products 
                ORDER BY created_at DESC 
                LIMIT 5
            """)
            recent_products = cursor.fetchall()
            
            # Métricas simplificadas (solo para estadísticas básicas)
            metrics = []
            
            # Obtener productos más caros
            cursor.execute("SELECT * FROM expensive_products LIMIT 5")
            expensive_products = cursor.fetchall()
            
            # Obtener datos de stock por producto para la gráfica
            cursor.execute("""
                SELECT name, stock 
                FROM products 
                ORDER BY stock DESC 
                LIMIT 10
            """)
            stock_data = cursor.fetchall()
            
            # Actualizar cache
            dashboard_cache['stats'] = {
                'total_products': stats[0] if stats else 0,
                'avg_price': float(stats[1]) if stats and stats[1] else 0,
                'total_stock': stats[2] if stats else 0,
                'products_in_stock': stats[3] if stats else 0,
                'products_out_of_stock': stats[4] if stats else 0
            }
            
            dashboard_cache['products'] = [
                {
                    'id': row[0],
                    'name': row[1],
                    'price': float(row[2]),
                    'stock': row[3],
                    'created_at': row[4].isoformat() if row[4] else None
                }
                for row in recent_products
            ]
            
            dashboard_cache['metrics'] = []
            
            dashboard_cache['expensive_products'] = [
                {
                    'id': row[0],
                    'name': row[1],
                    'price': float(row[2]),
                    'stock': row[3],
                    'created_at': row[4].isoformat() if row[4] else None
                }
                for row in expensive_products
            ]
            
            dashboard_cache['stock_data'] = [
                {
                    'name': row[0],
                    'stock': row[1]
                }
                for row in stock_data
            ]
            
            dashboard_cache['last_update'] = datetime.now().isoformat()
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error updating dashboard data: {e}")
        
        time.sleep(1)  # Actualizar cada 10 segundos para mejor rendimiento

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    return jsonify(dashboard_cache['stats'])

@app.route('/api/products')
def get_products():
    return jsonify(dashboard_cache['products'])

@app.route('/api/metrics')
def get_metrics():
    return jsonify(dashboard_cache['metrics'])

@app.route('/api/expensive')
def get_expensive():
    return jsonify(dashboard_cache.get('expensive_products', []))

@app.route('/api/stock')
def get_stock_data():
    return jsonify(dashboard_cache.get('stock_data', []))

@app.route('/api/dashboard')
def get_dashboard_data():
    return jsonify(dashboard_cache)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'dashboard'})

if __name__ == '__main__':
    # Iniciar hilo para actualizar datos en tiempo real
    update_thread = threading.Thread(target=update_dashboard_data, daemon=True)
    update_thread.start()
    
    # Configuración optimizada para mejor rendimiento
    app.run(host='0.0.0.0', port=5004, debug=False, threaded=True)

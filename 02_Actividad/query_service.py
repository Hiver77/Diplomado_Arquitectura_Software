from flask import Flask, request, jsonify
import psycopg2
import json
import os

app = Flask(__name__)

# Configuración de PostgreSQL Read DB
def get_read_db_connection():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_READ_HOST', 'postgres_read'),
        database=os.getenv('POSTGRES_READ_DB', 'products_read'),
        user=os.getenv('POSTGRES_READ_USER', 'admin'),
        password=os.getenv('POSTGRES_READ_PASSWORD', 'admin123')
    )

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'query'}), 200

@app.route('/products', methods=['GET'])
def get_all_products():
    try:
        conn = get_read_db_connection()
        cursor = conn.cursor()
        
        # Obtener todos los productos de PostgreSQL
        cursor.execute("""
            SELECT id, name, description, price, stock, created_at, updated_at
            FROM products 
            ORDER BY id
        """)
        
        products = []
        for row in cursor.fetchall():
            products.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'price': float(row[3]),
                'stock': row[4],
                'created_at': row[5].isoformat() if row[5] else None,
                'updated_at': row[6].isoformat() if row[6] else None
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'total': len(products),
            'products': products
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        conn = get_read_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, description, price, stock, created_at, updated_at
            FROM products 
            WHERE id = %s
        """, (product_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return jsonify({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'price': float(row[3]),
                'stock': row[4],
                'created_at': row[5].isoformat() if row[5] else None,
                'updated_at': row[6].isoformat() if row[6] else None
            }), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '').lower()
    
    try:
        conn = get_read_db_connection()
        cursor = conn.cursor()
        
        # Búsqueda en nombre y descripción
        cursor.execute("""
            SELECT id, name, description, price, stock, created_at, updated_at
            FROM products 
            WHERE LOWER(name) LIKE %s OR LOWER(description) LIKE %s
            ORDER BY name
        """, (f'%{query}%', f'%{query}%'))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'price': float(row[3]),
                'stock': row[4],
                'created_at': row[5].isoformat() if row[5] else None,
                'updated_at': row[6].isoformat() if row[6] else None
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'query': query,
            'total': len(results),
            'products': results
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products/stats', methods=['GET'])
def get_product_stats():
    try:
        conn = get_read_db_connection()
        cursor = conn.cursor()
        
        # Obtener estadísticas del dashboard
        cursor.execute("SELECT * FROM dashboard_stats")
        stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if stats:
            return jsonify({
                'total_products': stats[0],
                'avg_price': float(stats[1]) if stats[1] else 0,
                'total_stock': stats[2],
                'products_in_stock': stats[3],
                'products_out_of_stock': stats[4]
            }), 200
        else:
            return jsonify({'error': 'No statistics available'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products/expensive', methods=['GET'])
def get_expensive_products():
    try:
        conn = get_read_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM expensive_products")
        
        products = []
        for row in cursor.fetchall():
            products.append({
                'id': row[0],
                'name': row[1],
                'price': float(row[2]),
                'stock': row[3],
                'created_at': row[4].isoformat() if row[4] else None
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'total': len(products),
            'products': products
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products/recent', methods=['GET'])
def get_recent_products():
    try:
        conn = get_read_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recent_products")
        
        products = []
        for row in cursor.fetchall():
            products.append({
                'id': row[0],
                'name': row[1],
                'price': float(row[2]),
                'stock': row[3],
                'created_at': row[4].isoformat() if row[4] else None
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'total': len(products),
            'products': products
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import time
    time.sleep(10)  # Esperar a que PostgreSQL esté listo
    app.run(host='0.0.0.0', port=5001, debug=True)
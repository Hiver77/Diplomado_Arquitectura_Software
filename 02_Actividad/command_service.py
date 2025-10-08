from flask import Flask, request, jsonify
import psycopg2
import pika
import json
import os

app = Flask(__name__)

# Configuración de PostgreSQL (Write DB)
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'postgres_write'),
        database=os.getenv('POSTGRES_DB', 'products_write'),
        user=os.getenv('POSTGRES_USER', 'admin'),
        password=os.getenv('POSTGRES_PASSWORD', 'admin123')
    )

# Publicar evento en RabbitMQ
def publish_event(event_type, data):
    try:
        credentials = pika.PlainCredentials('admin', 'admin123')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.getenv('RABBITMQ_HOST', 'rabbitmq'),
                credentials=credentials
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue='product_events', durable=True)
        
        event = {
            'event_type': event_type,
            'data': data
        }
        
        channel.basic_publish(
            exchange='',
            routing_key='product_events',
            body=json.dumps(event),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
    except Exception as e:
        print(f"Error publishing event: {e}")

# Inicializar base de datos
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            stock INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'command'}), 200

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    
    # Validaciones
    if not data.get('name') or not data.get('price'):
        return jsonify({'error': 'Name and price are required'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            'INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s) RETURNING id',
            (data['name'], data.get('description', ''), data['price'], data.get('stock', 0))
        )
        product_id = cur.fetchone()[0]
        conn.commit()
        
        # Publicar evento
        product_data = {
            'id': product_id,
            'name': data['name'],
            'description': data.get('description', ''),
            'price': float(data['price']),
            'stock': data.get('stock', 0)
        }
        publish_event('product_created', product_data)
        
        return jsonify({'id': product_id, 'message': 'Product created'}), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            'UPDATE products SET name=%s, description=%s, price=%s, stock=%s WHERE id=%s',
            (data['name'], data.get('description', ''), data['price'], data.get('stock', 0), product_id)
        )
        conn.commit()
        
        if cur.rowcount > 0:
            product_data = {
                'id': product_id,
                'name': data['name'],
                'description': data.get('description', ''),
                'price': float(data['price']),
                'stock': data.get('stock', 0)
            }
            publish_event('product_updated', product_data)
            return jsonify({'message': 'Product updated'}), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
            
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    import time
    time.sleep(10)  # Esperar a que los servicios estén listos
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
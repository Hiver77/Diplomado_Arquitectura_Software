import pika
import json
import psycopg2
import os
import time

# Configuración de PostgreSQL Read DB
def get_read_db_connection():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_READ_HOST', 'postgres_read'),
        database=os.getenv('POSTGRES_READ_DB', 'products_read'),
        user=os.getenv('POSTGRES_READ_USER', 'admin'),
        password=os.getenv('POSTGRES_READ_PASSWORD', 'admin123')
    )

def process_event(ch, method, properties, body):
    try:
        event = json.loads(body)
        event_type = event['event_type']
        data = event['data']
        
        print(f"Processing event: {event_type} for product {data['id']}")
        
        conn = get_read_db_connection()
        cursor = conn.cursor()
        
        if event_type == 'product_created':
            # Insertar nuevo producto en la base de lectura
            cursor.execute("""
                INSERT INTO products (id, name, description, price, stock, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description,
                    price = EXCLUDED.price,
                    stock = EXCLUDED.stock,
                    updated_at = EXCLUDED.updated_at
            """, (
                data['id'],
                data['name'],
                data['description'],
                data['price'],
                data['stock'],
                data.get('created_at'),
                data.get('updated_at')
            ))
            print(f"Product {data['id']} created in read database")
            
        elif event_type == 'product_updated':
            # Actualizar producto existente
            cursor.execute("""
                UPDATE products 
                SET name = %s, description = %s, price = %s, stock = %s, updated_at = %s
                WHERE id = %s
            """, (
                data['name'],
                data['description'],
                data['price'],
                data['stock'],
                data.get('updated_at'),
                data['id']
            ))
            print(f"Product {data['id']} updated in read database")
            
        elif event_type == 'product_deleted':
            # Eliminar producto
            cursor.execute("DELETE FROM products WHERE id = %s", (data['id'],))
            print(f"Product {data['id']} deleted from read database")
        
        # Registrar métrica del evento
        cursor.execute("""
            INSERT INTO product_metrics (product_id, metric_type, metric_value)
            VALUES (%s, %s, %s)
        """, (data['id'], event_type, 1))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Confirmar procesamiento
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"Error processing event: {e}")
        # No hacer ack para reintentar
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    print("Event Handler starting...")
    time.sleep(15)  # Esperar a que RabbitMQ esté listo
    
    # Conectar a RabbitMQ
    credentials = pika.PlainCredentials('admin', 'admin123')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST', 'rabbitmq'),
            credentials=credentials
        )
    )
    channel = connection.channel()
    
    # Declarar la cola
    channel.queue_declare(queue='product_events', durable=True)
    
    # Configurar consumidor
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='product_events',
        on_message_callback=process_event
    )
    
    print("Event Handler ready. Waiting for events...")
    channel.start_consuming()

if __name__ == '__main__':
    main()
-- Script de inicialización para la base de datos de lectura
-- Esta base de datos se sincroniza con la base de escritura a través de eventos

-- Crear tabla de productos para lectura
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para optimizar consultas de lectura
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);
CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at);

-- Crear tabla de métricas para el dashboard
CREATE TABLE IF NOT EXISTS product_metrics (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    metric_type VARCHAR(50) NOT NULL, -- 'view', 'search', 'purchase', etc.
    metric_value DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para métricas
CREATE INDEX IF NOT EXISTS idx_metrics_product_id ON product_metrics(product_id);
CREATE INDEX IF NOT EXISTS idx_metrics_type ON product_metrics(metric_type);
CREATE INDEX IF NOT EXISTS idx_metrics_created_at ON product_metrics(created_at);

-- Crear vista para estadísticas del dashboard
CREATE OR REPLACE VIEW dashboard_stats AS
SELECT 
    COUNT(*) as total_products,
    AVG(price) as avg_price,
    SUM(stock) as total_stock,
    COUNT(CASE WHEN stock > 0 THEN 1 END) as products_in_stock,
    COUNT(CASE WHEN stock = 0 THEN 1 END) as products_out_of_stock
FROM products;

-- Crear vista para productos más caros
CREATE OR REPLACE VIEW expensive_products AS
SELECT 
    id,
    name,
    price,
    stock,
    created_at
FROM products 
WHERE price > (SELECT AVG(price) FROM products)
ORDER BY price DESC;

-- Crear vista para productos recientes
CREATE OR REPLACE VIEW recent_products AS
SELECT 
    id,
    name,
    price,
    stock,
    created_at
FROM products 
WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY created_at DESC;

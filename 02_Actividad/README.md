# CQRS Pattern - Sistema de Productos E-commerce con PostgreSQL y Dashboard

## 📋 Arquitectura

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Cliente   │──────▶│   Command    │──────▶│ PostgreSQL  │
│             │ POST  │   Service    │ Write │  (Write DB) │
└─────────────┘       └──────┬───────┘       └─────────────┘
                             │
                             │ Event
                             ▼
                      ┌─────────────┐
                      │  RabbitMQ   │
                      └──────┬──────┘
                             │
                             │ Subscribe
                             ▼
┌─────────────┐       ┌──────────────┐      ┌─────────────┐
│   Cliente   │◀──────│    Query     │◀─────│ PostgreSQL  │
│             │  GET  │   Service    │ Read │  (Read DB)  │
└─────────────┘       └──────────────┘      └─────────────┘
                             ▲
                             │ Sync
                      ┌──────┴──────┐
                      │   Event     │
                      │   Handler   │
                      └─────────────┘
                             │
                             ▼
                      ┌─────────────┐
                      │  Dashboard  │
                      │  (Puerto    │
                      │   5004)     │
                      └─────────────┘
```

## 🚀 Componentes

1. **Command Service** (Puerto 5005): Maneja escrituras (CREATE, UPDATE)
2. **Query Service** (Puerto 5006): Maneja lecturas (GET, SEARCH) desde PostgreSQL Read
3. **Dashboard Server** (Puerto 5007): Gráficos en tiempo real
4. **Event Handler**: Sincroniza datos entre bases de datos
5. **PostgreSQL Write**: Base de datos transaccional para escrituras (Puerto 5434)
6. **PostgreSQL Read**: Base de datos optimizada para lecturas (Puerto 5435)
7. **RabbitMQ**: Message broker para eventos (Puertos 5673, 15673)

## 📦 Instalación

### Estructura de archivos requerida:

```
cqrs-postgrest-demo/
├── command_service.py
├── query_service.py
├── event_handler.py
├── dashboard_server.py
├── docker-compose.yml
├── Dockerfile.command
├── Dockerfile.query
├── Dockerfile.handler
├── Dockerfile.dashboard
├── Dockerfile.read_db
├── init_read_db.sql
└── templates/
    └── dashboard.html
```

### Iniciar el sistema:

```bash
docker compose up --build
```

Espera 20-30 segundos para que todos los servicios estén listos.

## 🧪 Pruebas

### 1. Crear un producto (Command)

```bash
curl -X POST http://localhost:5005/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop HP",
    "description": "Laptop 16GB RAM, 512GB SSD",
    "price": 899.99,
    "stock": 15
  }'
```

### 2. Crear más productos

```bash
curl -X POST http://localhost:5005/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mouse Logitech",
    "description": "Mouse inalámbrico ergonómico",
    "price": 29.99,
    "stock": 50
  }'

curl -X POST http://localhost:5005/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Teclado Mecánico",
    "description": "Teclado RGB con switches azules",
    "price": 79.99,
    "stock": 30
  }'
```

### 3. Listar todos los productos (Query)

```bash
curl http://localhost:5006/products
```

### 4. Buscar un producto específico

```bash
curl http://localhost:5006/products/1
```

### 5. Buscar productos (Query optimizado)

```bash
curl "http://localhost:5006/products/search?q=laptop"
```

### 6. Obtener estadísticas

```bash
curl http://localhost:5006/products/stats
```

### 7. Productos más caros

```bash
curl http://localhost:5006/products/expensive
```

### 8. Productos recientes

```bash
curl http://localhost:5006/products/recent
```

### 9. Actualizar un producto

```bash
curl -X PUT http://localhost:5005/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop HP Actualizada",
    "description": "Laptop 32GB RAM, 1TB SSD",
    "price": 1299.99,
    "stock": 10
  }'
```

### 10. Verificar la actualización

```bash
curl http://localhost:5006/products/1
```

## 📊 Dashboard en Tiempo Real

### Acceder al Dashboard:

```
URL: http://localhost:5007
```

### Características del Dashboard:

- **Estadísticas en Tiempo Real**: Total de productos, precio promedio, stock total
- **Gráficos Interactivos**: Distribución de stock, métricas por día
- **Tabla de Productos**: Productos recientes con información detallada
- **Actualización Automática**: Los datos se actualizan cada 5 segundos
- **Indicador de Estado**: Muestra el estado de conexión y última actualización

### API del Dashboard:

```bash
# Datos completos del dashboard
curl http://localhost:5007/api/dashboard

# Solo estadísticas
curl http://localhost:5007/api/stats

# Solo productos
curl http://localhost:5007/api/products

# Solo métricas
curl http://localhost:5007/api/metrics

# Productos más caros
curl http://localhost:5007/api/expensive
```

## 🔍 Monitoreo

### Ver logs del Event Handler:

```bash
docker compose logs -f event_handler
```

### Acceder a RabbitMQ Management:

```
URL: http://localhost:15673
Usuario: admin
Password: admin123
```

### Verificar PostgreSQL Write:

```bash
docker exec -it poc_cqrs_postgrest-postgres_write-1 psql -U admin -d products_write
> \dt
> SELECT * FROM products;
```

### Verificar PostgreSQL Read:

```bash
docker exec -it poc_cqrs_postgrest-postgres_read-1 psql -U admin -d products_read
> \dt
> SELECT * FROM products;
> SELECT * FROM dashboard_stats;
```

## ✅ Ventajas del CQRS con PostgreSQL

1. **Bases de datos optimizadas**:
   - PostgreSQL Write: Transacciones ACID para escrituras
   - PostgreSQL Read: Consultas optimizadas para lecturas con índices específicos

2. **Escalabilidad independiente**:
   - Puedes escalar el Query Service sin afectar Commands
   - En e-commerce real, las lecturas son 100x más que escrituras

3. **Desacoplamiento**:
   - Los servicios se comunican vía eventos
   - Fácil agregar nuevos consumidores (ej: servicio de analytics)

4. **Rendimiento**:
   - Las consultas en PostgreSQL Read son optimizadas para lectura
   - Las escrituras mantienen integridad sin sacrificar velocidad de lectura

5. **Dashboard en Tiempo Real**:
   - Visualización inmediata de cambios
   - Métricas y estadísticas actualizadas automáticamente
   - Gráficos interactivos para análisis de datos

## 🛑 Detener el sistema

```bash
docker compose down
```

Para eliminar también los datos:

```bash
docker compose down -v
```

## 🎯 Casos de uso reales para CQRS con Dashboard

- **E-commerce**: Gestión de productos con dashboard de ventas
- **Banking**: Transacciones vs consultas de saldo con métricas financieras
- **Redes sociales**: Posts vs feed de lectura con analytics de engagement
- **Sistemas de reservas**: Booking vs disponibilidad con dashboard de ocupación
- **Analytics dashboards**: Escritura de métricas vs visualización en tiempo real

## 🔧 Configuración Avanzada

### Variables de Entorno:

```bash
# PostgreSQL Write
POSTGRES_HOST=postgres_write
POSTGRES_DB=products_write
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123

# PostgreSQL Read
POSTGRES_READ_HOST=postgres_read
POSTGRES_READ_DB=products_read
POSTGRES_READ_USER=admin
POSTGRES_READ_PASSWORD=admin123

# RabbitMQ
RABBITMQ_HOST=rabbitmq
```

### Puertos:

- **Command Service**: 5005
- **Query Service**: 5006
- **Dashboard Server**: 5007
- **PostgreSQL Write**: 5434
- **PostgreSQL Read**: 5435
- **RabbitMQ**: 5673, 15673
# Data Engine Synonym System

A FastAPI-based caching system for synonym data retrieval with support for both Redis and in-memory caching strategies.

## Features

- **Dual Caching Strategies**: Switch between Redis (distributed) and in-memory caching
- **Thread-Safe Operations**: Proper locking and atomic operations for concurrent requests
- **Connection Pooling**: Optimized database access with configurable pool sizes
- **Cache Metadata**: Every response includes information about cache hits/misses
- **Performance Monitoring**: Built-in timing metrics and colored logging
- **Auto-Expiration**: Configurable TTL with automatic cache invalidation

## Prerequisites

- Docker and Docker Compose
- Git

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Data-Engine-Synonym-System
```

## Running the Application

Start all services:

```bash
docker-compose up -d
```

The application will be available at:

- API: `http://localhost:8000`
- Streamlit Dashboard: `http://localhost:8501`

Wait about 60 seconds for SQL Server to initialize and the database to be created.

## Streamlit Dashboard

The Streamlit frontend provides an interactive interface to:

- View current cache configuration
- Fetch synonym data with real-time performance metrics
- See cache hit/miss status with color indicators
- Monitor cache expiration with countdown timer
- Search and filter synonym records

## API Endpoints

- `GET /` - Health check
- `GET /api/info` - Get current cache configuration
- `GET /api/synonyms` - Retrieve all synonym records

## Running Tests

Tests run inside the Docker container to access the ODBC driver:

```bash
docker-compose exec app pytest -v
```

Test logs are saved to `tests/test_logs.log`

## Configuration

Cache strategy and TTL are configured in `docker-compose.yml`:

- `CACHE_STRATEGY` - Either `redis` or `memory`
- `CACHE_TTL` - Time to live in seconds

## Stopping the Application

```bash
docker-compose down
```

To remove volumes as well:

```bash
docker-compose down -v
```

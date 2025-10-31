# Data Engine Synonym System

A FastAPI-based caching system for synonym data retrieval with support for both Redis and in-memory caching strategies.

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

The application will be available at `http://localhost:8000`

Wait about 60 seconds for SQL Server to initialize and the database to be created.

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

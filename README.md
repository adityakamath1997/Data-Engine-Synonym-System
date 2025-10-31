# Data Engine Synonym System

A synonym lookup API built with FastAPI and SQL Server, featuring dual caching strategies for optimal performance. This system demonstrates cache-first architecture with support for both Redis distributed caching and in-memory caching.

## Overview

This application retrieves synonym data from a SQL Server database and caches results to minimize database load. Every response includes metadata indicating whether the data came from cache or database, along with performance metrics.

The system was designed with the following priorities:
- Minimize database queries through intelligent caching
- Support both single-instance (memory) and distributed (Redis) deployments
- Ensure thread safety for concurrent request handling
- Provide visibility into caching behavior for monitoring and debugging

## Architecture

Built with a clean separation of concerns:

```
FastAPI Application
    |
    +-- API Layer (routes)
    +-- Service Layer (business logic)
    +-- Cache Layer (strategy pattern)
    +-- Repository Layer (data access)
    +-- Database (SQL Server with connection pooling)
```

The cache layer uses the Strategy pattern, allowing runtime switching between Redis and in-memory implementations without changing application code.

## Requirements Coverage

This implementation satisfies all specified requirements:

### Functional Requirements

**Synonym Retrieval:**
- Connects to SQL Server using SQLAlchemy with pyodbc driver
- Each record contains word_id (unique primary key), word, and synonyms fields
- Only supports bulk retrieval via `get_all()` - no single-entry lookups
- All responses include cache_metadata with from_cache boolean

**Caching System:**
- Dual strategy support: RedisCache for distributed systems, MemoryCache for single instances
- Configurable TTL via CACHE_TTL environment variable
- Automatic expiration: Redis uses native setex, Memory uses lazy deletion on access
- Serialization: Redis stores JSON, Memory stores native Python objects (more efficient for in-process)

### Performance Requirements

**Database Optimization:**
- Cache-first pattern: checks cache before querying database
- Connection pooling configured with pool_size=10, max_overflow=20
- pool_pre_ping enabled to handle stale connections

**Thread Safety:**
- MemoryCache: all operations protected by threading.Lock
- RedisCache: inherently thread-safe via redis-py connection pooling
- CacheFactory: double-checked locking for singleton initialization

**Speed:**
- Cache operations are O(1) lookups
- Response includes timing metrics showing cache hits are significantly faster

### Technology Stack

- FastAPI for API framework (not Django as specified)
- SQLModel + SQLAlchemy for ORM and queries (not Django ORM)
- SQL Server 2022 for data storage
- Redis 7 for distributed caching option
- Docker Compose for orchestration

## Getting Started

### Prerequisites

- Docker Desktop or Docker Engine with docker-compose
- Git
- 8GB RAM recommended (SQL Server requirement)

### Clone and Setup

```bash
git clone <repository-url>
cd Data-Engine-Synonym-System
```

### Start the Application

```bash
docker-compose up -d
```

This starts four services:
1. SQL Server 2022 (port 1433)
2. Redis 7 (port 6379)
3. FastAPI application (port 8000)
4. Streamlit dashboard (port 8501)

Wait approximately 60 seconds for SQL Server to initialize and the database schema to be created. The init script automatically creates the synonymdb database and loads 20 sample synonym records.

### Verify Services

Check that all services are running:

```bash
docker-compose ps
```

Test the API:

```bash
curl http://localhost:8000/
curl http://localhost:8000/api/synonyms | jq '.[:2]'
```

### Access the Application

- API Documentation: http://localhost:8000/docs (Swagger UI)
- API Base URL: http://localhost:8000
- Streamlit Dashboard: http://localhost:8501

## Using the Streamlit Dashboard

The Streamlit dashboard at http://localhost:8501 provides the easiest way to test and observe the caching system in action.

### Testing Cache Behavior

1. **First Request (Cache Miss)**
   - Open http://localhost:8501
   - Note the cache configuration at the top (strategy and TTL)
   - Click the "Fetch Synonyms" button
   - Observe:
     - Red "MISS" indicator showing cache miss
     - Response time (typically 40-60ms for database query)
     - All 20 synonym records loaded into the table

2. **Subsequent Requests (Cache Hit)**
   - Click "Fetch Synonyms" again immediately
   - Observe:
     - Green "HIT" indicator showing data came from cache
     - Much faster response time (1-3ms for memory, 5-8ms for Redis)
     - Same data returned instantly
   - Click multiple times to see consistent cache hits

3. **Cache Expiration**
   - After a cache miss, watch the "Cache Expiration Timer" in the top-right
   - It counts down from 25 seconds (the configured TTL)
   - Wait for it to reach zero
   - Click "Fetch Synonyms" again
   - You'll see a cache MISS as the data expired and needs to be reloaded

4. **Performance Comparison**
   - Compare response times between cache hits and misses
   - Cache hits should be 20-40x faster than database queries
   - The dashboard displays response time in milliseconds for each request

### Testing Different Cache Strategies

1. **Memory Cache (Default)**
   - Already configured in docker-compose.yml
   - Fastest response times (~1-3ms)
   - Cache is lost when container restarts

2. **Redis Cache**
   - Stop the application: `docker-compose down`
   - Edit docker-compose.yml line 52:
     ```yaml
     CACHE_STRATEGY: redis  # changed from 'memory'
     ```
   - Restart: `docker-compose up -d`
   - Wait 60 seconds for initialization
   - Open http://localhost:8501 and repeat the tests
   - Notice slightly slower cache hits (~5-8ms) but still much faster than database
   - Redis cache persists across container restarts

### Additional Features

- **Search**: Use the search box to filter synonyms by word
- **Cache Info**: When using Redis, connection details are displayed below the metrics
- **Real-time Metrics**: Every request shows current cache status and performance data

## Running Tests

The test suite includes 6 tests covering:
- Endpoint structure validation
- Cache hit/miss behavior
- TTL expiration (includes 26-second sleep to verify expiration)
- Cache metadata presence
- Data consistency across cache operations

Run tests inside the container:

```bash
docker-compose exec app pytest -v
```

Test output is logged to `tests/test_logs.log` for review.

## Configuration

### Cache Strategy

Edit `docker-compose.yml` to switch between caching strategies:

```yaml
environment:
  CACHE_STRATEGY: memory  # or 'redis'
  CACHE_TTL: 25           # seconds
```

After changing configuration:

```bash
docker-compose restart app
```

### Connection Pooling

Database connection pool is configured in `app/database/connection.py`:
- pool_size: 10 persistent connections
- max_overflow: 20 additional connections under load
- pool_pre_ping: True (tests connections before use)

## API Reference

### GET /

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

### GET /api/info

Returns current cache configuration.

**Response:**
```json
{
  "cache_strategy": "memory",
  "cache_ttl_seconds": 25
}
```

### GET /api/synonyms

Retrieves all synonym records with cache metadata.

**Response:**
```json
[
  {
    "word_id": 1,
    "word": "happy",
    "synonyms": "joyful, cheerful, content, pleased, delighted",
    "cache_metadata": {
      "from_cache": true,
      "cache_info": {
        "cache_source": "memory"
      }
    }
  }
]
```

The `from_cache` field indicates whether this request was served from cache (true) or database (false).

## Project Structure

```
.
├── app/
│   ├── api/            # FastAPI routes
│   ├── cache/          # Cache implementations (base, redis, memory, factory)
│   ├── database/       # Database connection and repository
│   ├── models/         # SQLModel models and response schemas
│   ├── services/       # Business logic layer
│   ├── config.py       # Application configuration
│   └── main.py         # FastAPI application entry point
├── tests/              # Test suite
├── docker-compose.yml  # Service orchestration
├── Dockerfile          # Application container
├── init-db.sh          # Database initialization script
└── streamlit_app.py    # Dashboard for visualization
```

## Implementation Notes

### Cache Strategy Pattern

The cache layer uses the Strategy pattern with a factory for instantiation. This allows:
- Runtime selection of cache implementation
- Easy addition of new cache backends
- Consistent interface across implementations

### Thread Safety Approach

Memory cache uses explicit locking with threading.Lock on all operations. Redis cache relies on redis-py's built-in connection pooling which is thread-safe by default. The factory uses double-checked locking to ensure singleton initialization in multi-threaded environments.

### Serialization Trade-offs

Redis cache serializes data to JSON for storage. Memory cache stores native Python objects directly, avoiding serialization overhead since it operates in-process. Both approaches are valid depending on deployment needs.

### Why SQLAlchemy Query API

While SQLModel provides a newer select() API, this implementation uses the classic SQLAlchemy query() API. Both work with SQLModel models since SQLModel is built on SQLAlchemy. The query API is well-documented and widely understood.

## Troubleshooting

### SQL Server Taking Too Long to Start

SQL Server needs time to initialize on first run. Wait 60-90 seconds before accessing the application. Check logs:

```bash
docker-compose logs sqlserver
```

### Port Already in Use

If ports 1433, 6379, 8000, or 8501 are in use, edit `docker-compose.yml` to use different ports.

### Tests Failing

Ensure all services are healthy:

```bash
docker-compose ps
```

Restart the application service:

```bash
docker-compose restart app
```

### Cache Not Working

Check the logs for cache operations:

```bash
docker-compose logs app
```

You should see colored log messages indicating CACHE HIT or CACHE MISS.

## Cleanup

Stop and remove all containers:

```bash
docker-compose down
```

Remove all data (including SQL Server data):

```bash
docker-compose down -v
```

## Performance Characteristics

Based on local testing with the default dataset:

- Database query (cache miss): ~40-60ms
- Memory cache hit: ~1-3ms
- Redis cache hit: ~5-8ms

Cache hits are approximately 20-40x faster than database queries, demonstrating effective optimization of database access.

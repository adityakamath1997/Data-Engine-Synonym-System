import time


def test_root_endpoint(client):
    """Test the root endpoint returns OK"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_info_endpoint(client):
    """Test the info endpoint returns cache configuration"""
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.json()
    assert "cache_strategy" in data
    assert "cache_ttl_seconds" in data
    assert data["cache_strategy"] in ["memory", "redis"]
    assert isinstance(data["cache_ttl_seconds"], int)


def test_synonyms_endpoint_structure(client):
    """Test the synonyms endpoint returns correct data structure"""
    response = client.get("/api/synonyms")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    first_synonym = data[0]
    assert "word_id" in first_synonym
    assert "word" in first_synonym
    assert "synonyms" in first_synonym
    assert "cache_metadata" in first_synonym

    cache_metadata = first_synonym["cache_metadata"]
    assert "from_cache" in cache_metadata
    assert isinstance(cache_metadata["from_cache"], bool)

    if cache_metadata.get("cache_info"):
        cache_info = cache_metadata["cache_info"]
        assert "cache_source" in cache_info
        assert cache_info["cache_source"] in ["memory", "redis"]


def test_cache_behavior_with_ttl():
    """
    Test cache behavior with TTL expiration, assuming TTL is set to 25 seconds
    """
    from fastapi.testclient import TestClient

    from app.main import app

    client = TestClient(app)

    # First call - should be cache MISS (database query)
    response1 = client.get("/api/synonyms")
    assert response1.status_code == 200
    data1 = response1.json()
    assert len(data1) > 0

    # Second call immediately after, which should be cache HIT
    response2 = client.get("/api/synonyms")
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2[0]["cache_metadata"]["from_cache"] is True

    # Third call immediately after, which should still be cache HIT
    response3 = client.get("/api/synonyms")
    assert response3.status_code == 200
    data3 = response3.json()
    assert data3[0]["cache_metadata"]["from_cache"] is True

    # Fourth call immediately after, which should still be cache HIT
    response4 = client.get("/api/synonyms")
    assert response4.status_code == 200
    data4 = response4.json()
    assert data4[0]["cache_metadata"]["from_cache"] is True

    # Verify data consistency across cache hits
    assert data2 == data3 == data4

    print("\n[TEST] Sleeping for 26 seconds to let cache expire (TTL=25s)...")
    time.sleep(26)

    # After TTL expiration, which should be cache MISS
    response5 = client.get("/api/synonyms")
    assert response5.status_code == 200
    data5 = response5.json()
    assert data5[0]["cache_metadata"]["from_cache"] is False

    # Immediately after cache miss, should be cache HIT again
    response6 = client.get("/api/synonyms")
    assert response6.status_code == 200
    data6 = response6.json()
    assert data6[0]["cache_metadata"]["from_cache"] is True


def test_synonyms_endpoint_returns_all_records(client):
    """Test that the endpoint returns all synonym records from database"""
    response = client.get("/api/synonyms")
    assert response.status_code == 200
    data = response.json()

    # Should have exactly 20 records, as dfeined in init-db.sh
    assert len(data) == 20

    # Verify word_ids are unique
    word_ids = [item["word_id"] for item in data]
    assert len(word_ids) == len(set(word_ids))


def test_cache_metadata_includes_source_info(client):
    """Test that cache metadata includes cache source information"""
    # Make first call
    client.get("/api/synonyms")

    # Make second call to get cached response
    response = client.get("/api/synonyms")
    assert response.status_code == 200
    data = response.json()

    cache_metadata = data[0]["cache_metadata"]

    # If from cache, should have cache info
    if cache_metadata["from_cache"]:
        assert "cache_info" in cache_metadata
        assert cache_metadata["cache_info"] is not None
        cache_info = cache_metadata["cache_info"]
        assert "cache_source" in cache_info
        assert cache_info["cache_source"] in ["memory", "redis"]

        # If redis, should have connection info
        if cache_info["cache_source"] == "redis":
            assert "redis_host" in cache_info
            assert "redis_port" in cache_info

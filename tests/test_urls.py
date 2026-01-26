from app.main import app


def test_shorten_validity(client):
    res = client.post(
        "/shorten", json={"original_url": "https://github.com/Venkateshkamat"}
    )
    assert res.status_code == 200
    assert "short_code" in res.json()


def test_shorten_invalid_url(client):
    res = client.post("/shorten", json={"original_url": "not-a-valid-url"})
    assert res.status_code == 422


def test_shorten_missing_original_url(client):
    res = client.post("/shorten", json={})
    assert res.status_code == 422


def test_shorten_short_code_format(client):
    res = client.post("/shorten", json={"original_url": "https://example.com"})
    assert res.status_code == 200
    short_code = res.json()["short_code"]
    assert len(short_code) == 6
    assert short_code.isalnum()

def test_stats_success(client):
    create  = client.post('/shorten', json={"original_url":"https://example.com/page"})
    assert create.status_code == 200
    short_code = create.json()['short_code']

    res = client.get(f'/stats/{short_code}')
    assert res.status_code == 200
    data = res.json()
    assert data["original_url"] == "https://example.com/page"
    assert data["short_code"] == short_code
    assert data["clicks"] == 0
    assert "created_at" in data
    assert "id" in data

def test_stats_not_found(client):
    res = client.get("/stats/nonexistent")
    assert res.status_code == 404
    assert "URL not found" in res.json()["detail"]
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_shorten():
    res = client.post("/shorten",json = {"original_url":"https://github.com/Venkateshkamat"})
    assert res.status_code == 200
    assert "short_code" in res.json()
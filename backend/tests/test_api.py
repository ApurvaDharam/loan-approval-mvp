from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    res = client.get('/health')
    assert res.status_code == 200
    assert 'status' in res.json()

# prediction test is skipped here because model may not exist in CI environment

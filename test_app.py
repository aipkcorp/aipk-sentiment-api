from app import app
import json

def test_analyze():
    with app.test_client() as client:
        response = client.post('/analyze', json={"text": "너무 힘들어"})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "score" in data
        assert "sentiment" in data

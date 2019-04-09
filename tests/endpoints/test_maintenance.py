def test_ping(client):
    response = client.get('api/maintanance/ping')
    assert response.status_code == 200
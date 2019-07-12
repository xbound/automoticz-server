def test_ping(client):
    response = client.get('api/system/ping')
    assert response.status_code == 200

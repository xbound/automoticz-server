def test_registration(app, client, database):
    response = client.post(
        '/api/auth/login',
        json={
            'username': 'user1'
        })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['access_token']
    assert json_data['refresh_token']


def test_login(app, client, database):
    response = client.post(
        '/api/auth/login',
        json={
            'username': 'user1'
        })
    response = client.post(
        '/api/auth/login',
        json={
            'username': 'user1'
        })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'LOGIN'


def test_refresh(app, client):
    response = client.post(
        '/api/auth/login',
        json={
            'username': 'user1'
        })
    json_data = response.get_json()
    access_token = json_data['access_token']
    refresh_token = json_data['refresh_token']
    response = client.post(
        '/api/auth/refresh', json={
            'refresh_token': refresh_token,
        })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['access_token'] != access_token


def test_revoke_access(client):
    username = 'user1'
    response = client.post(
        '/api/auth/login',
        json={
            'username': username
        })
    json_data = response.get_json()
    access_token = json_data['access_token']
    response = client.post(
        '/api/auth/revoke_access', json={
            'access_token': access_token,
        })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['username'] == username

def test_revoke_refresh(client):
    username = 'user1'
    response = client.post(
        '/api/auth/login',
        json={
            'username': username
        })
    json_data = response.get_json()
    refresh_token = json_data['refresh_token']
    response = client.post(
        '/api/auth/revoke_refresh', json={
            'refresh_token': refresh_token,
        })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['username'] == username
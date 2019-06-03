from automoticz.extensions import socketio

def test_ws(app):
    client = socketio.test_client(app)
    assert client.is_connected()

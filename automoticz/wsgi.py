from automoticz.app import create_app
from gevent.pywsgi import WSGIServer

app = create_app()

server = WSGIServer((app.config.SERVER_HOST, app.config.SERVER_PORT), app)

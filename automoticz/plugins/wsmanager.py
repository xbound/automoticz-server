from websocket import create_connection, WebSocket
from sqlalchemy.orm.exc import NoResultFound

from automoticz.extensions import db
from automoticz.utils import to_json
from automoticz.models import WSDevice

class WsDeviceWrapper:

    __devices__ = []

    def __init__(self, device: WSDevice, url ,query_types):
        self._name = device.name
        self._set_query_types(query_types)
        self._url = url


    @property
    def socket(self) -> WebSocket:
        return self._socket

    @property
    def name(self) -> str:
        return self._name

    def _set_query_types(self, query_types):
        self._query_types = {}
        if not query_types:
            raise ValueError('No query types set for device')
        for query in query_types:
            key = query.get('key')
            params = query.get('params')
            self._query_types[key] = params

    def _connect(self):
        try:
            self._socket = create_connection(
                self._url,
                timeout=20,
            )
        except:
            self._socket = None

    def is_connected(self):
        if hasattr(self, '_socket'):
            if self._socket:
                return self._socket.connected
        return False
    
    def _close(self):
        if self.is_connected():
            self._socket.close()

    def send_query(self, query_type: str):
        while not self.is_connected():
            self._connect()
        params = self._query_types[query_type]
        recv = None
        while not recv:
            try:
                self._socket.send(to_json(params))
                recv = self._socket.recv()
            except Exception as e:
                recv  = None
        return str(recv)
        


class WSManager:
    '''
    Extension for managing Websocket connections
    '''

    __devices__ = {}

    def __init__(self, app=None):
        '''
        Extension initialization
        '''
        if app:
            self.init_app(app)

    def get_device(self, name) -> WsDeviceWrapper:
        return self.__devices__.get(name)

    def get_device_db_instance(self, name) -> WSDevice:
        wsdevice = None
        wsdevice = WSDevice.query.filter_by(name=name).first()
        return wsdevice

    def get_devices(self):
        return self.__devices__

    def init_app(self, app):
        '''
        App initialization
        '''
        self.app = app
        devices_list = app.config.WS_DEVICES
        for device in devices_list:
            wsdevice = self.make_device(device)
            query_types = device.get('queries')
            url = device.get('url')
            wrapper = WsDeviceWrapper(wsdevice, url, query_types)
            WSManager.__devices__[wsdevice.name] = wrapper
        self.app.extensions['wsmanager'] = self

    def make_device(self, device: dict) -> WSDevice:
        name = device['name']
        wsdevice = None
        with self.app.app_context():
            wsdevice = WSDevice.query.filter_by(name=name).first()
            if not wsdevice:
                wsdevice = WSDevice(name=name)
                db.session.add(wsdevice)
                db.session.commit()
        return wsdevice
        




        
        

    

from automoticz.extensions import celery_app
from automoticz.utils import get_used_devices, get_users


@celery_app.task(bind=True)
def fetch_devices_usage_map(self):
    ''' 
    Fetch all devices registered on Domoticz server.
    '''
    users = get_users()
    devices = get_used_devices()


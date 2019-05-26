from automoticz.tasks import *
from automoticz.utils import get_pin
from automoticz.utils import CACHE_PIN_KEY
from automoticz.extensions import cache
def test_set_beacon_pin(app):

    with app.app_context():

        task = set_beacon_pin.delay()
        result = task.get(timeout=30)
        cached_pin = get_pin(cached=True)
        pin = get_pin()
        assert int(pin) == int(cached_pin)

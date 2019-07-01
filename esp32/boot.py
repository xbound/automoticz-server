# This file is executed on every boot (including wake-boot from deepsleep)
import device
import machine

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')

if not device.sta_if.isconnected():
    device.connect_WIFI()
elif device.sta_if.isconnected():
    print('Connected to WIFI...')
    led = machine.Pin(2, machine.Pin.OUT)
    led.value(True)
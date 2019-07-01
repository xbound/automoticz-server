import ujson
import network
import machine

sta_if = network.WLAN(network.STA_IF)

def read_json_config():
    with open('config.json', 'r') as file:
        data = ujson.load(file)
    return data


CONFIG_DATA = read_json_config()

def connect_WIFI():
    if not sta_if.active():
        sta_if.active(True)
    if sta_if.isconnected():
        sta_if.disconnect()
    print('Scanning network...')
    discovered_networks = sta_if.scan()
    networks = CONFIG_DATA['Networks']
    for network in discovered_networks:
        n_ssid = network[0].decode('utf-8')
        print('Checking network {}'.format(n_ssid))
        net_info = list(filter(lambda x: x['SSID'] == n_ssid, networks))
        if net_info:
            net_info = net_info[0]
            print('Connecting...')
            sta_if.connect(net_info['SSID'], net_info['Password'])
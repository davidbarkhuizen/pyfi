NETWORK_INTERFACE = 'wlan0'

# LOG_LOCATION = '/var/log/pyfi/'
LOG_LOCATION = '/home/david/Documents/pyfi/vm/'

SAMPLE_INTERVAL_SECONDS = 5

def cls():
	print('\r\n'*80)

def networks_file_path():
	return LOG_LOCATION + 'networks.json'

def network_states_file_path():
	return LOG_LOCATION + 'network_states.json'

def gpx_file_path():
	return LOG_LOCATION + 'gps.gpx'

def network_locations_file_output_path():
	return LOG_LOCATION + 'network_locations.gpx'

def render_network_key(ssid, address):
	return ssid + ':' + address

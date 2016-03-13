import datetime
import time

from wifi import Cell, Scheme
from wifi.exceptions import InterfaceError

def render_network_key(ssid, address):
	"""ssid:address"""
	return ssid + ':' + address

def new_network_state():
	"""{ time, signal, quality }"""
	return {
		'time': [],
		'signal': [],
		'quality': []
	}

def new_network(address, ssid, frequency, encrypted, encryption_type, mode, bit_rates, channel):
	"""{ address, ssid, frequency, encrypted, encryption_type, mode, bit_rates, channel }"""

	network = {
		'address' : address
		,'ssid' : ssid
		,'frequency' : frequency
		,'encrypted' : encrypted
		,'encryption_type': encryption_type
		,'mode' : mode
		,'bit_rates' : bit_rates
		,'channel' : channel
		}

	return network

def sample_interface_neighbourhood(network_interface, networks = None, network_states = None):
	"""sample interface neighbourhood"""

	networks = networks if networks else {}
	network_states = network_states if network_states else {}

	timestamp = str(datetime.datetime.now())
	cells = Cell.all(network_interface)

	for cell in cells:

		network_key = render_network_key(cell.ssid, cell.address)

		if network_key not in networks.keys():

			network = new_network(
				cell.address, cell.ssid, cell.frequency,
				cell.encryption_type if cell.encrypted else None, cell.encrypted, cell.mode,
				cell.bitrates, cell.channel)

			networks[network_key] = network
			network_states[network_key] = new_network_state()

		network_state = network_states[network_key]

		network_state['time'].append(time)
		network_state['signal'].append(cell.signal)
		network_state['quality'].append(cell.quality)

	return networks, network_states

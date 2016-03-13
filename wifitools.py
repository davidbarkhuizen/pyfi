from wifi import Cell, Scheme
from wifi.exceptions import InterfaceError

def new_network_state():

	'''
	'''
	return {
		'time': [],
		'signal': [],
		'quality': []
	}

def new_network(address, ssid, frequency, encrypted, encryption_type, mode, bit_rates, channel):
	'''
	'''
	network = {
				'address' : address,
				'ssid' : ssid,
				'frequency' : frequency,
				'encrypted' : encrypted,
				'encryption_type': encryption_type,
				'mode' : mode,
				'bit_rates' : bit_rates,
				'channel' : channel
				}

	return network

def add_wifi_sample(networks, network_states):
	'''
	'''
	timestamp = str(datetime.datetime.now())
	cells = Cell.all(common.NETWORK_INTERFACE)

	for cell in cells:

		network_key = render_network_key(cell.ssid, cell.address)

		if network_key not in networks.keys():

			network = new_network(
								cell.address,
								cell.ssid,
								cell.frequency,
								cell.encrypted,
								cell.encryption_type if cell.encrypted else None,
								cell.mode,
								cell.bitrates,
								cell.channel
								)

			networks[network_key] = network
			network_states[network_key] = new_network_state()

		network_state = network_states[network_key]
		network_state['time'].append(time)
		network_state['signal'].append(signal)
		network_state['quality'].append(quality)

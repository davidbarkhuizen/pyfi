import common

from wifi import Cell, Scheme
from wifi.exceptions import InterfaceError

import datetime, os, json, signal
from threading import Thread, Event

def new_network_state():

	return {
		'time' : [],
		'signal' : [],
		'quality' : []
	}

def append_to_network_state(state, time, signal, quality):

	state['time'].append(time)
	state['signal'].append(signal)
	state['quality'].append(quality)

def new_network(address, ssid, frequency, encrypted, encryption_type, mode, bit_rates):
		
	network = { 'address' : address,
		'ssid' : ssid,
		'frequency' : frequency,
		'encrypted' : encrypted, 
		'encryption_type': encryption_type,
		'mode' : mode,
		'bit_rates' : bit_rates
		}

	return network

network_states = {}
networks = {}

def scan():

	# take sample
	
	cells = Cell.all(common.NETWORK_INTERFACE)
	timestamp = str(datetime.datetime.now())

	ssids = []

	# update data set

	for cell in cells:

		ssids.append(cell.ssid)

		# create new

		network_key = common.render_network_key(cell.ssid, cell.address) 

		if network_key not in networks.keys():

			network = new_network(cell.address, 
				cell.ssid, 
				cell.frequency, 
				cell.encrypted, 
				cell.encryption_type if cell.encrypted else None, 
				cell.mode, 
				cell.bitrates
				)

			networks[network_key] = network
			network_states[network_key] = new_network_state()

		# append to state series

		network_state = network_states[network_key]
		append_to_network_state(network_state, timestamp, cell.signal, cell.quality)

	print('%i active networks' % len(ssids))
	for ssid in sorted(ssids):
		print('- ' + ssid)

def get_logger():

	if not os.path.isdir(common.LOG_LOCATION):
		os.mkdir(common.LOG_LOCATION)

	def logger():
		
		networks_json = json.dumps(networks)
		with open(common.networks_file_path(), 'wt') as networks_file:
			networks_file.write(networks_json)

		network_state_json = json.dumps(network_states)
		with open(common.network_states_file_path(), 'wt') as network_states_file:
			network_states_file.write(network_state_json)

	return logger

exit_mutex = False

class ScanThreadWorker(Thread):

	def __init__(self, event):

		Thread.__init__(self)
		self.stopped = event

		self.log = get_logger()

	def run(self):

		log = True
		
		while not self.stopped.wait(common.SAMPLE_INTERVAL_SECONDS):

			common.cls()

			print('HIT ENTER TO EXIT')
			print('sampling frequency = 1 / {0} Hz'.format(common.SAMPLE_INTERVAL_SECONDS))

			print()

			print(datetime.datetime.now())
			
			try:
				scan()
			except InterfaceError as e:
				print('InterfaceError encountered during scanning')
				print(e)
				continue

			print('%i networks found in total' % len(networks.keys()))

			if not log:
				print('logging disabled')
				continue

			try:
				self.log()
			except PermissionError as e:
				print('permission error during attempt to log')
				print(e)
				log = False            	


def sample():

	stopFlag = Event()
	thread = ScanThreadWorker(stopFlag)
	thread.start()

	discard = input()
	stopFlag.set()

	cls()
	print('networks found:')
	for ssid in sorted([network['ssid'] for network in networks.values()]):
		print(ssid)

sample()

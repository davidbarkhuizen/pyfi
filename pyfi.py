import datetime
import os
import json
import wifitools

from console import NonBlockingConsole

import time

def render_network_key(ssid, address):
	return ssid + ':' + address

network_states = {}
networks = {}

def scan():

	# take sample


	f = open('network_summary.log', 'wt')

	for key in networks.keys():

		net = networks[key]

		signal = active_net_signal[key] if net in active_networks else ''
		quality = active_net_quality[key] if net in active_networks else ''

		s = '{0:32} {1:20}\n{2:10} {3:6} {4:8} {5:8} {6:5} {7:5}'.format(net['ssid'], net['address'], net['frequency'], str(net['encrypted']), net['encryption_type'], net['mode'], signal, quality)

		if net in active_networks:
			s = '* ' + s
		else:
			s = '  ' + s

		print(s)
		f.write(s + '\n')

	f.close()

def get_logger():

	'''
	if not os.path.isdir(log_file_path):
		os.mkdir(log_file_path)
	'''

	def logger():

		'''
		networks_json = json.dumps(networks)
		with open(common.networks_file_path(), 'wt') as networks_file:
			networks_file.write(networks_json)

		network_state_json = json.dumps(network_states)
		with open(common.network_states_file_path(), 'wt') as network_states_file:
			network_states_file.write(network_state_json)
		'''
		pass

	return logger

# ----------------------------------------

def cls():
	print('\r\n'*80)

def run_scans():

	log = get_logger()

	with NonBlockingConsole() as nb_console:

		while (True):

			print('HIT ENTER TO EXIT')
			print('')
			print(datetime.datetime.now())
			print('')

			try:
				scan()
			except InterfaceError as e:
				print('InterfaceError encountered during scanning')
				msg = str(e)
				print(msg)
			except SyntaxError as se:
				print(se)
				local_stop = True
				print('stopping')
				return

			print('')
			print('{0} networks found'.format(len(networks.keys())))

			if not log:
				print('logging disabled')

			try:
				log()
			except Exception as e:
				print('permission error during attempt to log')
				print(e)
				log = None

			time.sleep(common.SAMPLE_INTERVAL_SECONDS)

			if nb_console.get_key_presses():
				break

def sample():

	run_scans()

sample()

import json
import datetime

from dateutil import parser

TIME_DIFF_CORRECTION = datetime.timedelta(hours=-2)

import common
from pygpx.gpxparser import parse_gpx_xml

def insert_raw_xml_into_gpx_template(raw_xml):
	gpx_template = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?><gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:wptx1="http://www.garmin.com/xmlschemas/WaypointExtension/v1" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" creator="eTrex 20" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www8.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/WaypointExtension/v1 http://www8.garmin.com/xmlschemas/WaypointExtensionv1.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd"><metadata><link href="http://www.garmin.com"><text>Garmin International</text></link><time>2015-06-15T07:25:53Z</time></metadata>{0}</gpx>'''
	return gpx_template.format(raw_xml)

# -------------------------------

gpx_xml = ''
with open(common.gpx_file_path(), 'rt') as gpx_file:
	gpx_xml = gpx_file.read()

gpx = parse_gpx_xml(gpx_xml)

networks = None
with open(common.networks_file_path(), 'rt') as networks_file:
	networks_json_string = networks_file.read()
	networks = json.loads(networks_json_string)

network_states = None
with open(common.network_states_file_path(), 'rt') as network_states_file:
	network_states_json_string = network_states_file.read()
	network_states = json.loads(network_states_json_string)

wpts = []

for network_key in networks.keys():
	network = networks[network_key]
	states = network_states[network_key]

	ssid = network['ssid']
	address = network['address']

	skip = False

	reject_tokens = ['Megasurf', 'Sectrete']
	for token in reject_tokens:
		if ssid.find(token) != -1:
			print('rejecting ...', ssid)
			skip = True
			break
	if skip:
		continue

	locations = []
	for time in states['time']:
		time = parser.parse(time) + TIME_DIFF_CORRECTION
		locations_for_time = gpx.get_locations_at_time(time)
		locations.extend(locations_for_time)

	for location in locations:
		# s = '{0}|{1}|{2}|{3}'.format(ssid, address, location.lat, location.lon)	
		s = '<wpt lat="{1}" lon="{2}"><ele>1631.336304</ele><name>{0}</name></wpt>'
		s = s.format(ssid, location.lat, location.lon)
		wpts.append(s)

waypoint_gpx_xml = insert_raw_xml_into_gpx_template(''.join(wpts))
with open(common.network_locations_file_output_path(), 'wt') as network_locations_file:
	network_locations_file.write(waypoint_gpx_xml)
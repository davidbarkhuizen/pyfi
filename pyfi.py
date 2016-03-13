
import json
import wifitools
import pyconfig

import os

cfg = pyconfig.load_json_config('config.json')
print(cfg)
net_interface = cfg['network_interface']
networks, network_states = wifitools.sample_interface_neighbourhood(net_interface)
print(networks)

import json

def load_json_config(path):
	"""load json file at path as python dict"""
	json_dict = None

	with open(path) as json_file:
		json_dict = json.load(json_file)

	return json_dict

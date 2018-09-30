'''
This script helps to configure public server settings and provides utilities to 
save and read config files across the project.
'''

import sys
import json

PUBLIC_SERVER_CONFIG_FILE = 'config/public_server.json'

def read():
	try:
		file = open(PUBLIC_SERVER_CONFIG_FILE, 'r')
	except IOError, e:
		print 'Configuration file %s missing!' %(PUBLIC_SERVER_CONFIG_FILE)
		sys.exit(0)

	config = json.load(file)
	assert config.get('ip', None) is not None
	assert config.get('hostname', None) is not None
	assert config.get('port', None) is not None
	assert config.get('username', None) is not None
	assert config.get('password', None) is not None
	return config

def write():
	# Overwrite configuration for public server
	config = read()
	for key in config:
		print '%s: [%s]' %(key, config[key]),
		input_val = raw_input()
		if input_val != '':
			config[key] = input_val

	print 'Final config to save: '
	print json.dumps(config, indent=4)
	print 'Save [Y/n]', 
	input_val = raw_input()
	
	if (input_val.lower() == 'y' 
		or input_val.lower() == 'yes' 
		or input_val == ''):

		file = open(PUBLIC_SERVER_CONFIG_FILE, 'w')
		json.dump(config, file)

	else:
		write()

	print 'Saved!'


if __name__ == '__main__':
	# initialize the params and start the script
	write()
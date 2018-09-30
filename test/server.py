# Append src folder path to sys.path

import sys
import os
sys.path.append('/'.join(os.path.realpath(__file__).split('/')[0:-2]) + '/src')

from connection import Connection
s = Connection(sock_type='server_sock', port=12355)

assert s.is_server_sock

assert s.bind()
assert s.listen()

while True:
	client_connection = s.accept()
	print client_connection
	client_connection.send('Welcome client!')
	client_connection.close()
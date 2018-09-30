# Append src folder path to sys.path

import sys
import os
sys.path.append('/'.join(os.path.realpath(__file__).split('/')[0:-2]) + '/src')

from connection import Connection
c = Connection(sock_type='client_sock', port=12355)

assert c.is_client_sock

c.connect()
print c.recv()
c.close()
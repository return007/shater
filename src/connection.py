import sys
import json
import os
import socket

class Connection(object):
	'''
	The class helps create TCP connection using socket library.
	Also provides some high level methods to send and receive Command objects.
	'''

	def __init__(self, sock=None, ip='', port=12345, sock_type='server_sock', **kwargs):
		'''
		Intializes with given ip address and port. 

		:param str ip 			: IP address to connect/bind to
		:param int port			: Port to connect/bind to
		:param str sock_type 	: Type of socket, defaults to server_sock, 
								  acceptable values are 'server_sock', 
								  'client_sock'
		'''

		if sock is not None and type(sock) is socket._socketobject:
			self._socket = sock
		else:
			self._socket = socket.socket()

		self._sock_type = sock_type

		if self.is_server_sock:
			self._init_server_sock(ip, port, **kwargs)
		elif self.is_client_sock:
			self._init_client_sock(ip, port, **kwargs)
		else:
			raise ValueError('Unable to determine sock_type. Use "server_sock"\
							  to create server socket or "client_sock" to \
							  create client socket.')


	def _init_server_sock(self, binding_ip='', binding_port=12345, **kwargs):
		# Private helper method to create server socket
		# Be default binds to 0.0.0.0 meaning accepting connections from 
		# anywhere. Default port is 12345

		self._ip = binding_ip
		self._port = binding_port


	def _init_client_sock(self, ip='127.0.0.1', port=12345, **kwargs):
		# Private helped method to create client socket
		# By default, connects to localhost on 12345 port

		self._ip = ip
		self._port = port


	def __str__(self):
		return 'Connection Object at ip: %s, port: %s, sock_type: %s' %(self._ip, 
			self._port, self._sock_type)

	@property
	def is_server_sock(self):
		return self._sock_type == 'server_sock'

	@property
	def is_client_sock(self):
		return self._sock_type == 'client_sock'
	

	def bind(self):
		# Helper method to bind server socket

		if not self.is_server_sock:
			raise TypeError('Cannot bind client socket!')

		try:
			self._socket.bind((self._ip, self._port))
		except:
			return False
		return True


	def listen(self, max_connection=10):
		# Helper method to listen to clients on same port

		if not self.is_server_sock:
			raise TypeError('Cannot listen via client socket!')

		try:
			self._socket.listen(max_connection)
		except:
			return False
		return True


	def connect(self):
		# Helper method to connect to server socket

		if not self.is_client_sock:
			raise TypeError('Cannot connect via server socket!')

		try:
			self._socket.connect((self._ip, self._port))
		except:
			return False
		return True


	def accept(self):
		'''
		Helper method to accept connections from client socket.

		:return Connection object: returns client's Connection object  

		'''

		if not self.is_server_sock:
			raise TypeError('Cannot accept connections to client socket!')

		try:
			c_sock, addr = self._socket.accept()
			return Connection(sock=c_sock, sock_type='client_sock', ip=addr[0], port=addr[1])
		except:
			return None


	def send(self, data):
		'''
		Helper method to send string data over connection
		'''

		if type(data) is str:
			return self._socket.send(data)
		raise TypeError('Unable to send non str data')


	def recv(self, chunk_size=1024):
		'''
		Helper method to receive data from socket, broken into chuck size
		'''

		data = self._socket.recv(chunk_size)
		complete_data = ''
		while data != '':
			complete_data += data
			data = self._socket.recv(chunk_size)

		return complete_data


	def close(self):
		# Helper method to close socket object
		self._socket.close()
#! usr/bin/python3
# -*- coding:utf-8-*-
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for data in [b'I', b'biliang', b'cai']:
	s.sendto(data, ('127.0.0.1', 6666))
	print(s.recv(1024).decode('utf-8'))
s.close()
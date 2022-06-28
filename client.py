# Python program to implement client side of chat room.
import os
import socket
import select
import sys
import time
from _thread import start_new_thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect(("localhost", 3124))

def send_img(socks):
	message = sys.stdin.readline()
	f = open(message[:-1], "rb")
	l = os.path.getsize(message[:-1])
	m = f.read(l)
	f.close()
	server.sendall(m)
	print("message sent", len(m))
	time.sleep(0.1)
	server.send(bytes("EOF", 'utf-8'))

total_message = bytes()
while True:
	sockets_list = [sys.stdin, server]

	read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
	for socks in read_sockets:
		if socks == server:
			try:
				message = socks.recv(2048)
				try:
					value = message.decode('utf-8')
					if value.lower() == 'eof':
						print("recv")
						file = open("done1.png", 'wb')
						file.write(total_message)
						file.close()
						total_message = bytes()
				except:
					total_message += message
			except:
				continue
		else:
			start_new_thread(send_img, (server,))


server.close()

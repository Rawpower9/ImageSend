# Python program to implement server side of chat room.
import os
import socket
import sys
import time
from _thread import start_new_thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = "localhost"

Port = 3124

server.bind((IP_address, Port))


server.listen(100)

list_of_clients = []

# def send_img(conn, addr):
# 	while True:
# 		message = sys.stdin.readline()
# 		f = open(message[:-1], "rb")
# 		l = os.path.getsize(message[:-1])
# 		m = f.read(l)
# 		server.sendall(m)
# 		f.close()
# 		time.sleep(0.3)
# 		print("SENDING EOF")
# 		conn.send(bytes("EOF", 'utf-8'))
# 		print("sent")

def broadcast(connection):
	while True:
		for clients in list_of_clients:
			try:
				message = sys.stdin.readline()
				f = open(message[:-1], "rb")
				l = os.path.getsize(message[:-1])
				m = f.read(l)
				conn.sendall(m)
				print("message sent", len(m))
				f.close()
				time.sleep(0.1)
				connection.send(bytes("EOF", 'utf-8'))
			except:
				print("something went wrong 49 server")
		if len(list_of_clients) == 0:
			break


def clientthread(conn, addr):
	total_message = bytes()
	start_new_thread(broadcast, (conn,))
	while True:
		try:
			message = conn.recv(2048)
			try:
				value = message.decode('utf-8')
				if value.lower() == 'eof':
					file = open("done.png", 'wb')
					file.write(total_message)
					file.close()
					print("recv", len(total_message))
					total_message = bytes()
			except:
				total_message += message
		except:
			continue


def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:
	conn, addr = server.accept()
	list_of_clients.append(conn)
	print (addr[0] + " connected")
	clientthread(conn,addr)

conn.close()
server.close()

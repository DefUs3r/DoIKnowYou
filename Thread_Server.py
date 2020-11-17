import numpy as np
import cv2
import socket
import pickle
import struct
from Recognize import *
import threading
import ClientHandler
import connUtils

def quit(command):
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.connect((HOST, PORT))
    connUtils.send_one_message(sckt, command.encode('utf-8'))
    sckt.close()
    return

HOST = "localhost"
# Port for socket
PORT = 5000 # Arbitrary non-privileged port
# Bind to the port
try:
	# Create a socket object
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("\r[CONN] Socket successfully created")
except socket.error as err:
	print("\r[FAIL] Socket creation failed with error : ",err)

try:
	server_socket.bind((HOST, PORT))
except socket.error as err:
	print('[FAIL] Bind failed. Error Message :  ',err)
	sys.exit()

print('Socket bind successfully')
print("\r[BIND] Socket binded to : ",PORT)
# Listen for connections : allow only 5 connection
server_socket.listen(5)
print("\r[LISN] Socket is now listening") 	 

name = input('Enter your name :')
print('Welcome to DoIKnowYou. This is server.')

def listen():
	while True:
		print('\r[CONN] Waiting for client...')
		# Wait to accept a connection - blocking call
		client_socket, addr = server_socket.accept()
		# print the socket object : ip addr and port nb : client info
		print('\r[CONN] Connected from ip: {} and port : {} '.format(addr[0],addr[1]))
		t = threading.Thread(target=ClientHandler.handle_client, args=(client_socket,))
		#t.daemon = True
		t.start()
		if t.is_alive(): 
		    pass 
		else: 
		    print('[THREAD] Serviced Thread.')
		    break 

while True:
	sys.stdout.write('%s@[Server] -> ' %name)
	sys.stdout.flush()
	command = sys.stdin.readline().strip()

	if (command == 'quit'):
		print('[WARNING] Quitting Server side. If you sent this command in between an operation you might experience bugs. You have been warned.')
		break

	if (command == 'listen'):
		listen()

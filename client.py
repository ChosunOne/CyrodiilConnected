import socket
import threading
import copy
import inspect
from player import Player

def waitforserver(server):
	connected = True
	while connected:
		data = server.recv(1024)
		print("Received data from server")

def waitforupdate(player, server):
	oldPlayer = Player(name = player.name, character = copy.deepcopy(player.character), position = copy.deepcopy(player.position), 
		loadedcells = copy.deepcopy(player.loadedcells), inputs = copy.deepcopy(player.inputs), connection = player.connection)
	while True:
		oldAttributes = inspect.getmembers(oldPlayer, lambda a:not(inspect.isroutine(a)))
		oldAttributes = [a for a in oldAttributes if not(a[0].startswith('__') and a[0].endswith('__'))]
		newAttributes = inspect.getmembers(player, lambda a:not(inspect.isroutine(a)))
		newAttributes = [a for a in newAttributes if not(a[0].startswith('__') and a[0].endswith('__'))]
		changes = []

		for i in range(len(oldAttributes)):
			if oldAttributes[i][1] != newAttributes[i][1]:
				changes.append(newAttributes[i])

		if len(changes) != 0:
			for c in changes:
				server.send("begin".encode('ascii'))
				server.send(c[0].encode('ascii'))
				server.send(c[1].encode('ascii'))
				server.send("end".encode('ascii'))
				setattr(oldPlayer, c[0], c[1])


name = input("Enter a name for your player:\n")

server = socket.socket()
host = socket.gethostname()
port = 12345
server.connect((host, port))

confirm = server.recv(1024)

if confirm.decode('ascii') == 'Connection Established':
	print("Connected to server")
	connected = True
	cPlayer = Player(name = name, connection = server)
	server.send(cPlayer.name.encode('ascii'))
	
	servermanager = threading.Thread(target=waitforserver, args=(server,))
	servermanager.daemon = True
	servermanager.start()

	updatemanager = threading.Thread(target=waitforupdate, args=(cPlayer, server,))
	updatemanager.daemon = True
	updatemanager.start()

while True:
	pass

	

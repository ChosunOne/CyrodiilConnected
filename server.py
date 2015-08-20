import socket
import threading
from player import Player

lock = threading.Lock()

def waitforclients():
	while True:
		c, addr = server.accept()
		print("Got connection from", addr)

		newplayer = Player(connection = c)
		newplayer.connection.send("Connection Established".encode('ascii'))
		newplayer.name = newplayer.connection.recv(1024).decode('ascii')
		players.append(newplayer)

		lock.acquire()
		print(newplayer.name, "has connected to the server.")
		lock.release()

		t = threading.Thread(target=waitforupdate, args=(newplayer,))
		t.daemon = True
		threads.append(t)
		t.start()
		
def waitforupdate(player):
	connected = True
	while connected:
		if player.connection.recv(1024).decode('ascii') == "begin":
			attr = player.connection.recv(1024).decode('ascii')
			update = player.connection.recv(1024).decode('ascii')
			setattr(player, attr, update)
		if player.connection.recv(1024).decode('ascii') == "end":
			pass


players = []
time = None
hosts = []
threads = []

server = socket.socket()
host = socket.gethostname()
port = 12345
server.bind((host, port))
server.listen(16)

connectionmanager = threading.Thread(target=waitforclients)
connectionmanager.daemon = True
connectionmanager.start()

while True:
	pass


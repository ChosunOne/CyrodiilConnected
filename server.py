import socket
import threading
from player import Player

lock = threading.Lock()

rbuffer = {}
sbuffer = {}

sending = False

def fillrbuffer(player):
    connected = True
    while connected:
        if not sending:
            datatype = player.connection.recv(1024).decode('ascii')
            print("Datatype", datatype, "has been received from", player.name)
            player.connection.send("confirm".encode('ascii'))
            print("Confirmation message has been sent to", player.name)
            data = player.connection.recv(1024).decode('ascii')
            print(data, "has been received from", player.name)
            player.connection.send("confirm".encode('ascii'))
            print("Confirmation message 2 has been sent to", player.name)
        
            if datatype == "string":
                pass
            elif datatype == "int":
                data = int(data)
            elif datatype == "float":
                data = float(data)
            elif datatype == "bool":
                data = bool(data)
            rbuffer[player].append(data)
            print(data, "has been appended to the rbuffer for", player.name)

def sendsbuffer(player):
    connected = True
    while connected:
        if len(sbuffer[player]) != 0:
            sending = True
            confirm = False
            data = sbuffer[player][0]
            datatype = type(data)
            if datatype is str:
                player.connection.send("string".encode('ascii'))
                print("Server is sending string to", player.name)
            elif datatype is int:
                player.connection.send("int".encode('ascii'))
                print("Server is sending int to", player.name)
            elif datatype is float:
                player.connection.send("float".encode('ascii'))
                print("Server is sending float to", player.name)
            elif datatype is bool:
                player.connection.send("bool".encode('ascii'))
                print("Server is sending bool to", player.name)

            while not confirm:
                response = player.connection.recv(1024).decode('ascii')
                print("Response", response, "received from", player.name)
                if response == "confirm":
                    confirm = True

            confirm = False
            data = str(data).encode('ascii')
            player.connection.send(data)
            print(data.decode('ascii'), "has been sent to", player.name)

            while not confirm:
                response = player.connection.recv(1024).decode('ascii')
                print("Response", response, "received from", player.name)
                if response == "confirm":
                    confirm = True

            sbuffer[player] = sbuffer[player][1:]
            print("Sent", str(data), "to", player.name)
            sending = False

def receivedata(player):
    if not rbuffer[player]:
        while not rbuffer[player]:
            pass
    data = rbuffer[player][0]
    rbuffer[player] = rbuffer[player][1:]
    return data

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

        rbuffer[newplayer] = []
        sbuffer[newplayer] = []

        rbuffermanager = threading.Thread(target = fillrbuffer, args = (newplayer,))
        rbuffermanager.daemon = True
        rbuffermanager.start()

        sbuffermanager = threading.Thread(target = sendsbuffer, args = (newplayer,))
        sbuffermanager.daemon = True
        sbuffermanager.start()

        updatemanager = threading.Thread(target=waitforupdate, args=(newplayer,))
        updatemanager.daemon = True
        threads.append(updatemanager)
        updatemanager.start()
        
def waitforupdate(player):
    connected = True
    while connected:
        data = receivedata(player)
        #See if the client is updating the character
        if data == "character":
            #Wait for the beginning of a transmission
            data = receivedata(player)
            if data == "begin":
                while data != "end":
                    #Check to see if the transmission has ended, if not then begin updating data
                    data = receivedata(player)
                    if data != "end":
                        #If the data was not the word "end" then we received the name of the field to update
                        attr = data
                        #Receive the value to update
                        update = receivedata(player)
                        setattr(player.character, attr, update)

        elif data == "attributes":
            #Wait for beginning of attributes transmission
            data = receivedata(player)
            if data == "begin":
                while data != "end":
                    #Check to see if transmission has ended, if not then prepare to update
                    data = receivedata(player)
                    if data != "end":
                        #If data is not "end" then the data is the name of the attribute to update
                        attr = data
                        #Receive value to update and update the value
                        update = receivedata(player)
                        setattr(player.character.attributes, attr, update)

        elif data == "position":
            data = receivedata(player)
            if data == "begin":
                attr = receivedata(player)
                update = receivedata(player)
                setattr(player.position, attr, update)


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


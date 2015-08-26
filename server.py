import socket
import threading
import struct
from player import Player

DEBUG_NET = True
DEBUG_NET_REL = False

lock = threading.Lock()

rbuffer = {}
sbuffer = {}

sending = False

def fillrbuffer(player):
    connected = True
    while connected:
        if not sending:
            datatype = player.connection.recv(1024).decode('ascii')

            if DEBUG_NET_REL:
                print("Datatype", datatype, "has been received from", player.name)

            player.connection.send("confirm".encode('ascii'))

            if DEBUG_NET_REL:
                print("Confirmation message has been sent to", player.name)

            data = player.connection.recv(1024)

            if DEBUG_NET_REL:
                print(data, "has been received from", player.name)

            player.connection.send("confirm".encode('ascii'))

            if DEBUG_NET_REL:
                print("Confirmation message 2 has been sent to", player.name)
        
            if datatype == "string":
                data = data.decode('ascii')
            elif datatype == "int":
                data = struct.unpack('i', data)[0]
            elif datatype == "float":
                data = struct.unpack('f', data)[0]
                data = round(data, ndigits = 4)
            elif datatype == "bool":
                data = struct.unpack('?', data)[0]
            elif datatype == "tuple":
                #To be used only in receiving positional coordinate data
                data = struct.unpack('iii', data)
            elif datatype == "list":
                data = list(data)
            elif datatype == "bytes":
                pass
            rbuffer[player].append(data)
            if DEBUG_NET:
                print(data, "has been appended to the rbuffer for", player.name)

def sendsbuffer(player):
    connected = True
    while connected:
        if len(sbuffer[player]) != 0:
            sending = True
            confirm = False
            data = sbuffer[player].pop(0)
            datatype = type(data)
            if datatype is str:
                player.connection.send("string".encode('ascii'))
                data = data.encode('ascii')
                if DEBUG_NET:
                    print("Server is sending string to", player.name)
            elif datatype is int:
                player.connection.send("int".encode('ascii'))
                data = struct.pack('i', data)
                if DEBUG_NET:
                    print("Server is sending int to", player.name)
            elif datatype is float:
                player.connection.send("float".encode('ascii'))
                data = struct.pack('f', data)
                if DEBUG_NET:
                    print("Server is sending float to", player.name)
            elif datatype is bool:
                player.connection.send("bool".encode('ascii'))
                data = struct.pack('?', data)
                if DEBUG_NET:
                    print("Server is sending bool to", player.name)
            elif datatype is tuple:
                #To be used only in sending positional coordinate data
                player.connection.send("tuple".encode('ascii'))
                data = struct.pack(''.join(['i' for x in range(0, len(data))]), data[0], data[1], data[2])
                if DEBUG_NET:
                    print("Server is sending tuple to", player.name)
            elif datatype is list:
                player.connection.send("list".encode('ascii'))
                if DEBUG_NET:
                    print("Server is sending list to", player.name)
            elif datatype is bytes:
                player.connection.send("bytes".encode('ascii'))
                if DEBUG_NET:
                    print("Server is sending bytes to", player.name)

            while not confirm:
                response = player.connection.recv(1024).decode('ascii')
                if DEBUG_NET_REL:
                    print("Response", response, "received from", player.name)
                if response == "confirm":
                    confirm = True

            confirm = False
            data = bytes(data)
            player.connection.send(data)
            if DEBUG_NET:
                print(data.decode('ascii'), "has been sent to", player.name)

            while not confirm:
                response = player.connection.recv(1024).decode('ascii')
                if DEBUG_NET_REL:
                    print("Response", response, "received from", player.name)
                if response == "confirm":
                    confirm = True

            if DEBUG_NET:
                print("Sent", data.decode('ascii'), "to", player.name)
            sending = False

def receivedata(player):
    if not rbuffer[player]:
        while not rbuffer[player]:
            pass
    data = rbuffer[player][0]
    rbuffer[player] = rbuffer[player][1:]
    return data

def senddata(player, data):
    sbuffer[player].append(data)

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
                while data != "end":
                    data = receivedata(player)
                    if data != "end":
                        attr = data
                        update = receivedata(player)
                        setattr(player.position, attr, update)

def updateplayer(player, serverplayer):
    connected = True
    while connected:
        #Check to see if the server's representation of the player character has changed from the client character
        oldchar = player.character
        newchar = serverplayer.character
        charchanges = oldchar.compare(newchar)

        if len(charchanges) != 0:
            senddata(player, "character")
            senddata(player, "begin")
            for c in charchanges:
                senddata(player, c[0])
                senddata(player, c[1])
                setattr(oldchar, c[0], c[1])
            senddata(player, "end")

        #Check to see if the server player character attributes have changed
        oldattr = player.character.attributes
        newattr = serverplayer.character.attributes
        attrchanges = oldattr.compare(newattr)

        if len(attrchanges) != 0:
            senddata(player, "attributes")
            senddata(player, "begin")
            for c in attrchanges:
                senddata(player, c[0])
                senddata(player, c[1])
                setattr(oldattr, c[0], c[1])
            senddata(player, "end")

        #Check to see if the server player has changed position
        oldpos = player.position
        newpos = serverplayer.position
        poschanges = oldpos.compare(newpos)

        if len(poschanges) != 0:
            senddata(player, "position")
            senddata(player, "begin")
            for c in poschanges:
                senddata(player, c[0])
                senddata(player, c[1])
                setattr(oldpos, c[0], c[1])
            senddata(player, "end")


players = []
time = None
hosts = []
threads = []

server = socket.socket()
host = socket.gethostname()
port = 30033
server.bind((host, port))
server.listen(16)

connectionmanager = threading.Thread(target=waitforclients)
connectionmanager.daemon = True
connectionmanager.start()

while True:
    pass


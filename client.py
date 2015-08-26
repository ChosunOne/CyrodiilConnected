import socket
import threading
import copy
import inspect
import struct
import random
from player import Player

DEBUG_NET = True
DEBUG_NET_REL = False


lock = threading.Lock()

sending = True

rbuffer = []
sbuffer = []

def fillrbuffer(server):
    connected = True
    while connected:
        if not sending:
            datatype = server.recv(1024).decode('ascii')

            if DEBUG_NET_REL:
                print("Datatype", datatype, "has been received from server")

            server.send("confirm".encode('ascii'))
            
            if DEBUG_NET_REL:
                print("Confirmation message has been sent to server")

            data = server.recv(1024)
            
            if DEBUG_NET:
                print(data, "has been received from server")
            
            server.send("confirm".encode('ascii'))

            if DEBUG_NET_REL:
                print("Confirmation message 2 has been sent to server")

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
                data = struct.unpack('iii', data)
            elif datatype == "list":
                data = list(data)
            elif datatype == "bytes":
                pass
            rbuffer.append(data)
            if DEBUG_NET:
                print(str(data), "has been appended to the rbuffer")

def sendsbuffer(server):
    connected = True
    while connected:
        if len(sbuffer) != 0:
            sending = True
            confirm = False
            data = sbuffer.pop(0)
            datatype = type(data)
            if datatype is str:
                server.send("string".encode('ascii'))
                data = data.encode('ascii')
                if DEBUG_NET_REL:
                    print("Client is sending string to server")
            elif datatype is int:
                server.send("int".encode('ascii'))
                data = struct.pack('i', data)
                if DEBUG_NET_REL:
                    print("Client is sending int to server")
            elif datatype is float:
                server.send("float".encode('ascii'))
                data = struct.pack('f', data)
                if DEBUG_NET_REL:
                    print("Client is sending float to server")
            elif datatype is bool:
                server.send("bool".encode('ascii'))
                data = struct.pack('?', data)
                if DEBUG_NET_REL:
                    print("Client is sending bool to server")
            elif datatype is bytes:
                server.send("bytes".encode('ascii'))
                if DEBUG_NET_REL:
                    print("Client is sending bytes to server")
            elif datatype is tuple:
                #Only send a tuple containing 3 integers for positional coordinate data
                server.send("tuple".encode('ascii'))
                data = struct.pack(''.join(['i' for x in range(0, len(data))]), data[0], data[1], data[2])
                if DEBUG_NET_REL:
                    print("Client is sending tuple to server")
            elif datatype is list:
                server.send("list".encode('ascii'))
                if DEBUG_NET_REL:
                    print("Client is sending list to server")
            

            while not confirm:
                response = server.recv(1024).decode('ascii')
                if DEBUG_NET_REL:
                    print("Response", response, "has been received from the server")
                if response == "confirm":
                    confirm = True
            
            confirm = False
            server.send(data)
            if DEBUG_NET:
                print(data, "has been sent to the server")

            while not confirm:
                response = server.recv(1024).decode('ascii')
                if DEBUG_NET_REL:
                    print("Response", response, "received from server")
                if response == "confirm":
                    confirm = True

            sending = False

def receivedata(server):
    if not rbuffer:
        while not rbuffer:
            pass
        data = rbuffer[0]
        rbuffer = rbuffer[1:]
        return data

def updateplayer(player, server):
    oldPlayer = Player(name = player.name, character = copy.deepcopy(player.character), position = copy.deepcopy(player.position), 
        loadedcells = copy.deepcopy(player.loadedcells), inputs = copy.deepcopy(player.inputs), connection = player.connection)
    while True:
        #Check to see if the player character has been changed
        oldchar = oldPlayer.character
        newchar = player.character
        charchanges = oldchar.compare(newchar)

        if len(charchanges) != 0:
            sbuffer.append("character")
            sbuffer.append("begin")
            for c in charchanges:
                sbuffer.append(c[0])
                sbuffer.append(c[1])
                #Update the old player after update is sent to server
                setattr(oldchar, c[0], c[1])
                    
            sbuffer.append("end")

        #Check to see if the player's attributes have been changed
        oldattr = oldPlayer.character.attributes
        newattr = player.character.attributes
        attrchanges = oldattr.compare(newattr)

        if len(attrchanges) != 0:
            sbuffer.append("attributes")
            sbuffer.append("begin")
            for c in attrchanges:
                sbuffer.append(c[0])
                sbuffer.append(c[1])
                setattr(oldattr, c[0], c[1])
            sbuffer.append("end")
            

        #Check to see if the player position has been changed
        oldpos = oldPlayer.position
        newpos = player.position
        poschanges = oldpos.compare(newpos)

        if len(poschanges) != 0:
            sbuffer.append("position")
            sbuffer.append("begin")
            for c in poschanges:
                sbuffer.append(c[0])
                sbuffer.append(c[1])
                setattr(oldpos, c[0], c[1])
            sbuffer.append("end") 

        #TODO Check to see if the player's loaded cells has been changed

        #TODO Check to see in the player's inputs have changed

def waitforupdate(server):
    connected = True

    while connected:
        data = receivedata(server)
        if data == "character":
            data = receivedata(server)
            if data == "begin":
                while data != "end":
                    data = receivedata(server)
                    if data != "end":
                        attr = data
                        update = receivedata(server)
                        setattr(cPlayer.character, attr, update)

        elif data == "attributes":
            data = receivedata(server)
            if data == "begin":
                while data != "end":
                    data = receivedata(server)
                    if data != "end":
                        attr = data
                        update = receivedata(server)
                        setattr(cPlayer.character.attributes, attr, update)

        elif data == "position":
            data = receivedata(server)
            if data == "begin":
                while data != "end":
                    data = receivedata(server)
                    if data != "end":
                        attr = data
                        update = receivedata(server)
                        setattr(cPlayer.position, attr, update)


name = input("Enter a name for your player:\n")
host = input("Enter the host you wish to connect to:\n")

if host == "localhost" or host == "127.0.0.1":
    host = socket.gethostname()

server = socket.socket()
port = 30033
server.connect((host, port))

confirm = server.recv(1024)

if confirm.decode('ascii') == 'Connection Established':
    print("Connected to server")
    connected = True
    cPlayer = Player(name = name, connection = server)
    server.send(cPlayer.name.encode('ascii'))
    
    rbuffermanager = threading.Thread(target = fillrbuffer, args = (server,))
    rbuffermanager.daemon = True
    rbuffermanager.start()

    sbuffermanager = threading.Thread(target = sendsbuffer, args = (server,))
    sbuffermanager.daemon = True
    sbuffermanager.start()

    updatemanager = threading.Thread(target = updateplayer, args = (cPlayer, server,))
    updatemanager.daemon = True
    updatemanager.start()

cPlayer.character.bounty = 1000
cPlayer.character.encumbrance = 100
cPlayer.character.attributes.agility = 37
cPlayer.character.attributes.endurance = 57

while True:   
    randx = int(random.random() * 1000)
    randy = int(random.random() * 1000)
    randz = int(random.random() * 1000)
    cPlayer.position.local = (randx, randy, randz)

    

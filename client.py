import socket
import threading
import copy
import inspect
from player import Player

lock = threading.Lock()

sending = True

rbuffer = []
sbuffer = []

def fillrbuffer(server, rbuffer):
    connected = True
    while connected:
        if not sending:
            datatype = server.recv(1024).decode('ascii')
            print("Datatype", datatype, "has been received from server")
            server.send("confirm".encode('ascii'))
            print("Confirmation message has been sent to server")
            data = server.recv(1024).decode('ascii')
            print(data, "has been received from server")
            server.send("confirm".encode('ascii'))
            print("Confirmation message 2 has been sent to server")
            if datatype == "string":
                pass
            elif datatype == "int":
                data = int(data)
            elif datatype == "float":
                data = float(data)
            elif datatype == "bool":
                data = bool(data)
            rbuffer.append(data)
            print(str(data), "has been appended to the rbuffer")

def sendsbuffer(server, sbuffer):
    connected = True
    while connected:
        if len(sbuffer) != 0:
            sending = True
            confirm = False
            data = sbuffer[0]
            datatype = type(data)
            if datatype is str:
                server.send("string".encode('ascii'))
                print("Client is sending string to server")
            elif datatype is int:
                server.send("int".encode('ascii'))
                print("Client is sending int to server")
            elif datatype is float:
                server.send("float".encode('ascii'))
                print("Client is sending float to server")
            elif datatype is bool:
                server.send("bool".encode('ascii'))
                print("Client is sending bool to server")

            while not confirm:
                response = server.recv(1024).decode('ascii')
                print("Response", response, "has been received from the server")
                if response == "confirm":
                    confirm = True
            
            confirm = False
            data = str(data).encode('ascii')
            server.send(data)
            print(data.decode('ascii'), "has been sent to the server")

            while not confirm:
                response = server.recv(1024).decode('ascii')
                print("Response", response, "received from server")
                if response == "confirm":
                    confirm = True

            sbuffer = sbuffer[1:]
            sending = False

def receivedata(server):
    if not rbuffer:
        while not rbuffer:
            pass
        data = rbuffer[0]
        rbuffer = rbuffer[1:]
        return data

def waitforupdate(player, server):
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
                setattr(oldPlayer.character, c[0], c[1])
                    
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
                setattr(oldPlayer.character.attributes, c[0], c[1])
            sbuffer.append("end")


        #Check to see if the player position has been changed
        oldpos = oldPlayer.position
        newpos = player.position
        poschanges = oldpos.compare(newpos)

        if len(poschanges) != 0:
            sbuffer.append("position")
            for c in poschanges:
                sbuffer.append("begin")
                sbuffer.append(c[0])
                sbuffer.append(c[1])
                sbuffer.append("end")

                #Update the old player after update is sent to server
                setattr(oldPlayer.position, c[0], c[1]) 


        #TODO Check to see if the player's loaded cells has been changed

        #TODO Check to see in the player's inputs have changed


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
    
    rbuffermanager = threading.Thread(target = fillrbuffer, args = (server, rbuffer))
    rbuffermanager.daemon = True
    rbuffermanager.start()

    sbuffermanager = threading.Thread(target = sendsbuffer, args = (server, sbuffer))
    sbuffermanager.daemon = True
    sbuffermanager.start()

    updatemanager = threading.Thread(target = waitforupdate, args = (cPlayer, server,))
    updatemanager.daemon = True
    updatemanager.start()

cPlayer.character.bounty = 1000
cPlayer.character.encumbrance = 100
cPlayer.character.attributes.agility = 37
cPlayer.character.attributes.endurance = 57

while True:    
    pass

    

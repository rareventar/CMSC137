from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle
import random
import json
import time
import random
from collections import deque
from server import createChatServer
import multiprocessing

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        # client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()



def foodSpawn():
    global foodSpawnQueue
    while True:
        # print(foodSpawnQueue)
        foodX = random.randrange(foodSize, windowWidth-foodSize)
        foodY = random.randrange(foodSize, windowHeight-foodSize)
        foodSpawnQueue.append([foodX, foodY, foodSize, foodSize])
        #window.blit(food, [foodX, foodY, foodSize, foodSize])
        #pygame.display.update()
        time.sleep(random.randint(1,5))
def handle_client(client):  # Takes client socket as argument.
    global count
    global foodSpawnQueue
    global clientsAddress
    global clientsPosition
    # print(client)
    strClient = str(client)
    name = client.recv(BUFSIZ)
    clientsPosition[count] = pickle.loads(name)
    clientsAddress[client] = pickle.loads(name)
    num = str(count)
    num = bytes(num, "utf8")
    client.send(num)
    count = count + 1
    food_something = Thread(target=foodSpawn)
    food_something.start()
    while True:
        msg = client.recv(BUFSIZ)
        msg = pickle.loads(msg)
        if msg[0] == "0":
            foodSpawnQueuePacket = pickle.dumps(foodSpawnQueue)
            msg[4] = foodSpawnQueuePacket
            # msg.pop(0)
            x = deque(msg)
            x.popleft()
            y = list(x)
            # print(msg)
            # print(pickle.loads(y[2]))
            clientsAddress[client] = y
            temp = 0
            for a in clientsAddress:
                clientsPosition[temp] = clientsAddress[a]
                # print(clientsPosition[temp])
                temp+=1
            broadcastall(pickle.dumps(clientsPosition))
        elif msg[0] == "1":
            # thing  = pickle.loads(msg[1])
            if msg[1] in foodSpawnQueue:
                foodSpawnQueue.remove(msg[1])
        elif msg[0] == "2":
            foodSpawnQueuePacket = pickle.dumps(foodSpawnQueue)
            msg[3] = foodSpawnQueuePacket
            clientsAddress[client] = msg
            temp = 0
            for a in clientsAddress:
                clientsPosition[temp] = clientsAddress[a]
                # print(clientsPosition[temp])
                temp+=1
            broadcastall(pickle.dumps(clientsPosition))
        else:
            client.send(bytes("q", "utf8"))
            client.close()
            # del clientsPosition[strClient]
            del clientsAddress [client]
            broadcast(bytes("someone has left the chat.","utf8"))
            break


def broadcastall(msg):
    global clientsAddress
    for sock in clientsAddress:
        sock.sendall(msg)

def broadcast(msg):  # prefix is for name identification.
    global clientsAddress
    for sock in clientsAddress:
        sock.sendall(msg)

def cserverThread():
    global HOST, PORT
    #    multiprocessing.Process(target = createChatServer(HOST,PORT+2000)).start()
    Thread(target = createChatServer(HOST,PORT+2000)).start()

clientsAddress = {}
clientsPosition = {}
addresses = {}
count  = 0

HOST = ''
PORT = 53000
BUFSIZ = 32768
ADDR = (HOST, PORT)
Thread(target = cserverThread).start()
print("ASDDDD")
windowWidth, windowHeight = (750, 450)
foodSize = 30
foodSpawnQueue = []
print("!!@###")
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
print(1233122)
# foodSpawn()
#if __name__ == "__main__":
SERVER.listen(5)
print("Game Waiting for connection...")
ACCEPT_THREAD = Thread(target=accept_incoming_connections)
ACCEPT_THREAD.start()
print('game thread start')
ACCEPT_THREAD.join()
SERVER.close()

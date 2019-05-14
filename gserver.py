from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle
import random
import json


def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        # client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    global count
    # print(client)
    strClient = str(client)
    name = client.recv(BUFSIZ)
    clientsPosition[count] = pickle.loads(name)
    clientsAddress[client] = pickle.loads(name)
    num = str(count)
    num = bytes(num, "utf8")
    client.send(num)
    count = count + 1
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("q", "utf8"):
            msg = pickle.loads(msg)
            # print(msg.values())
            clientsAddress[client] = msg
            for a in clientsPosition:
                clientsPosition[a] = msg
            broadcastall(pickle.dumps(clientsPosition))
        else:
            client.send(bytes("q", "utf8"))
            client.close()
            del clientsPosition[strClient]
            del clientsAddress [client]
            broadcast(bytes("someone has left the chat.","utf8"))
            break


def broadcastall(msg):
    for sock in clientsAddress:
        sock.sendall(msg)

def broadcast(msg):  # prefix is for name identification.

    for sock in clientsAddress:
        sock.send(msg)

clientsAddress = {}
clientsPosition = {}
addresses = {}
count  = 0

HOST = ''
PORT = 35000
BUFSIZ = 1024
ADDR = (HOST, PORT)
windowWidth, windowHeight = (750, 450)
foodSize = 30
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

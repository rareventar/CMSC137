from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}
SERVER = None
def accept_incoming_connections():
    global SERVER,addresses, clients
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!\n", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    global clients
    """Handles a single client connection."""
    BUFSIZ = 1024

    name = client.recv(BUFSIZ).decode("utf8")
    name = name.strip()
    welcome = 'Welcome %s! If you ever want to quit\n' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!\n" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("q", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("q", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat.\n" % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


def createChatServer(HOST, PORT):
    global SERVER
    BUFSIZ = 1024
    ADDR = ('localhost', PORT)
    
    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)
    SERVER.listen(5)
    print("Chat waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections, daemon=True)
    ACCEPT_THREAD.start()
    print('block2')
    ACCEPT_THREAD.join()
    print('block3')
    SERVER.close()
    print('block4')
    return

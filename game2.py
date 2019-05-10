import math
import pygame
import threading
import random
import time
import pickle
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from collections import deque
def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ)
            # msg_list.insert(tkinter.END, msg)
            # global clients = pickle.loads(msg)
            print(msg)
        except OSError:  # Possibly client has left the chat.
            break

def getAngle(x1,y1, x2,y2):
    angle = math.degrees(math.atan2(y2-y1,x2-x1))
    return angle

def rotate(x, y, mousePos, image):
    angle = getAngle(x, y, mousePos[0], mousePos[1])
    # Rotate the image (use the negative angle).
    rotated = pygame.transform.rotate(image, -angle + 90)
    rect = rotated.get_rect(center=(x, y))
    return rotated, rect

def translate(x, y, mousePos, boosted):
    if boosted:
        speed = 3.5
    else:
        speed = 2
    newX = newY = 0
    angle = getAngle(x, y, mousePos[0], mousePos[1])
    angle = math.radians(angle)
    newX = x + (speed * math.cos(angle))
    newY = y + (speed * math.sin(angle))
    return newX, newY

def spawnFood():
    while alive:
        msg = "spawnFood"
        client_socket.send(bytes(msg, "utf8"))
        msg = client_socket.recv(BUFSIZ).decode("utf8")
        # print(msg)
        msg = msg.split()
        foodX = int(msg[0])
        foodY = int(msg[1])
        # foodX = random.randrange(foodSize, windowWidth-foodSize)
        # foodY = random.randrange(foodSize, windowHeight-foodSize)
        foodSpawnQueue.append([foodX, foodY, foodSize, foodSize])
        #window.blit(food, [foodX, foodY, foodSize, foodSize])
        #pygame.display.update()
        time.sleep(random.randint(1,5))

def send():  # event is passed by binders.
    """Handles sending of messages."""
    # msg = my_msg.get()
    # name = input("name: ")
    # client_socket.send(bytes(name, "utf8"))

    pygame.init()
    maxSnakeLength = 1
    gray = (30, 30, 30)

    windowWidth, windowHeight = (750, 450)

    x = windowWidth * 0.5
    y = windowHeight * 0.5
    snakeBody = deque()
    snakeList = tuple(snakeBody)
    hashable = hash(snakeList)

    radius = 10
    connection = True

    window = pygame.display.set_mode((windowWidth, windowHeight))

    clock = pygame.time.Clock()

    snakehead = pygame.image.load('Slither_snakehead.png')
    snakehead = pygame.transform.scale(snakehead, (40,40))
    food = pygame.image.load('food.png')
    food = pygame.transform.scale(food, (32, 32))


    data = {x,y,hashable}
    data = pickle.dumps(data)
    client_socket.send(bytes(data))
    count = int(client_socket.recv(BUFSIZ).decode("utf8"))
    threading.Thread(target=spawnFood, daemon=True).start()
    receive_thread = Thread(target=receive)
    receive_thread.start()
    while connection:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        mousex, mousey = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            boosted = True
        else:
            boosted = False
        x, y = translate(x, y, (mousex, mousey), boosted)
        if x > windowWidth:
            x = windowWidth - 10
        if x < 0:
            x = 10
        if y > windowHeight:
            y = windowHeight - 10
        if y < 0:
            y = 10

        window.fill(gray)
        rotimage, rect = rotate(x, y, (mousex, mousey), snakehead)
        window.blit(rotimage, rect)

        if len(foodSpawnQueue) != 0:
            for foodItem in foodSpawnQueue:
                window.blit(food, foodItem)

        #check if snake collided with food
        ate = False
        for foodItem in foodSpawnQueue:
            if rect.colliderect(foodItem):
                ate = True
                eaten = foodItem
                maxSnakeLength += 20
        #remove/eat food
        if ate:
            foodSpawnQueue.remove(eaten)

        if len(snakeBody) < maxSnakeLength:
            snakeBody.appendleft((x,y))
        else:
            dummy = snakeBody.pop()
            snakeBody.appendleft((x,y))

        for center in snakeBody:
            pygame.draw.circle(window, (30,200,30), [round(center[0]), round(center[1])], radius)
        window.blit(rotimage, rect)
        pygame.display.update()
        clock.tick(60)
        snakeList = tuple(snakeBody)
        # print(snakeList)
        hashable = hash(snakeList)
        data = {x,y,hashable}
        data = pickle.dumps(data)
        client_socket.send(bytes(data))

    gameloop()
    pygame.quit()

HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 31000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)
alive = True
foodSpawnQueue = []
foodSize = 30
count = -1
clients = {}



client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


send_thread = Thread(target = send)
send_thread.start()

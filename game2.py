import math
import pygame
import threading
import random
import time
import pickle
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from collections import deque
from client import createChatClient
import multiprocessing 
def receive():
    global foodSpawnQueue
    global clients
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ)
            # msg_list.insert(tkinter.END, msg)
            clients.clear()
            msg  = pickle.loads(msg)
            clients = msg.copy()
            # print(pickle.loads(msg))
            # for a in clients:
            # msg = pickle.loads(msg)
            foodSpawnQueue = pickle.loads(msg[count][3])
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

# def spawnFood():
#     while alive:
#         foodX = random.randrange(foodSize, windowWidth-foodSize)
#         foodY = random.randrange(foodSize, windowHeight-foodSize)
#         foodSpawnQueue.append([foodX, foodY, foodSize, foodSize])
#         #window.blit(food, [foodX, foodY, foodSize, foodSize])
#         #pygame.display.update()
#         time.sleep(random.randint(1,5))

def send():  # event is passed by binders.
    """Handles sending of messages."""
    # msg = my_msg.get()
    # name = input("name: ")
    # client_socket.send(bytes(name, "utf8"))
    global clients
    pygame.init()
    maxSnakeLength = 1
    gray = (30, 30, 30)
    green = (0,200,0)
    white = (255,255,255)
    black = (0,0,0)

    x = windowWidth * 0.75
    y = windowHeight * 0.75
    snakeBody = deque()
    snakeList = pickle.dumps(snakeBody)
    smallFont = pygame.font.SysFont("arial", 25)
    medFont = pygame.font.SysFont("arial", 50)
    largeFont = pygame.font.SysFont("arial", 80)


    global foodSpawnQueue
    radius = 10
    connection = True

    window = pygame.display.set_mode((windowWidth, windowHeight))

    clock = pygame.time.Clock()

    def text_objects(text, color, size):
        if size == "small":
            text_surface = smallFont.render(text, True, color)
        elif size == "medium":
            text_surface = medFont.render(text, True, color)
        elif size == "large":
            text_surface = largeFont.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def screenText(msg, color, y_displace=0, size="small"):
        text_surf, text_rect = text_objects(msg, color, size)
        text_rect.center = (windowWidth / 2), (windowHeight / 2) + y_displace
        window.blit(text_surf, text_rect)

    snakehead = pygame.image.load('Slither_snakehead.png')
    snakehead = pygame.transform.scale(snakehead, (40,40))
    food = pygame.image.load('food.png')
    food = pygame.transform.scale(food, (32, 32))

    foodSpawnQueuePacket = pickle.dumps(foodSpawnQueue)

    data = ["2", x,y,snakeList, foodSpawnQueuePacket]
    data = pickle.dumps(data)
    client_socket.send(bytes(data))
    count = int(client_socket.recv(BUFSIZ).decode("utf8"))
    # threading.Thread(target=spawnFood, daemon=True).start()
    receive_thread = Thread(target=receive)
    receive_thread.start()
    def instructions():
        inst = True
        window.fill(white)
        screenText("Instruction", black, -100, "large")
        screenText("The objective of the game is to eat the blue orbs.",black, -30)
        screenText("Your snake follows the mouse.", black,10)
        screenText("If you run into the edges, you die!",black, 50)
        screenText("Press B to go back or Q to quit.", black,180)
        pygame.display.update()

        while inst:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        inst = False

                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
        introloop()
        clock.tick(5)
    def introloop():
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        instructions()
                    if event.key == pygame.K_p:
                        intro = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
            window.fill(white)
            screenText("Welcome to Slither!", green, -100, "large")
            #screenText("The objective of the game is to the blue orbs",black, -30)
            #screenText("The more apples you eat, the longer you get", black,10)
            #screenText("If you run into other snakes or the edges, you die!",black, 50)
            screenText("Press P to play, I for instructions or Q to quit.", black,10)
            pygame.display.update()
        return False
    intro = True
    while connection:
        if intro:
            intro = introloop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        mousex, mousey = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            boosted = True
        else:
            boosted = False
        x, y = translate(x, y, (mousex, mousey), boosted)
        if x > windowWidth-10:
            pygame.quit()
        if x < 10:
            pygame.quit()
        if y > windowHeight-10:
            pygame.quit()
        if y < 10:
            pygame.quit()

        window.fill(gray)
        rotimage, rect = rotate(x, y, (mousex, mousey), snakehead)
        window.blit(rotimage, rect)

        # print(foodSpawnQueue)
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
            # eaten = pickle.dumps(eaten)
            data = ["1", eaten]
            data = pickle.dumps(data)
            client_socket.send(bytes(data))

        if len(snakeBody) < maxSnakeLength:
            snakeBody.appendleft((x,y))
        else:
            dummy = snakeBody.pop()
            snakeBody.appendleft((x,y))
        localClients = clients.copy()
        for player in localClients:
            # print(localClients[player][2])
            if type(localClients[player][2]) is float:
                body = pickle.loads(localClients[player][3])
            else:
                body = pickle.loads(localClients[player][2])
            for points in body:
                pygame.draw.circle(window,(30,200,30), [round(localClients[player][0]), round(localClients[player][1])], radius)
        #for center in snakeBody:
        #    pygame.draw.circle(window, (30,200,30), [round(center[0]), round(center[1])], radius)
        window.blit(rotimage, rect)
        pygame.display.update()
        clock.tick(60)
        snakeList = pickle.dumps(snakeBody)
        foodSpawnQueuePacket = pickle.dumps(foodSpawnQueue)
        data = ["0", x,y,snakeList,foodSpawnQueuePacket]
        data = pickle.dumps(data)
        client_socket.send(bytes(data))

    #    gameloop()
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
count = 0
clients = {}
windowWidth, windowHeight = (750, 450)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

send_thread = Thread(target = send)
send_thread.start()
#multiprocessing.Process(target = createChatClient(HOST, PORT+2000)).start()
Thread(target = createChatClient(HOST, PORT+2000)).start()

import math
import pygame
import threading
import random
import time
from collections import deque

pygame.init()

gray = (30, 30, 30)

windowWidth, windowHeight = (750, 450)
window = pygame.display.set_mode((windowWidth, windowHeight))

clock = pygame.time.Clock()

snakehead = pygame.image.load('Slither_snakehead.png')
snakehead = pygame.transform.scale(snakehead, (40,40))
food = pygame.image.load('food.png')
food = pygame.transform.scale(food, (32, 32))
foodSize = 30

smallFont = pygame.font.SysFont("arial", 25)
medFont = pygame.font.SysFont("arial", 50)
largeFont = pygame.font.SysFont("arial", 80)

maxSnakeLength = 0
radius = 10
alive = True
foodSpawnQueue = []
def spawnFood():
    while alive:
        foodX = random.randrange(foodSize, windowWidth-foodSize)
        foodY = random.randrange(foodSize, windowHeight-foodSize)
        foodSpawnQueue.append([foodX, foodY, foodSize, foodSize])
        #window.blit(food, [foodX, foodY, foodSize, foodSize])
        #pygame.display.update()
        time.sleep(random.randint(1,5))

def getAngle(x1,y1, x2,y2):
    angle = math.degrees(math.atan2(y2-y1,x2-x1))
    return angle

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

def gameloop():
    intro = True    
    green = (0,200,0)
    white = (255,255,255)
    black = (0,0,0)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        window.fill(white)
        screenText("Welcome to Slither", green, -100, "large")
        screenText("The objective of the game is to the blue orbs",black, -30)
        screenText("The more apples you eat, the longer you get", black,10)
        screenText("If you run into other snakes or the edges, you die!",black, 50)
        screenText("Press C to play, P to pause, or Q to quit.", black,180)
        pygame.display.update()

    x = windowWidth * 0.5
    y = windowHeight * 0.5

    snakeBody = deque()
    maxSnakeLength = 1

    threading.Thread(target=spawnFood, daemon=True).start()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        mousex, mousey = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            boosted = True
        else:
            boosted = False
        x, y = translate(x, y, (mousex,mousey), boosted)
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
            snakeBody.appendleft([x,y])
        else:
            dummy = snakeBody.pop()
            snakeBody.appendleft([x,y])
        
        for center in snakeBody:
            pygame.draw.circle(window, (30,200,30), [round(center[0]), round(center[1])], radius)
        window.blit(rotimage, rect)
        pygame.display.update()
        clock.tick(60)


gameloop()
pygame.quit()
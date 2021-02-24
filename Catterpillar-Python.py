#Caterpillar Python

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

pygame.display.set_caption("Catterpillar")

class cube(object):
    
    rows = 20
    w = 500
    
    def __init__(self,start,dirnx=1,dirny=0,color=(0,255,0)):
        self.pos = start
        self.dirnx = 1 #facing right
        self.dirny =0
        self.color = color
        
    def move(self, dirnx, dirny):
        self.dirnx =dirnx
        self.dirny = dirny
        self.pos = (self.pos[0]+self.dirnx , self.pos[1]+self.dirny) # change our position     

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface,self.color, (i*dis+1,j*dis+1,dis-2,dis-2))
        # By multiplying the row and column value of our cube by the width and height of each cube we can determine where to draw it
        
        if eyes :
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius) 
        
        

class Caterpillar(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos) #head
        self.body.append(self.head) #updating
        self.dirnx = 0
        self.dirny = 1
        """
        the way things work is that the top left coordinate is 0,0
        so to go left x must be -1 ; Right x must be 1
        """
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx =-1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx ,self.dirny]
                    #Above code : turns is a dictionary, head.pos is a key and the RHS is the value stored
                
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx ,self.dirny]
                    
                elif keys[pygame.K_UP]:
                    self.dirnx =0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx ,self.dirny]
                    
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx ,self.dirny]
                    
        #moving cube 
        for i,c in enumerate(self.body):
            #c is each block
            p = c.pos[:]  # This stores the cubes position on the grid
            if p in self.turns:  # If the cubes current position is one where we turned
                turn = self.turns[p]  # Get the direction we should turn
                c.move(turn[0],turn[1])  # Move our cube in that direction
                if i == len(self.body)-1:  # If this is the last cube in our body remove the turn from the dict
                    self.turns.pop(p)
            else:  # If we are not turning the cube
                # If the cube reaches the edge of the screen we will make it appear on the opposite side
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)  # If we haven't reached the edge just move in our current direction
    
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx , dy = tail.dirnx,tail.dirny

        # We need to know which side of the snake to add the cube to.
        # So we check what direction we are currently moving in to determine if we
        # need to add the cube to the left, right, above or below.
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
        
        # We then set the cubes direction to the direction of the snake.
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        

    def draw(self, surface):
        for i , c in enumerate(self.body):
            if i==0:
                c.draw(surface, True) #drawing eyes for the head
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w//rows

    x=0
    y=0
    for row in range(rows):
        x = x+sizeBtwn
        y = y+sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0), (x,w))
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y))

        

def redrawWindow(surface):
    global rows,width,s,snack
    surface.fill((0,0,0))
    cp.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows,surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body  # Get all the posisitons of cubes in our snake

    while True:  # Keep generating random positions until we get a valid one
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            # This wll check if the position we generated is occupied by the snake
            continue
        else:
            break
        
    return (x,y)
        


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost",True)
    root.withdraw()
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except:
        pass


def main():
    #window size. Rows and column
    global width,rows,cp,snack
    width =500
    rows = 20

    win = pygame.display.set_mode((width , width))
    cp= Caterpillar((255,0,0),(10,10))
    snack = cube(randomSnack(rows,cp), color = (255,0,0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50) #delays the game by 50milli seconds; lower the number,the faster
        clock.tick(10) #fps i.e in a sec the snake moves 10 blocks; lower the number,the slower
        #the above two commands together makes it comfortable speed to play the game in
        cp.move()
        if cp.body[0].pos == snack.pos:
             cp.addCube()
             snack = cube(randomSnack(rows,cp), color = (255,0,0))

        for x in range(len(cp.body)):
            if cp.body[x].pos in list(map(lambda z:z.pos,cp.body[x+1:])): # This will check if any of the positions in our body list overlap
                print('Score: ', len(cp.body))
                message_box('You Lost!', (f'Score: { len(cp.body)}'))
                cp.reset((10,10))
                break


        redrawWindow(win)

main()



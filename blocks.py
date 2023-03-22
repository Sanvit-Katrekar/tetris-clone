import random

import pygame

WIDTH = 500

class Block(pygame.sprite.Sprite):
    '''Creates a 4x4 block'''

    ''' [0]  [1]  [2]  [3]
        [4]  [5]  [6]  [7]
        [8]  [9]  [10] [11]
        [12] [13] [14] [15] '''

    def __init__(self, x, y):

        super().__init__()
        
        self.x = x
        self.y = y

        self.width = 25
        self.height = 25

        self.vel = 25

        blocks = [[1, 5, 9, 13], #Straight line
                  [2, 6, 10, 9], #J shape
                  [2, 6, 10, 11],#L shape
                  [2, 6, 10, 5], #T shape
                  [9, 5, 6, 2],  #Z shape
                  [1, 5, 6, 10], #S shape
                  [5, 6, 9, 10]  #Box
                  ]

        colours = [(96, 255, 16), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        
        self.blockType = random.choice(blocks)
        self.colour = random.choice(colours)
        self.rotation = random.randrange(0, 360, 90)

        temp = [1 if i in self.blockType else 0 for i in range(4*4)]
        self.matrix = [temp[i:(i+4)] for i in range(0, len(temp), 4)]

        self.collided = False

        for i in range(0, self.rotation + 1, 90):
            self.rotate()

        self.getRectangles()

            

    def rotate(self):

        if self.collided: return
        
        self.matrix = [
            [self.matrix[i][j] for i in range(len(self.matrix)-1, -1, -1)]
            for j in range(len(self.matrix))]

        self.getRectangles()

    def correctRotation(self):

        self.matrix = [
            [self.matrix[j][i] for j in range(len(self.matrix[0]))]
            for i in range(len(self.matrix) -1, -1, -1)]
        
        self.getRectangles()

    def getRectangles(self):

        self.rects = []

        for i in range(len(self.matrix)):

            for j in range(len(self.matrix[0])):

                draw = self.matrix[i][j]
                
                if draw:
                    rect = pygame.Rect(self.x + i*self.width, self.y +j*self.height, self.width, self.height)
                    self.rects.append(rect)


    def update(self):

        if self.collided: return

        for rect in self.rects:
            rect.y += self.vel

        self.y += self.vel

    def adjustment(self):

        self.y -= self.vel

        for rect in self.rects:
            rect.y -= self.vel
            
            

    def isCollision(self, spriteGroup):

        for sprite in spriteGroup:

            for rect in sprite.rects:

                for blockRect in self.rects:

                    if blockRect.colliderect(rect):

                        return True

        
        




import pygame

from blocks import Block

import sys

import random

pygame.init()

WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Tetris!')

clock = pygame.time.Clock()

floor = pygame.Rect((0, 0, WIDTH, 25))
floor.bottomleft = (0, HEIGHT)
floorColour = (255, 0, 0)

FONT = pygame.font.SysFont('Times New Roman', 30)
FONT2 = pygame.font.SysFont('Times New Roman', 50)

def terminateProgram():

    pygame.quit()
    sys.exit()

def keyPressCheck():
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q: terminateProgram()
            return True
        elif event.type == pygame.QUIT: terminateProgram()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            return True

    return False


def gameOver():

    redrawWindow(screen)

    screen.fill((0, 0, 0))

    text = FONT2.render('Game Over!', True, (255, 255, 255))
    screen.blit(text, (WIDTH//4, 0))

    text = FONT2.render(f'Final Score: {score}', True, (255, 255, 255))
    screen.blit(text, (WIDTH//5, 100))

    text = FONT2.render('High Scores:', True, (255, 0, 0))
    screen.blit(text, (WIDTH//5 + 25, 150))
    
    text = FONT.render('PRESS Q TO QUIT', True, (255, 255, 255))
    screen.blit(text, (125, HEIGHT - HEIGHT//5))
        
    highestScores, newScore = highScore(score)

    if newScore:
        text = FONT.render('New high score!', True, (0, 255, 0))
        screen.blit(text, (125, 375))

    for i in range(len(highestScores)):
        text = FONT2.render(f'{i+1}. {highestScores[i]}', True, (255, 255, 255))
        screen.blit(text, (WIDTH//3, HEIGHT//3 + i * 50 + 50))

    pygame.display.update()

    pygame.time.delay(2000)

    while not keyPressCheck():
        pass
            

def highScore(SCORE):

    import pickle

    data = None

    with open('Highscore.dat', 'rb') as f:
        try: data = pickle.load(f) 
        except: pass

    newScore = False

    with open('Highscore.dat', 'wb') as f:
        if not data:
            data = [SCORE, 0, 0]
            pickle.dump(data, f)

        elif SCORE not in data:
            for i in range(len(data)):
                if SCORE > data[i]:
                    data.insert(i, SCORE)
                    if len(data) > 3: data.pop()
                    newScore = True
                    break
            pickle.dump(data, f)

    return data, newScore


def clearRow():

    for y in range(HEIGHT - 25, 0, -25):


        all_rects = []
        for sprite in collSprites:
            all_rects.extend([rect for rect in sprite.rects])
            
        for x in range(0, WIDTH, 25):

            checkRect = pygame.Rect(x, y, 25, 25)
            checkRect.bottom = y

            clear = any([checkRect.colliderect(rect) for rect in all_rects])

            if not clear:
                break
        
                
        else:

            for sprite in collSprites:
                for rect in sprite.rects:
                    if rect.bottom == y:
                        sprite.kill()
                        break

            for sprite in collSprites:
                for rect in sprite.rects:
                    if rect.bottom < y:
                        sprite.collided = False

def adjustGrid():

    for sprite in collSprites:

        coll_sprites = [collsprite for collsprite in collSprites if collsprite != sprite]

        floorCheck = any([floor.colliderect(rect) for rect in sprite.rects])

        if floorCheck or sprite.isCollision(coll_sprites):

            sprite.adjustment()
        
            sprite.collided = True
           

def redrawWindow(window):

    window.fill((0, 0, 0))

    text = FONT.render(f'Score: {score}', True, (255, 255, 255))
    window.blit(text, (10, 0))

    for rect in block.rects:
        pygame.draw.rect(window, block.colour, rect)

    for sprite in collSprites:

        for rect in sprite.rects:
            
            pygame.draw.rect(window, sprite.colour, rect)
        

    pygame.draw.rect(window, floorColour, floor)
        
    block.update()
    collSprites.update()
    pygame.display.update()

def menuScreen():

    blocks = [Block(100, -50), Block(300, -50)]

    count = 0

    while not keyPressCheck():

        screen.fill((0, 0, 0))

        for i in range(len(blocks)):
            
            for rect in blocks[i].rects:
                pygame.draw.rect(screen, blocks[i].colour, rect)

            if count % 200 == 0: blocks[i].update()
                
            floorCollide = any([floor.colliderect(rect) for rect in blocks[i].rects])
            if floorCollide:
                xPos = random.randrange(0, 500, blocks[i].vel * 4)
                blocks[i] = Block(xPos, -50)

        pygame.draw.rect(screen, floorColour, floor)

        text = FONT2.render('TETRIS!', True, (255, 255, 255))
        screen.blit(text, (WIDTH//4 + 30, HEIGHT//3))

        text = FONT.render('PRESS ANY KEY TO PLAY', True, (255, 255, 255))
        screen.blit(text, (70, HEIGHT - HEIGHT//5))
        
        pygame.display.update()

        count += 1
    
menuScreen()

done = True

fps = 120

SPEED = 20

while done:
    block = Block(200, -50)
    collSprites = pygame.sprite.Group()

    run = True

    score = 0
    
    count = 0
    while run:

        count += 1

        clock.tick(fps)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
##                done = False
##                run = False
                terminateProgram() 
                
            elif event.type == pygame.KEYDOWN:

                xSpeed = 0
                
                if event.key == pygame.K_SPACE:

                    block.rotate()

                    borderCollision = any([rect.left <= 0 or rect.right >= WIDTH for rect in block.rects])

                    if borderCollision or block.isCollision(collSprites): block.correctRotation()
                
                if event.key in [pygame.K_a, pygame.K_LEFT] :
                    borderCollision = any([rect.left <= 0 for rect in block.rects])
                    if not borderCollision: xSpeed = -block.vel

                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    borderCollision = any([rect.right >= WIDTH for rect in block.rects])
                    if not borderCollision: xSpeed = block.vel

                elif event.key == pygame.K_c: print(collSprites)

                block.x += xSpeed
                for rect in block.rects:               
                    rect.x += xSpeed

                if block.isCollision(collSprites):
                    block.x -= xSpeed
                    for rect in block.rects:               
                        rect.x -= xSpeed
                    


        floorCollide = any([floor.colliderect(rect) for rect in block.rects])
        
        if floorCollide or block.isCollision(collSprites):

                block.adjustment()
            
                block.collided = True

                score += 10
                
                collSprites.add(block)
                
                block = Block(225, -25)
                
                if block.isCollision(collSprites):

                    gameOver()
                    
                    break

        adjustGrid()
        

        if count % SPEED == 0:
            redrawWindow(screen)
            clearRow()
            count = 0













import pygame
import sys
import os

'''OBJECTS'''
# put classes & functions here

class Player(pygame.sprite.Sprite):
    #spawn a player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.momentumX = 0 #move along X
        self.momentumY = 0 #move along Y
        self.image = pygame.image.load(os.path.join('images', 'hero.png')).convert()
        self.image.convert_alpha() #opimise for alpha
        self.image.set_colorkey(alpha) #set alpha
        self.rect = self.image.get_rect()
        
    def control(self, x, y):
        #control player movement
        self.momentumX += x
        self.momentumY += y

    def update(self):
        #update sprite position
        currentX = self.rect.x
        nextX = currentX + self.momentumX
        self.rect.x = nextX

        currentY = self.rect.y
        nextY = currentY + self.momentumY
        self.rect.y = nextY

    



        
'''SETUP'''
# code runs once
screenX = 960  #screen width
screenY = 720  #screen height
alpha = (0, 0, 0)
black = (1, 1, 1)
white = (255, 255, 255)
fps = 40 #frame rate
afps = 4 #animation cycles
clock = pygame.time.Clock ( )
pygame.init ( )

main = True

screen = pygame.display.set_mode ( [screenX,  screenY] )
backdrop = pygame.image.load (os.path.join ( 'images',   'stage.png' ) ) .convert ( )
backdropRect = screen.get_rect ( )

player = Player() #spawn player
player.rect.x = 0 #go to x
player.rect.y = 0 #go to y
movingsprites = pygame.sprite.Group()
movingsprites.add(player)
movesteps = 10 #how fast to move







'''MAIN LOOP'''
# code runs many times

while main == True:
    for event in pygame.event.get ( ) :
        if event.type == pygame.QUIT:
            pygame.quit ( ) ;  sys.exit ( )
            main = False

        if event.type == pygame.KEYUP :
            if event.key == ord ( 'q' ):
                pygame.quit ( )
                sys.exit ( )
                main = False

            if event.key == pygame.K_LEFT or event.key == ord ('a'):
                print('left stop')
                player.control(movesteps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord ('d'):
                print('right stop')
                player.control(-movesteps, 0)
            if event.key == pygame.K_UP or event.key == ord ('w'):
                print('jump stop')


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord ('a'):
                print ('left')
                player.control(-movesteps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord ('d'):
                print ('right')
                player.control(movesteps, 0)
            if event.key == pygame.K_UP or event.key == ord ('w'):
                print ('jump')
                




    screen.blit (backdrop,  backdropRect)

    player.update() #update player position
    movingsprites.draw(screen) #draw player
    pygame.display.flip()
    clock.tick(fps)

  



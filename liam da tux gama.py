


import pygame #load pygame keywords
import sys
import os
import pygame.freetype #load fonts

'''OBJECTS'''
# put classes & functions here

def stats(score):
    #display text, 1, color (rgb)
    text_score = myfont.render("Score: "+str(score), 1, (250,147,248))
    screen.blit(text_score, (4,4))

class Player(pygame.sprite.Sprite):
    #spawn a player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.momentumX = 0 #move along X
        self.momentumY = 0 #move along Y

        #gravity variables
        self.collide_delta = 0
        self.jump_delta = 6
        self.image = pygame.image.load(os.path.join('images', 'hero.png')).convert()
        self.image.convert_alpha() #opimise for alpha
        self.image.set_colorkey(alpha) #set alpha
        self.rect = self.image.get_rect()

        self.score = 0 #set score
        self.damage = 0 #player is hit

    def control(self, x, y):
        #control player movement
        self.momentumX += x
        self.momentumY += y

        

    def update(self, enemy_list, platform_list, loot_list):
        #update sprite position
        currentX = self.rect.x
        nextX = currentX + self.momentumX
        self.rect.x = nextX

        currentY = self.rect.y
        nextY = currentY + self.momentumY
        self.rect.y = nextY

        #gravity
        if self.collide_delta < 6 and self.jump_delta < 6:
            self.jump_delta = 6*2
            self.momentumY -=33 #how high to jump

            self.collide_delta +=6
            self.jump_delta += 6



        #collisions
        loot_hit_list = pygame.sprite.spritecollide(self, loot_list, False)
        for loot in loot_hit_list:
            loot_list.remove(loot)
            self.score += 1
            
        enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        '''for enemy in enemy_hit_list:
            self.score -= 1
            print(self.score)'''

        if self.damage == 0:
            for enemy in enemy_hit_list:
                if not self.rect.contains(enemy):
                    self.damage = self.rect.colliderect(enemy)
                    print(self.score)


        if self.damage == 1:
            idx = self.rect.collidelist(enemy_hit_list)
            if idx == -1:
                self.damage = 0 #set damage back to 0
                self.score -= 1 #subtract 1 hp

                    

        block_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
        if self.momentumX > 0:
            for block in block_hit_list:
                self.rect.y = currentY
                self.rect.x = currentX+9
                self.momentumY = 0
                self.collide_delta = 0 #stop jumping

        if self.momentumY > 0:
            for block in block_hit_list:
                self.rect.y = currentY
                self.momentumY = 0
                self.collide_delta = 0 #stop jumping
                
    def jump (self, platform_list):
        self.jump_delta = 0
        
    def gravity(self):
        self.momentumY += 3.2  #how fast player falls

        if self.rect.y > 960 and self.momentumY >= 0:
            self.momentumY = 0
            self.rect.y = 0
            self.rect.x = 0

class Throwable(pygame.sprite.Sprite):
    #Spawn throwable object
    def __init__(self,x,y,img,throw):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img))
        self.image.convert_alpha()
        self.image.set_colorkey(alpha)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.firing = throw

    def update(self,screenY):
        #throw physics
        if self.rect.y < screenY: #vertical axis
            self.rect.x += 15 #how fast it moves forward
            self.rect.y += 5 #how fast it falls
        else:
            self.kill() #remove throwable object
            self.firing = 0 #free up firing slot
        

class Enemy(pygame.sprite.Sprite):
    #spawn an enemy
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img))
        self.image.convert_alpha()
        self.image.set_colorkey(alpha)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0 #counter variable

    def move(self):
        #enemy movement
        if self.counter >= 0 and self.counter <= 30:
            self.rect.x += 2
        elif self.counter >= 30 and self.counter <= 60:
            self.rect.x -= 2
        else:
            self.counter = 0
            print('reset')

        self.counter += 1

    def update(self, firepower, enemy_list):
        #detect firepower collision
        fire_hit_list = pygame.sprite.spritecollide(self, firepower, False)
        for fire in fire_hit_list:
            enemy_list.remove(self)


class Platform(pygame.sprite.Sprite):
    #x location, y location, img width, img height, img file)
    def __init__(self,xloc,yloc,imgw, imgh, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([imgw, imgh])
        self.image.convert_alpha()
        self.image.set_colorkey(alpha)
        self.blockpic = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc

        #paint image into blocks
        self.image.blit(self.blockpic,(0,0),(0,0,imgw,imgh))

        
    def level1():
        #create level 1
        platform_list = pygame.sprite.Group()
        block = Platform(0, 591, 500, 77,os.path.join('images','block0.png'))
        platform_list.add(block) #after each block

        block = Platform(500, 200, 500, 77,os.path.join('images','block0.png'))
        platform_list.add(block) #after each block

        block = Platform(700, 600, 500, 77,os.path.join('images','block0.png'))
        platform_list.add(block) #after each block

        return platform_list #at end of function level1


    def loot1():
        #loot level1
        loot_list = pygame.sprite.Group()
        loot = Platform(450, 572, 175, 86, os.path.join('images', 'loot.png'))
        loot_list.add(loot)

        return loot_list #at end of function loot1



        
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
pygame.font.init() #start freetype

font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fonts", "amazdoom.ttf")
font_size = 64
myfont = pygame.font.Font(font_path, font_size)


main = True

screen = pygame.display.set_mode ( [screenX,  screenY] )
backdrop = pygame.image.load (os.path.join ( 'images',   'stage.png' ) ) .convert ( )
backdropRect = screen.get_rect ( )

platform_list = Platform.level1() #set stage to Level 1
loot_list = Platform.loot1() #set loot to Level 1


player = Player() #spawn player
player.rect.x = 0 #go to x
player.rect.y = 0 #go to y
movingsprites = pygame.sprite.Group()
movingsprites.add(player)

fire = Throwable(player.rect.x, player.rect.y, 'throw.png', 0)
firepower = pygame.sprite.Group()

movesteps = 10 #how fast to move

forwardX = 600 #when to scroll
backwardX = 150 #when to scroll

#enemy code
enemy = Enemy(300,250, 'enemy.png') #spawn enemy
enemy_list = pygame.sprite.Group() #create enemy group
enemy_list.add(enemy) #add enemy to group                 







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
            if event.key == pygame.K_SPACE:
                if not fire.firing:
                    fire = Throwable(player.rect.x, player.rect.y, 'throw.png', 1)
                    firepower.add(fire)


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord ('a'):
                print ('left')
                player.control(-movesteps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord ('d'):
                print ('right')
                player.control(movesteps, 0)
            if event.key == pygame.K_UP or event.key == ord ('w'):
                print ('jump')
                player.jump(platform_list)

    #scroll world forward
    if player.rect.x >= forwardX:
        scroll = player.rect.x - forwardX
        player.rect.x = forwardX
        for platform in platform_list:
            platform.rect.x -= scroll

        for enemy in enemy_list:
             enemy.rect.x -= scroll

        for loot in loot_list:
            loot.rect.x -= scroll

    #scroll world backward
    if player.rect.x <+ backwardX:
        scroll = min(1,  (backwardX - player.rect.x))
        player.rect.x = backwardX
        for platform in platform_list:
            platform.rect.x += scroll

        for enemy in enemy_list:
            enemy.rect.x += scroll

        for loot in loot_list:
            loot.rect.x += scroll
            
    
                




    screen.blit (backdrop,  backdropRect)
    
    platform_list.draw(screen) #draw platforms on screen
    player.gravity()  #check gravity
    player.update(enemy_list, platform_list, loot_list) #update player position
    movingsprites.draw(screen) #draw player
    
    enemy_list.draw(screen) #refresh enemies
    enemy.move() # move enemy sprite

    if fire.firing:
        fire.update(screenY)
        firepower.draw(screen)
        enemy_list.update(firepower, enemy_list) #update enemy

    loot_list.draw(screen) #refresh loot

    stats(player.score) #draw text

    pygame.display.flip()
    clock.tick(fps)

  



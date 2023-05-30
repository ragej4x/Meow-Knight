import csv
import math


   

#animate = animationClass()


class playerClass():
    def __init__(self):
        self.x = 0
        self.y = 700

        self.speed = 2
        self.jump = False
        self.jumpVel = 15
        self.onGround = False
        self.gravity = 5
        self.jumpCd = True
        self.jumpCounter = 0

        self.white = (200, 200, 200)
        self.red = (200, 0, 0)
        self.green = (0, 200, 0)
        self.blue = (0, 0, 200)

        self.Left = False
        self.Right = False


    def update(self, pg, window):
        self.catRect = pg.draw.rect(window, self.red, (self.x - camera.cameraX + 3, self.y - camera.cameraY + 3, 10,15),1)
        self.dx , self.dy = 0, 0
        
        
    def updateAnimation(self, pg, window, keyinput):

        if self.Left == True and not keyinput[pg.K_a] and not keyinput[pg.K_d]:
            animate.idleAnimationLeft(pg, window)
            
        if self.Right == True and not keyinput[pg.K_a] and not keyinput[pg.K_d]:
            animate.idleAnimationRight(pg, window)

        if keyinput[pg.K_a]:
            animate.runAnimationLeft(pg, window)

        if keyinput[pg.K_d]:
            animate.runAnimationRight(pg, window)

        if self.jump == True and self.Left == True and not keyinput[pg.K_a] and not keyinput[pg.K_d]:
            animate.jumpAnimationLeft(pg, window)

        if self.jump == True and self.Right == True and not keyinput[pg.K_a] and not keyinput[pg.K_d]:
            animate.jumpAnimationRight(pg, window) 

        
        
    def movement(self, pg, keyinput):

        if keyinput[pg.K_a]:
            self.dx -= self.speed
            self.Left = True
            self.Right = False

        if keyinput[pg.K_d]:
            self.dx += self.speed 
            self.Right = True
            self.Left = False    

        if keyinput[pg.K_w] and self.jumpCd == True and self.onGround == True:
            self.jump = True
            self.jumpCd = False
            self.jumpCounter = 0


        if self.jump == True:
            self.dy -= self.jumpVel
            self.jumpVel -= 0.5
            self.speed = 2
            
        else:
            self.speed = 3
            

        
        if self.jumpVel < 0 and self.onGround == True:
            self.jump = False
            self.jumpVel = 15
            self.onGround = False
                            
            
        #print(self.jumpVel)
            

        self.dy += self.gravity
        if self.dy > self.gravity:
            self.dy = self.gravity

        #self.dy += self.y
        self.gravity = 5
        #print(self.jumpCounter)

        #JUMP COOLDOWN
        self.jumpCounter += 0.3
        if self.jumpCounter > 10:
            self.jumpCd = True

        if self.jumpCounter > 10:
            self.jumpCounter = 10
        
        #print(self.onGround)



    def mapFunc(self, pg, window, keyinput):

        with open("data/map/mapData/data_1.txt") as data:
            
            #self.tile.fill(0)
            csv_reader = csv.reader(data, delimiter=',')
            y = 0
            for row in csv_reader:
                x = -1
                for column in range(len(row)):
                    x += 1

                    if row[column] == "1":
                        self.tile = pg.draw.rect(window, self.white, (x * 16 - camera.cameraX , y * 16 - camera.cameraY, 16, 16), 1)

                        #COLLISION
                        if self.tile.colliderect(self.catRect.x + self.dx , self.catRect.y, self.catRect.width , self.catRect.height) and keyinput[pg.K_d]:
                            self.dx = 0
                            self.gravity = 1

                        if self.tile.colliderect(self.catRect.x + self.dx , self.catRect.y, self.catRect.width , self.catRect.height) and keyinput[pg.K_a]:
                            self.dx = 0
                            self.gravity = 1


                        if self.tile.colliderect(self.catRect.x, self.catRect.y + self.dy, self.catRect.width , self.catRect.height):
                            
                            self.dy = 0
                            self.onGround = True

                            if abs((self.catRect.top + self.dy) - self.tile.bottom) < 20:
                                self.jumpVel = 0
                                self.dy = self.tile.bottom - self.catRect.top

                                    
                y += 1


        self.x += self.dx
        self.y += self.dy



player = playerClass()


#CAMERA
class cameraClass():
    def __init__(self):
         self.cameraX = player.x - 1024/6.3
         self.cameraY = player.y - 620/5.5
         self.cameraSpeed = 3
         self.cameraFixSpeed = 4

    def update(self, pg, display, keyinput):
        camCenter = pg.Rect((1024/6.3 ,620/6.5 , 5,5))

        angle = math.atan2(player.y - self.cameraY - 620/6.5, player.x - self.cameraX - 1024/6.3)
        cdx = math.cos(angle)
        cdy = math.sin(angle)


        if not camCenter.colliderect(player.catRect):
            self.cameraX += cdx * self.cameraSpeed
            self.cameraY += cdy * self.cameraSpeed

        if self.cameraX > player.x - 90:
            self.cameraSpeed = self.cameraFixSpeed
            
        elif self.cameraX + 220 < player.x:
            self.cameraSpeed = self.cameraFixSpeed
           # print("AAAA")
            
        #elif self.cameraY > player.y - 70:
        elif self.cameraY + 60 >  player.y:
            self.cameraSpeed = self.cameraFixSpeed

        elif self.cameraY + 160 <  player.y:
            self.cameraSpeed = player.gravity

        else:
            self.cameraSpeed = 3

camera = cameraClass()


class animationClass():
    def __init__(self, pg) -> None:
        self.idleImage = pg.image.load("data/sprites/idle_sprite.png")
        self.idleFrames = []
        self.idleSurface = pg.Surface((16,17))
        self.idleCount = 0

        self.runImage = pg.image.load("data/sprites/run_sprite.png")
        self.runFrames = []
        self.runSurface = pg.Surface((16,17))
        self.runCount = 0

        self.jumpImage = pg.image.load("data/sprites/jump_sprite.png")
        self.jumpFrames = []
        self.jumpSurface = pg.Surface((16,17))
        self.jumpCount = 0

        #WEAPON

        self.atk1Image = pg.image.load("data/sprites/atk1_sprite.png")
        self.atk1WeaponImage = pg.image.load("data/sprites/atk1_sprite.png")
        self.atk1Frames = []
        self.atk1Surface = pg.Surface((16,17))
        self.atk1Count = 0



    def idleAnimationLeft(self, pg, window):
        self.idleSurface.fill(0)
        self.idleSurface.set_colorkey(0)

        for num in range(6):
            self.idleFrames.append(-16 * num)
        
        self.idleImageFlipped = pg.transform.flip(self.idleImage, True, False)
        self.idleSurface.blit(self.idleImageFlipped,(self.idleFrames[int(self.idleCount)], 0))
        self.idleCount += 0.12
        

        window.blit(self.idleSurface,(player.x - camera.cameraX, player.y - camera.cameraY + 3))


    def idleAnimationRight(self, pg, window):
        self.idleSurface.fill(0)
        self.idleSurface.set_colorkey(0)

        for num in range(6):
            self.idleFrames.append(-16 * num)

        
        self.idleSurface.blit(self.idleImage,(self.idleFrames[int(self.idleCount)], 0))
        self.idleCount += 0.12

        window.blit(self.idleSurface,(player.x - camera.cameraX, player.y - camera.cameraY + 3))


    def runAnimationLeft(self, pg, window):
        self.runSurface.fill(0)
        self.runSurface.set_colorkey(0)

        for num in range(8):
            self.runFrames.append(-16 * num)
        
        self.runImageFlipped = pg.transform.flip(self.runImage, True, False)
        self.runSurface.blit(self.runImageFlipped,(self.runFrames[int(self.runCount)], 0))
        
        self.runCount += 0.2
        window.blit(self.runSurface,(player.x - camera.cameraX, player.y - camera.cameraY + 3))
        

    def runAnimationRight(self, pg, window):
        self.runSurface.fill(0)
        self.runSurface.set_colorkey(0)

        for num in range(8):
            self.runFrames.append(-16 * num)
        
        
        self.runSurface.blit(self.runImage,(self.runFrames[int(self.runCount)], 0))
        
        self.runCount += 0.2
        window.blit(self.runSurface,(player.x - camera.cameraX, player.y - camera.cameraY + 3))


    def jumpAnimationLeft(self, pg, window):
        self.jumpSurface.fill(0)
        self.jumpSurface.set_colorkey(0)

        for num in range(12):
            self.jumpFrames.append(-16 * num)
        
        self.jumpImageFlipped = pg.transform.flip(self.jumpImage, True, False)
        self.jumpSurface.blit(self.jumpImageFlipped,(self.jumpFrames[int(self.jumpCount)], 0))
        
        self.jumpCount += 0.12
        window.blit(self.jumpSurface,(player.x - camera.cameraX, player.y - camera.cameraY + 3))

    def jumpAnimationRight(self, pg, window):
        self.jumpSurface.fill(0)
        self.jumpSurface.set_colorkey(0)

        for num in range(12):
            self.jumpFrames.append(-16 * num)
        
        
        self.jumpSurface.blit(self.jumpImage,(self.jumpFrames[int(self.jumpCount)], 0))
        
        self.jumpCount += 0.12
        window.blit(self.jumpSurface,(player.x - camera.cameraX, player.y - camera.cameraY + 3))
        

    #ATK ANIMATION


    def atk1AnimationLeft(self, pg, window):
        self.atk1Surface.fill(0)
        self.atk1Surface.set_colorkey(0)

        for num in range(6):
            self.atk1Frames.append(-16 * num)
        
        self.atk1ImageFlipped = pg.transform.flip(self.atk1Image, True, False)
        self.atk1Surface.blit(self.atk1ImageFlipped,(self.atk1Frames[int(self.atk1Count)], 0))
        self.atk1Count += 0.12
        

        window.blit(self.atk1Surface,(player.x - camera.cameraX, player.y - camera.cameraY + 3))





import pygame as pg
animate = animationClass(pg)


#NPC TEST
class npcClass():
    def __init__(self, pg) -> None:
        self.idleImage = pg.image.load("data/sprites/rrh_sprite.png")
        self.idleFrames = []
        self.idleSurface = pg.Surface((25,40))
        self.idleCount = 0

        self.sliderCounter = 0
        self.nameSlider = 0

    def updateJordin(self, pg, window, mousePointer, FONT, display):
        font = pg.font.Font(FONT, 16)
        self.idleSurface.fill(0)
        self.idleSurface.set_colorkey(0)

        self.hitbox = pg.draw.rect(window, (255,0,255), (98 - camera.cameraX + 3, 792 - camera.cameraY + 10, 14,25),1)
        self.idleImage.set_colorkey((255,0,255))


        for num in range(17):
            self.idleFrames.append(-25 * num)

        self.idleSurface.blit(self.idleImage,(self.idleFrames[int(self.idleCount)], 0))
        self.idleCount += 0.2

        window.blit(self.idleSurface,(98 - camera.cameraX, 792 - camera.cameraY))

        name = "NPC(01)"
        nameRnd = font.render(name[0:int(self.nameSlider)], False, (255,255,255))
        
        #ACTION
        if self.hitbox.colliderect(mousePointer):
            window.blit(nameRnd, (self.hitbox.x + 20 , self.hitbox.y))

            slider = pg.draw.rect(window, (255,255,255), (self.hitbox.x + 20 , self.hitbox.y , self.sliderCounter,1))
            slider1 = pg.draw.line(window, (255,255,255),(self.hitbox.x + 20 , self.hitbox.y),(self.hitbox.x + 10, self.hitbox.y + 5))
            self.sliderCounter += 3
            self.nameSlider += 0.2
            if self.sliderCounter > 40:
                self.sliderCounter = 40
                self.nameSlider

            if self.nameSlider > 12:
                self.nameSlider = 12
                
        else:
            self.sliderCounter = 0
            self.nameSlider = 0

        

npc = npcClass(pg)
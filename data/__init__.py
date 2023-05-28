import csv
import math



class animationClass():
    def __init__(self, pg) -> None:
        self.animList = []
        self.x, self.y = 0,0
        self.idleImage = pg.image.load("data/sprites/Meow Knight/Meow-Knight_Idle.png")
        self.surfaceBlit = pg.Surface((16,16))

    def testStrips(self, pg, window):
        pass
        

            

#animate = animationClass()


class playerClass():
    def __init__(self):
        self.x = 0
        self.y = 200

        self.speed = 3
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




    def update(self, pg, window):
        self.catRect = pg.draw.rect(window, self.red, (self.x - camera.cameraX, self.y - camera.cameraY, 16,20),1)
        self.dx , self.dy = 0, 0
        


        
    def movement(self, pg, keyinput):

        if keyinput[pg.K_a]:
            self.dx -= self.speed

        if keyinput[pg.K_d]:
            self.dx += self.speed      

        if keyinput[pg.K_w] and self.jumpCd == True:
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
        
        else:
            self.onGround = False
            


        #print(self.jumpVel)
            

        self.dy += self.gravity
        if self.dy > self.gravity:
            self.dy = self.gravity

        #self.dy += self.y
        self.gravity = 5
        print(self.jumpCounter)

        #JUMP COOLDOWN
        self.jumpCounter += 0.3
        if self.jumpCounter > 10:
            self.jumpCd = True

        if self.jumpCounter > 10:
            self.jumpCounter = 10



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
                        tile = pg.draw.rect(window, self.white, (x * 16 - camera.cameraX , y * 16 - camera.cameraY, 16, 16), 1)


                        #COLLISION
                        if tile.colliderect(self.catRect.x + self.dx , self.catRect.y, self.catRect.width , self.catRect.height) and keyinput[pg.K_d]:
                            self.dx = 0
                            self.gravity = 1

                        if tile.colliderect(self.catRect.x + self.dx , self.catRect.y, self.catRect.width , self.catRect.height) and keyinput[pg.K_a]:
                            self.dx = 0
                            self.gravity = 1


                        if tile.colliderect(self.catRect.x, self.catRect.y + self.dy, self.catRect.width , self.catRect.height):
                            
                            self.dy = 0

                            if abs((self.catRect.top + self.dy) - tile.bottom) < 20:
                                self.jumpVel = 0
                                self.dy = tile.bottom - self.catRect.top
                            
                            self.onGround = True
                            

                y += 1


        self.x += self.dx
        self.y += self.dy



player = playerClass()



#CAMERA
class cameraClass():
    def __init__(self):
         self.cameraX = player.x - 1024/6.3
         self.cameraY = player.y - 620/5.5
         self.cameraSpeed = 1
         self.cameraFixSpeed = 5

    def update(self, pg, display, keyinput):
        camCenter = pg.draw.rect(display, (255,30,255), (1024/6.3 ,620/6.5 , 2,2))

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
            self.cameraSpeed = self.cameraFixSpeed

        else:
            self.cameraSpeed = 1

camera = cameraClass()

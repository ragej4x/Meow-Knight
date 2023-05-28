import pygame as pg
from data import *

pg.init()

winSize = (1024, 620)
display = pg.display.set_mode(winSize)
window = pg.Surface((winSize[0]//3, winSize[1]//3))
pg.display.set_caption("Meow Knight")

clock = pg.time.Clock()
animate = animationClass(pg)
FONT  = ("data/fonts/rainyhearts.ttf")

ShowFps = True
ShowCoordinate = True

loop = True

def showFps():
    font = pg.font.Font(FONT, 18)
    getFps = str(int(clock.get_fps()))
    rndFps = font.render(f"FPS: {getFps}", True, (200,200,200))
    display.blit(rndFps, (5, 2))

def showCoordinate():
    font = pg.font.Font(FONT, 18)
    rndCoord = font.render(f"X: {str(player.x)}  Y: {str(player.y)}", True, (200,200,200))
    display.blit(rndCoord, (100, 2))


def eventHandler():
    global loop

    #dynamic resolution
    dynamicRes = pg.transform.scale(window, winSize)
    display.blit(dynamicRes,(0,0))


    for event in pg.event.get():
        if event.type == pg.QUIT:
            loop = False

    if ShowFps == True:
        showFps()

    if ShowCoordinate == True:
        showCoordinate()

    pg.display.flip()
    clock.tick(60)

while loop == True:
    window.fill((30,30,30))
    
    #inputs
    keyinput = pg.key.get_pressed()

    #CALLING FUNC
    player.update(pg, window)
    player.movement(pg, keyinput)
    player.mapFunc(pg, window, keyinput)

    animate.testStrips(pg, window)
    camera.update(pg, window, keyinput)

    eventHandler()

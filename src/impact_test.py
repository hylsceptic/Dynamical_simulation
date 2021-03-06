import pygame
import sys
import time, math
from settings import Settings
from utils import generateRandomBalls, detectAllImpactAndUpdate, createLocationTable


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(ai_settings.display)
    surface1 = pygame.Surface(ai_settings.resolution)
    pygame.display.set_caption("Dynamics simulation")
    # rect = Rectangle(ai_settings,screen)
    # pygame.draw.rect(screen, (0,0,255), (100, 200, 100, 100))
    # font = pygame.font.Font(None, 36)
    # text = font.render("Now create your world", 1, (10, 10, 10))
    # textpos = text.get_rect(centerx=screen.get_width()/2)
    g =  [0, 0] # 加速度
    updateTime = 0.005
    # clock = pygame.time.Clock()
    t1 = time.time() # 

    balls = generateRandomBalls(120, -300, 300, 30, ai_settings.resolution)
    # balls = [ ball.Ball(100, [-200, 0], [2400, 1000], [0, 0, 255], 20),
    #           ball.Ball(40, [ 200, 0], [ 800, 1000], [0, 255, 0], 1),]
    k = 40
    LocationTable = createLocationTable(balls, ai_settings.resolution, k)
    
    while True:
        # clock.tick(30)
        # supervise keyboard and mouse item
        # print(t2,velocity)
        tic = time.time() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # circlePosY = round(circlePosY + (t2 - t1) * velocity)
        t2 = time.time()       
        surface1.fill(ai_settings.bg_color) # fill color

        while t2 - t1 > updateTime:
            # tt1 = time.time()
            detectAllImpactAndUpdate(balls, ai_settings.resolution, k, LocationTable, updateTime, g)
            # tt2 = time.time()
            # for eachBall in balls:
            #     if eachBall.isImpact == 1:
            #         print("got you")
            # print(LocationTable)

            for eachBall in balls:
                if eachBall.isImpact == 0:
                    eachBall.update(surface1, g, updateTime)

            LocationTable = createLocationTable(balls, ai_settings.resolution, k)
            # tt3 = time.time()
            # print((tt3 - tt2)/(tt2 - tt1))
            t1 += updateTime
            # if (int(t1/updateTime) % 200 == 0):
            #     balls.append(ball.Ball(40, [ 200, 0], [ 800, 1000], [0, 255, 0], 1))
 

        # screen.blit(text, textpos) 
        # rect.blitme()
        for eachBall in balls:
            location = [int(eachBall.location[0]), int(eachBall.location[1])]
            pygame.draw.circle(surface1, eachBall.color, location, eachBall.radius)
        # visualiaze the window
        ## resize the resolution into the window
        pygame.transform.scale(surface1, ai_settings.display, screen)
        pygame.display.flip()
        toc = time.time() 
        # print(toc - tic)

if __name__ == '__main__':
    run_game()
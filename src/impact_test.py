import pygame
# from pygame.sprite import Group
import sys
import time, math
import ball
from random import random
import numpy as np
from settings import Settings
# from rectangle import Rectangle
# from game_stats import game_statsts
# from scoreboard import Scoreboard
# from button import Button
# from circle import Circle
# import game_functions as gf


def impact(ball1, ball2, dt):
    v1  = ball1.location - ball2.location
    v2 = ball1.velocity - ball2.velocity
    dis = np.linalg.norm(v1)
    velocity = np.linalg.norm(v2)
    cs = np.dot(v1, v2)/dis/velocity
    if cs >= 0: return 0
    s1 = np.sqrt(1 - max(1, cs**2))*dis
    if s1 - ball1.radius - ball2.radius > 0: return 0    
    dt1 = (np.sqrt(dis**2 - s1**2) - np.sqrt((ball1.radius + ball2.radius)**2 - s1**2))*-cs/velocity
    if dt1 > dt:
        return 0
    ball1.location += ball1.velocity*dt1
    ball2.location += ball2.velocity*dt1
    dt2 = dt - dt1
    v1  = ball1.location - ball2.location
    dis = np.linalg.norm(v1)
    dvscale = np.dot(v1, v2)/dis
    dv = -dvscale*v1/dis
    ball1.velocity += dv
    ball2.velocity -= dv
    ball1.location += ball1.velocity*dt2
    ball2.location += ball2.velocity*dt2

    return 1



def setBallLocation(balls, resolution, k):
    LocationTable = []
    for x in range(k):
        pX = []
        for y in range(k):
            pX.append([])
        LocationTable.append(pX)
    width, height = resolution[0]/k, resolution[1]/k
    for eachBall in balls:
        LocationTable[int(eachBall.location[0]/width)][int(eachBall.location[1]/height)].append(eachBall)
        eachBall.isImpact = 0
    return LocationTable

def updateImpact(totalballs, resolution, k, LocationTable, dt):
    # t1 = time.time()
    for x in range(k):
        for y in range(k):
            balls = []
            for eachBall in LocationTable[x][y]:
                balls.append(eachBall)
            num1 = len(balls)
            if x + 1 < k:
                for eachBall in LocationTable[x + 1][y]:
                    balls.append(eachBall)
            if y + 1 < k:
                for eachBall in LocationTable[x][y + 1]:
                    balls.append(eachBall)
            if x + 1 < k and y + 1 < k:
                for eachBall in LocationTable[x + 1][y + 1]:
                    balls.append(eachBall)
            if x - 1 > 0 and y + 1 < k:
                for eachBall in LocationTable[x - 1][y + 1]:
                    balls.append(eachBall)

            num2 = len(balls)
            for i in range(num1):
                ball1 = balls[i]
                if ball1.isImpact == 1: continue
                for j in range(i + 1, num2):
                    ball2 = balls[j]
                    if  ball2.isImpact == 1:
                        continue
                    isImpact = impact(ball1, ball2, dt)
                    ball1.isImpact, ball2.isImpact = isImpact, isImpact

    # t2 = time.time()
    LocationTable = setBallLocation(totalballs, resolution, k)
    # t3 = time.time()
    # print((t3 - t2)/(t2 - t1))
    return LocationTable 

def generateBalls(num, maxv, minv, radius, resolution):
    balls = []
    for i in range(num):
        while 1:
            location = [resolution[0]*random(), resolution[1]*random()]
            if location[0] + radius > resolution[0] or location[0] - radius < 0 \
                or location[1] + radius > resolution[1] or location[1] - radius < 0: continue
            sig = 0
            for eachBall in balls:
                if math.sqrt((location[0] - eachBall.location[0])**2 + (location[1] - eachBall.location[1])**2) - radius - eachBall.radius < 0: 
                    sig = 1
                    break
            if sig == 1: continue
            vx = minv + (maxv - minv)*random()
            vy = minv + (maxv - minv)*random()
            balls.append(ball.Ball(radius, [vx, vy], location, [255*random(), 255*random(), 255*random()]))
            break
    return balls

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
    updateTime = 0.02
    balls = generateBalls(700, -100, 100, 30, ai_settings.resolution)
    k = 32
    LocationTable = setBallLocation(balls, ai_settings.resolution, k)
    
    t1 = time.time() # 
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
            tt1 = time.time()
            LocationTable = updateImpact(balls, ai_settings.resolution, k, LocationTable, updateTime)
            tt2 = time.time()
            for eachBall in balls:
                if eachBall.isImpact == 0:
                    eachBall.update(surface1, g, updateTime)
            tt3 = time.time()
            # print((tt3 - tt2)/(tt2 - tt1))

            # isImpact = impact(ball0, ball1, updateTime)
            # # print(isImpact)
            # if not isImpact:
            #     ball1.update(surface1, g, updateTime)
            #     ball0.update(surface1, g, updateTime)
            # else:
            #     ball1.update(surface1, g, 0)
            #     ball0.update(surface1, g, 0)

            t1 += updateTime
        # velocity = velocity + g * (t2 - t1)
        # print(pygame.TIMER_RESOLUTION)

        # screen.blit(text, textpos) 
        # rect.blitme()
        # visualiaze the window
        ## resize the resolution into the window
        for eachBall in balls:
            location = [int(eachBall.location[0]), int(eachBall.location[1])]
            pygame.draw.circle(surface1, eachBall.color, location, eachBall.radius)
        pygame.transform.scale(surface1, ai_settings.display, screen)
        pygame.display.flip()
        toc = time.time() 
        print(toc - tic)


    #############
    # # Make the Play button.
    # play_button = Button(ai_settings, screen, "Play")
    
    # # Create an instance to store game statistics, and a scoreboard.
    # stats = GameStats(ai_settings)
    # sb = Scoreboard(ai_settings, screen, stats)
    
    
    # # Make a ship, a group of bullets, and a group of aliens.
    # ship = Ship(ai_settings, screen)
    # bullets = Group()
    # aliens = Group()
    
    # # Create the fleet of aliens.
    # gf.create_fleet(ai_settings, screen, ship, aliens)

    # # Start the main loop for the game.
    # while True:
    #     gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
    #         aliens, bullets)
        
    #     if stats.game_active:
    #         ship.update()
    #         gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
    #             bullets)
    #         gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
    #             bullets)
        
    #     gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
    #         bullets, play_button)


if __name__ == '__main__':
    run_game()
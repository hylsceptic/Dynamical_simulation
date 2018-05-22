import pygame
# from pygame.sprite import Group
import sys
import time, math
import ball

from settings import Settings
# from rectangle import Rectangle
# from game_stats import game_statsts
# from scoreboard import Scoreboard
# from button import Button
# from circle import Circle
# import game_functions as gf


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
    # g =  [1000, 5000] # 加速度
    G = 9.8
    updateTime = 0.0001
    # clock = pygame.time.Clock()
    t1 = time.time() # 
    t2 = t1
    ball0 = ball.Ball(40, [0, 0], [800, ai_settings.resolution[1]/2], [0, 0, 255])
    ball2 = ball.Ball(40, [0, 200], [800, ai_settings.resolution[1]/2], [0, 255, 0])
    ball1 = ball.Ball(100, [0, 0], [ai_settings.resolution[0]/2, ai_settings.resolution[1]/2], [0, 255, 0], 5000000)
    balls = [ball1, ball2, ball0]
    ball0.getGravityEnergy([ball1,], G)
    ball2.getGravityEnergy([ball1,], G)
    while True:
        # clock.tick(30)
        # supervise keyboard and mouse item
        # print(t2,velocity)
        # tic = time.time() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # circlePosY = round(circlePosY + (t2 - t1) * velocity)
        t2 = time.time()
        surface1.fill(ai_settings.bg_color) # fill color
        # dis = math.sqrt((ball0.location[0] - ball1.location[0])**2 + (ball0.location[1] - ball1.location[1])**2)
        # gscale = G*ball0.mass*ball1.mass/dis**2
        # g1 = [gscale*(ball1.location[0] - ball0.location[0])/dis, gscale*(ball1.location[1] - ball0.location[1])/dis]
        # print(g1)

        while t2 - t1 > updateTime:
            ball0.updateGravity(surface1, updateTime, [ball1,], G)
            ball2.updateGravity(surface1, updateTime, [ball1,], G)
            ball1.update(surface1, (0, 0), updateTime)
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
        # print(g[1]*(ai_settings.resolution[1] - ball0.location[1]) + g[0]*(ai_settings.resolution[0] - ball0.location[0]) + 1/2*ball0.velocity[1]**2) 
        # toc = time.time() 
        # print((t2 - t1), toc - tic)


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
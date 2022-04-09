import pygame
import random
import sys
import os
from math import ceil

def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)
 
# initialize 
pygame.init()
random.seed()

def normal_snake_display(
    display, width, height,
    fn, skin, snake_head,
    snake_tail, snake_eat,
    TL, menu_button,
    continue_button, restart_button, 
    skin_f, apple, game_end,
    eat_sound, click_sound):

    # snake position with offsets
    snake_pos = {
        "x": width/2-10,
        "y": height/2-10,
        "x_change": -10,
        "y_change": 0,
        'dir': 'left'}
    Dir = 'left'
 
    # snake el size
    snake_size = (10, 10)
 
    # current snake movement speed
    snake_speed = 10
 
    # snake tails
    snake_tails = []
 
    for i in range(2):
        snake_tails.append([snake_pos["x"] + 10*i, snake_pos["y"], 'left'])
 
    # food
    food_eaten = 0
    food_pos = {
        "x": round(random.randrange(0, width - snake_size[0]) / 10) * 10,
        "y": round(random.randrange(60, height - snake_size[1]) / 10) * 10}
    
    fd = pygame.font.SysFont('Cooper Black', 48)

    # start loop
    FPS = 8
    fpsClock=pygame.time.Clock()
 
    while game_end:
        # game loop
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end = False
 
        keys = pygame.key.get_pressed()
    
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and snake_pos["x_change"] == 0:
            # move left
            snake_pos["x_change"] = -snake_speed
            snake_pos["y_change"] = 0
            Dir = 'left'
 
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and snake_pos["x_change"] == 0:
            # move right
            snake_pos["x_change"] = snake_speed
            snake_pos["y_change"] = 0
            Dir = 'right'
 
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and snake_pos["y_change"] == 0:
            # move up
            snake_pos["x_change"] = 0
            snake_pos["y_change"] = -snake_speed
            Dir = 'up'
 
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and snake_pos["y_change"] == 0:
            # move down
            snake_pos["x_change"] = 0
            snake_pos["y_change"] = snake_speed
            Dir = 'down'
        elif keys[pygame.K_ESCAPE]:
            hep = Pause_display(
                width, height, display, fn, 
                menu_button, continue_button,
                restart_button, game_end, click_sound)
            game_end = hep[0]
            if hep[1] == 0:
                pygame.mixer.Sound.play(click_sound)
                return (game_end, True, False)
            if hep[1] == 1:
                pygame.mixer.Sound.play(click_sound)
            if hep[1] == 2:
                pygame.mixer.music.play(-1)
                return (game_end, False, True)
 
        # screen
        display.fill((0, 0, 0))
        fn_xy = 200
        W1 = int(ceil(width/fn_xy))
        H1 = int(ceil((height-60)/fn_xy))
    
        for x in range(W1):
            for y in range(H1):
                X = fn_xy * x
                Y = fn_xy * y + 60
                display.blit(fn, (X, Y))

        # draw food
        display.blit(apple[skin_f], (food_pos["x"], food_pos["y"]))
     
        # move snake tails
        ltx = snake_pos["x"]
        lty = snake_pos["y"]
        ltd = snake_pos['dir']
 
        for i,v in enumerate(snake_tails):
            _ltx = snake_tails[i][0]
            _lty = snake_tails[i][1]
            _ltd = snake_tails[i][-1]
 
            snake_tails[i][0] = ltx
            snake_tails[i][1] = lty
            snake_tails[i][-1] = ltd
 
            ltx = _ltx
            lty = _lty
            ltd = _ltd
 
        # draw snake tails
        for t in snake_tails[:-1]:
            display.blit(TL[str(skin)] ,(t[0], t[1]))
            
        display.blit(snake_tail[skin][snake_tails[-2][2]],(snake_tails[-1][0], snake_tails[-1][1]))
 
        # direction
        snake_pos["x"] += snake_pos["x_change"]
        snake_pos["y"] += snake_pos["y_change"]
        snake_pos['dir'] = Dir
 
        #if required
        if(snake_pos["x"] < 0):
            snake_pos["x"] = width-10
 
        elif(snake_pos["x"] > width-10):
            snake_pos["x"] = 0
 
        elif(snake_pos["y"] < 60):
            snake_pos["y"] = height-10
 
        elif(snake_pos["y"] > height-10):
            snake_pos["y"] = 60

        # draw snake
        display.blit(snake_head[skin][snake_pos['dir']], (snake_pos["x"], snake_pos["y"]))

        # detect collision with tail
        for i,v in enumerate(snake_tails):
            if(snake_pos["x"] == snake_tails[i][0]
                and snake_pos["y"] == snake_tails[i][1]):
                snake_tails = snake_tails[:i]
                break
 
        # detect collision with food
        if(snake_pos["x"] == food_pos["x"]
            and snake_pos["y"] == food_pos["y"]):
            pygame.mixer.Sound.play(eat_sound)
            food_eaten += 1
            snake_tails.append([food_pos["x"], food_pos["y"], Dir])
            display.blit(snake_eat[skin][snake_pos['dir']], (snake_pos["x"], snake_pos["y"]))
        
            food_pos = {
                "x": round(random.randrange(0, width - snake_size[0]) / 10) * 10,
                "y": round(random.randrange(60, height - snake_size[1]) / 10) * 10}
        
            xx = snake_pos["x"]
            yy = snake_pos["y"]

            #if food spawn on snake
            for t in snake_tails:
                while xx == food_pos["x"] and yy == food_pos["y"]:
                    food_pos = {
                        "x": round(random.randrange(0, width - snake_size[0]) / 10) * 10,
                        "y": round(random.randrange(60, height - snake_size[1]) / 10) * 10}
                xx = t[0]
                yy = t[1]

        #score food
        score = fd.render(str(food_eaten), 1, (255, 255, 255))
        display.blit(score, (20, 0)) 
 
        pygame.display.update()
    return (game_end, False, False)


def survival_snake_display(
    display, width, height,
    fn, skin, snake_head,
    snake_tail, snake_eat,
    TL, golden_cup, menu_button,
    continue_button, restart_button, 
    skin_f, apple, game_end,
    eat_sound, lose_sound, click_sound, win_sound):

    # snake position with offsets
    snake_pos = {
        "x": width/2-10,
        "y": height/2-10,
        "x_change": -10,
        "y_change": 0,
        'dir': 'left'}
    Dir = 'left'
 
    # snake el size
    snake_size = (10, 10)
 
    # current snake movement speed
    snake_speed = 10
 
    # snake tails
    snake_tails = []
 
    for i in range(2):
        snake_tails.append([snake_pos["x"] + 10*i, snake_pos["y"], 'left'])
 
    # food
    food_pos = {
        "x": round(random.randrange(10, width - snake_size[0]-10) / 10) * 10,
        "y": round(random.randrange(70, height - snake_size[1]-10) / 10) * 10}
    
    #score
    food_eaten = 0
    file = open(resource_path('score.txt'),'r+')
    file_ = file.read()
    if file_ == '':
        file_ = '0'
    fd = pygame.font.SysFont('Cooper Black', 48)
    flag = False

    # start loop
    FPS = 8
    fpsClock=pygame.time.Clock()
 
    while game_end:
        # game loop
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end = False
 
        keys = pygame.key.get_pressed()
    
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and snake_pos["x_change"] == 0:
            # move left
            snake_pos["x_change"] = -snake_speed
            snake_pos["y_change"] = 0
            Dir = 'left'
 
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and snake_pos["x_change"] == 0:
            # move right
            snake_pos["x_change"] = snake_speed
            snake_pos["y_change"] = 0
            Dir = 'right'
 
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and snake_pos["y_change"] == 0:
            # move up
            snake_pos["x_change"] = 0
            snake_pos["y_change"] = -snake_speed
            Dir = 'up'
 
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and snake_pos["y_change"] == 0:
            # move down
            snake_pos["x_change"] = 0
            snake_pos["y_change"] = snake_speed
            Dir = 'down'
        elif keys[pygame.K_ESCAPE]:
            hep = Pause_display(
                width, height, display, fn, 
                menu_button, continue_button,
                restart_button, game_end, click_sound)
            game_end = hep[0]
            if hep[1] == 0:
                pygame.mixer.Sound.play(click_sound)
                file.close()
                return (game_end, True, False)
            if hep[1] == 1:
                pygame.mixer.Sound.play(click_sound)
            if hep[1] == 2:
                file.close()
                pygame.mixer.music.play(-1)
                return (game_end, False, True)
 
        # screen
        fn_xy = 200
        W1 = int(ceil(width/fn_xy))
        H1 = int(ceil((height-60)/fn_xy))
    
        for x in range(W1):
            for y in range(H1):
                X = fn_xy * x
                Y = fn_xy * y + 60
                display.blit(fn, (X, Y))

        pygame.draw.rect(display, (169, 186, 186), (0, 60, 640, 420), 20)
        pygame.draw.rect(display, (0, 0, 0), (0, 0, 640, 60))

        # draw food
        display.blit(apple[skin_f], (food_pos["x"], food_pos["y"]))
     
        # move snake tails
        ltx = snake_pos["x"]
        lty = snake_pos["y"]
        ltd = snake_pos['dir']
 
        for i,v in enumerate(snake_tails):
            _ltx = snake_tails[i][0]
            _lty = snake_tails[i][1]
            _ltd = snake_tails[i][-1]
 
            snake_tails[i][0] = ltx
            snake_tails[i][1] = lty
            snake_tails[i][-1] = ltd
 
            ltx = _ltx
            lty = _lty
            ltd = _ltd
 
        # draw snake tails
        for t in snake_tails[:-1]:
            display.blit(TL[str(skin)] ,(t[0], t[1]))
            
        display.blit(snake_tail[skin][snake_tails[-2][2]],(snake_tails[-1][0], snake_tails[-1][1]))
 
        # direction
        snake_pos["x"] += snake_pos["x_change"]
        snake_pos["y"] += snake_pos["y_change"]
        snake_pos['dir'] = Dir
 
        #if required
        if (snake_pos["x"] < 10 or snake_pos["x"] > width-20 or snake_pos["y"] < 70 or snake_pos["y"] > height-20):
            pygame.mixer.Sound.play(lose_sound)
            perem = Game_over_display(
                width, height, display, food_eaten, 
                fn, menu_button, continue_button,
                restart_button, game_end, flag, file, win_sound, click_sound)
            game_end = perem[0]
            if perem[1] == 0:
                pygame.mixer.Sound.play(click_sound)
                return (game_end, True, False)
            if perem[1] == 1:
                pygame.mixer.music.play(-1)
                return (game_end, False, True)

        # draw snake
        display.blit(snake_head[skin][snake_pos['dir']], (snake_pos["x"], snake_pos["y"]))

        # detect collision with tail
        for i,v in enumerate(snake_tails):
            if(snake_pos["x"] == snake_tails[i][0]
                and snake_pos["y"] == snake_tails[i][1]):
                pygame.mixer.Sound.play(lose_sound)
                perem = Game_over_display(
                    width, height, display, food_eaten, 
                    fn, menu_button, continue_button,
                    restart_button, game_end, flag, file, win_sound, click_sound)
                game_end = perem[0]
                if perem[1] == 0:
                    pygame.mixer.Sound.play(click_sound)
                    return (game_end, True, False)
                if perem[1] == 1:
                    pygame.mixer.music.play(-1)
                    return (game_end, False, True)
 
        # detect collision with food
        if(snake_pos["x"] == food_pos["x"]
            and snake_pos["y"] == food_pos["y"]):
            pygame.mixer.Sound.play(eat_sound)
            food_eaten += 1
            snake_tails.append([food_pos["x"], food_pos["y"], Dir])
            display.blit(snake_eat[skin][snake_pos['dir']], (snake_pos["x"], snake_pos["y"]))
        
            food_pos = {
                "x": round(random.randrange(10, width - snake_size[0]-10) / 10) * 10,
                "y": round(random.randrange(70, height - snake_size[1]-10) / 10) * 10}
        
            xx = snake_pos["x"]
            yy = snake_pos["y"]

            #if food spawn on snake
            for t in snake_tails:
                while xx == food_pos["x"] and yy == food_pos["y"]:
                    food_pos = {
                        "x": round(random.randrange(10, width - snake_size[0]-10) / 10) * 10,
                        "y": round(random.randrange(70, height - snake_size[1]-10) / 10) * 10}
                xx = t[0]
                yy = t[1]

        #score food
        score = fd.render(str(food_eaten), 1, (255, 255, 255))
        display.blit(score, (20, 0))
        if int(file_) >= food_eaten:
            score = fd.render('total score ' + file_, 1, (255, 255, 255))
            display.blit(score, (250, 0))
        else:
            score = fd.render('new record ' + str(food_eaten), 1, (255, 255, 255))
            display.blit(score, (250, 0))
            flag = True

        #win
        if food_eaten >= 300:
            perem = Game_over_display(
                width, height, display, food_eaten, 
                fn, menu_button, continue_button,
                restart_button, game_end, flag, file, 
                win_sound, click_sound, golden_cup, True)
            game_end = perem[0]
            if perem[1] == 0:
                pygame.mixer.Sound.play(click_sound)
                return (game_end, True, False)
            if perem[1] == 1:
                pygame.mixer.music.play(-1)
                return (game_end, False, True)
 
        pygame.display.update()
    file.close()
    return (game_end, False, False)


def button(mouse, click, x, y, ON, OFF, display):
    if (x+212 > mouse[0] > x) and (y+83 > mouse[1] > y) and click[0] == 1:
        display.blit(OFF, (x, y))
        return '1'
    else:
        display.blit(ON, (x, y))
        return '0'

#button for skin
def button_s(click_sound, mouse, click, pp, x, y, buttON, fd, text, display, skin, this_skin, color, py = 0):
    #draw background button
    pygame.draw.rect(display, (255, 255, 255), (x,y, 115, 115))
    pygame.draw.rect(display, color, (x,y, 115, 115), 8)
    
    for i in range(len(buttON)):
        display.blit(buttON[i], (x+(115/2-5), y+(10*i)+10+py))

    #text
    mess = fd.render(text, 1, color)
    display.blit(mess, (x+8+pp, y+80))

    t = False

    if (x+115 > mouse[0] > x) and (y+115 > mouse[1] > y) and click[0] == 1 and skin != this_skin:
        t = True #sound play
    if (x+115 > mouse[0] > x) and (y+115 > mouse[1] > y) and click[0] == 1:
        skin = this_skin
    if skin == this_skin:
        pygame.draw.rect(display, (255, 242, 0), (x-4,y-4, 123, 123), 8)
    return (skin, t)


def menu_display(
    width, height, display,
    fn, start_button, skins_button,
    exit_button, skin, snake_head,
    snake_tail ,snake_eat,
    TL, golden_cup, skin_f, apple,
    menu_button, survival_button,
    continue_button, normal_button,
    restart_button, game_end,
    eat_sound, lose_sound, click_sound, win_sound):

    FPS = 30
    fpsClock=pygame.time.Clock()
 
    while game_end:
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end = False
        
        #draw screen
        fn_xy = 200
        W1 = int(ceil(width/fn_xy))
        H1 = int(ceil((height)/fn_xy))
    
        for x in range(W1):
            for y in range(H1):
                X = fn_xy * x
                Y = fn_xy * y
                display.blit(fn, (X, Y))

        #check mouse pressed
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #draw buttons
        st = button(mouse, click, width/2-100, height/2-140, start_button[0], start_button[1], display)
        sk = button(mouse, click, width/2-100, height/2-35, skins_button[0], skins_button[1], display)
        ex = button(mouse, click, width/2-100, height/2+70, exit_button[0], exit_button[1], display)
        
        pygame.display.update()
        pygame.time.wait(100)

        #check pressed buttons
        t = (st + sk + ex).find('1')
        if t != -1:
            if t == 0:
                pygame.mixer.Sound.play(click_sound)
                game_end = GameMode_display(
                    width, height, display,
                    fn, skin, snake_head,
                    snake_tail,snake_eat,
                    TL, golden_cup, skin_f, apple,
                    menu_button, survival_button,
                    normal_button, continue_button,
                    restart_button, game_end,
                    eat_sound, lose_sound, click_sound, win_sound)
            elif t == 1:
                pygame.mixer.Sound.play(click_sound)
                hep = skins_display(
                    width, height, display,
                    fn, skin, snake_head,
                    snake_tail,snake_eat,
                    TL, skin_f, apple,
                    menu_button, game_end, click_sound)
                game_end = hep[0]
                skin = hep[1] #skin snake
                skin_f = hep[2] #skin food
            elif t == 2:
                return


def GameMode_display(
    width, height, display,
    fn, skin, snake_head,
    snake_tail,snake_eat,
    TL, golden_cup, skin_f, apple,
    menu_button, survival_button,
    normal_button, continue_button,
    restart_button, game_end,
    eat_sound, lose_sound, click_sound, win_sound):

    FPS = 30
    fpsClock=pygame.time.Clock()
 
    while game_end:
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end = False
            
        #draw screen
        fn_xy = 200
        W1 = int(ceil(width/fn_xy))
        H1 = int(ceil((height)/fn_xy))
    
        for x in range(W1):
            for y in range(H1):
                X = fn_xy * x
                Y = fn_xy * y
                display.blit(fn, (X, Y))

        #check mouse pressed
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed() 

        #draw buttons
        sv = button(mouse, click, width/2-100, height/2-140, survival_button[0], survival_button[1], display)
        nr = button(mouse, click, width/2-100, height/2-35, normal_button[0], normal_button[1], display)
        mn = button(mouse, click, width/2-100, height/2+70, menu_button[0], menu_button[1], display)
        
        pygame.display.update()
        pygame.time.wait(100)

        t = (sv + nr + mn).find('1')

        #check pressed buttons
        if t != -1:
            if t == 0:
                pygame.mixer.Sound.play(click_sound)
                pygame.mixer.music.stop() #stop background music
                sv1 = True #while menu button not pressed do this cycle
                while sv1:
                    hep = survival_snake_display(
                        display, width, height,
                        fn, skin, snake_head,
                        snake_tail, snake_eat,
                        TL, golden_cup, menu_button,
                        continue_button, restart_button, 
                        skin_f, apple, game_end,
                        eat_sound, lose_sound, click_sound, win_sound)
                    game_end = hep[0]
                    sv1 = hep[1] #if restart button pressed
                    Bl = hep[2] #if menu button pressed
            elif t == 1:
                pygame.mixer.Sound.play(click_sound)
                pygame.mixer.music.stop()
                nr1 = True #while menu button not pressed do this cycle
                while nr1:
                    hep = normal_snake_display(
                        display, width, height,
                        fn, skin, snake_head,
                        snake_tail, snake_eat,
                        TL, menu_button,
                        continue_button, restart_button, 
                        skin_f, apple, game_end,
                        eat_sound, click_sound)
                    game_end = hep[0]
                    nr1 = hep[1] #if restart button pressed
                    Bl = hep[2] #if menu button pressed
            if t == 2 or Bl:
                pygame.mixer.Sound.play(click_sound)
                pygame.time.wait(200)
                return game_end


def skins_display(
    width, height, display,
    fn, skin, snake_head,
    snake_tail,snake_eat,
    TL, skin_f, apple,
    menu_button, game_end, click_sound):

    #initialize text
    fd = pygame.font.SysFont('Cooper Black', 30)
    
    FPS = 30
    fpsClock=pygame.time.Clock()
 
    while game_end:
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end = False

        bl = False # for click sound play once
                
        #draw screen
        fn_xy = 200
        W1 = int(ceil(width/fn_xy))
        H1 = int(ceil((height)/fn_xy))
    
        for x in range(W1):
            for y in range(H1):
                X = fn_xy * x
                Y = fn_xy * y
                display.blit(fn, (X, Y))

        #check mouse pressed
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
                
        #green_snake
        hep = button_s(
            click_sound, mouse, click, 7, 60, 60,
            [snake_head[0]['up'],
             TL['0'], TL['0'], TL['0'],
             snake_tail[0]['up']],
            fd, 'green', display,
            skin, 0, (65, 100, 0))
        skin = hep[0]
        bl = hep[1] or bl # for click sound play once

        #king_snake
        hep = button_s(
            click_sound, mouse, click, 15, 260, 60,
            [snake_head[1]['up'],
             TL['1'], TL['1'], TL['1'],
             snake_tail[1]['up']],
            fd, 'king', display,
            skin, 1, (255, 202, 24))
        skin = hep[0]
        bl = hep[1] or bl # for click sound play once

        #cold_snake
        hep = button_s(
            click_sound, mouse, click, 15, 460, 60,
            [snake_head[2]['up'],
             TL['2'], TL['2'], TL['2'],
             snake_tail[2]['up']],
            fd, 'cold', display,
            skin, 2, (0, 168, 243))
        skin = hep[0]
        bl = hep[1] or bl # for click sound play once


        #apple_snake
        hep = button_s(
            click_sound, mouse, click, 7, 150, 200, [apple[0]],
            fd, 'apple', display,
            skin_f, 0, (182, 0, 36), 40)
        skin_f = hep[0]
        bl = hep[1] or bl # for click sound play once

        #cherry_snake
        hep = button_s(
            click_sound, mouse, click, 0, 360, 200, [apple[1]],
            fd, 'cherry', display,
            skin_f, 1, (182, 0, 36), 40)
        skin_f = hep[0]
        bl = hep[1] or bl # for click sound play once

        #sound cick
        if bl:
            pygame.mixer.Sound.play(click_sound)

        #menu button
        mn = button(mouse, click, width/2-100, height-125, menu_button[0], menu_button[1], display)
    
        pygame.display.update()
        
        if mn == '1':
            pygame.mixer.Sound.play(click_sound)
            pygame.time.wait(200)
            return (game_end, skin, skin_f)
    return (game_end, skin, skin_f)


def Pause_display(
    width, height, display,
    fn, menu_button, continue_button,
    restart_button, game_end, click_sound):
    
    FPS = 30
    fpsClock=pygame.time.Clock()
 
    while game_end:
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end = False
            
        #draw screen
        fn_xy = 200
        W1 = int(ceil(width/fn_xy))
        H1 = int(ceil((height)/fn_xy))
    
        for x in range(W1):
            for y in range(H1):
                X = fn_xy * x
                Y = fn_xy * y
                display.blit(fn, (X, Y))

        #check mouse pressed
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #draw buttons
        rs = button(mouse, click, width/2-100, height/2-140, restart_button[0], restart_button[1], display)
        cn = button(mouse, click, width/2-100, height/2-35, continue_button[0], continue_button[1], display)
        mn = button(mouse, click, width/2-100, height/2+70, menu_button[0], menu_button[1], display)
        
        pygame.display.update()

        #check buttons pressed
        t = (rs + cn + mn).find('1')
        if t != -1:
            pygame.time.wait(150)
            return (game_end, t)
    return (game_end, 3)


def Game_over_display(
    width, height, display, food_eaten, 
    fn, menu_button, continue_button,
    restart_button, game_end, flag, file,
    win_sound, click_sound, golden_cup = None, win = False):

    #write to file new record
    if flag:
        file.seek(0)
        file.write(str(food_eaten))
    file.close()

    #initialize text
    fd = pygame.font.SysFont('Cooper Black', 45)
    
    FPS = 30
    fpsClock=pygame.time.Clock()

    #for win sound play once
    sound = True
 
    while game_end:
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end = False
            
        #draw screen
        fn_xy = 200
        W1 = int(ceil(width/fn_xy))
        H1 = int(ceil((height)/fn_xy))
    
        for x in range(W1):
            for y in range(H1):
                X = fn_xy * x
                Y = fn_xy * y
                display.blit(fn, (X, Y))

        #if win
        if win:
            display.blit(golden_cup, (width/2-45, 40))
            mess = fd.render('   YOU WIN', 1, (255, 242, 0))
        #lose
        elif flag:
            mess = fd.render('GAME OVER', 1, (120, 180, 0))
            display.blit(mess, (180, height/2-150))
            mess = fd.render('new record '+str(food_eaten), 1, (120, 180, 0))
        #if lose but have new record
        else:
            mess = fd.render('GAME OVER', 1, (255, 0, 10))
            display.blit(mess, (180, height/2-150))
            mess = fd.render('your score '+str(food_eaten), 1, (255, 0, 10))
        #write text
        display.blit(mess, (180, height/2-100))

        #check mouse pressed
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #draw button
        rs = button(mouse, click, width/2-100, height/2-35, restart_button[0], restart_button[1], display)
        mn = button(mouse, click, width/2-100, height/2+70, menu_button[0], menu_button[1], display)
        
        pygame.display.update()

        #for win sound play once
        if win and sound:
            pygame.mixer.Sound.play(win_sound)
            sound = False

        #check buttons pressed
        t = (rs + mn).find('1')
        if t != -1:
            pygame.time.wait(150)
            return (game_end, t)
    return (game_end, 3)


# imports
import pygame
import pygame_gui
import sqlite3
import config
import physics
import maps

#game variables
screen = config.screen
screen_width = config.screen_width
screen_height = config.screen_height

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("sounds/bg_sound.mp3")
pygame.mixer.music.play(loops = -1)

bg = (89, 120, 142)
bg_image = pygame.image.load("images/bg_image.png")

clock = pygame.time.Clock()
fps = 60

manager = pygame_gui.UIManager((screen_width, screen_height))

#database
connection = sqlite3.connect("Users.DB")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS USERS(
        email TEXT, 
        username TEXT, 
        password TEXT
    )
""")
connection.commit()

#font sizes
font1 = pygame.font.SysFont(None, 75)
font2 = pygame.font.SysFont(None, 35)
font3 = pygame.font.SysFont(None, 50)

lvl = 1

#player images for char_select
player1 = pygame.image.load("images/player_front1.png")
player1 = pygame.transform.scale(player1, (500,500))
player1.set_colorkey((255, 255, 255))

player2 = pygame.image.load("images/player2.png")
player2 = pygame.transform.scale(player2, (500,500))
player2.set_colorkey((255, 255, 255))

player3 = pygame.image.load("images/player3.png")
player3 = pygame.transform.scale(player3, (500,500))
player3.set_colorkey((255, 255, 255))

playerimg = None

#wrie function (like screen.blit)
def write(text, font, colour, surface, x, y):
    obj = font.render(text, True, colour)
    rect = obj.get_rect()
    rect.topleft = (x, y)
    surface.blit(obj, rect)

class Button:

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.button = pygame.Rect(x, y, 300, 75)
        pygame.draw.rect(screen, (33, 40, 45), self.button)
        write(self.text, font3, (255, 255, 255), screen, (self.x + 10), (self.y + 10))

    def click (self, pos):
        if self.x < pos[0] < self.x + 300:
            if self.y < pos[1] < self.y + 70:
                return True

        return False

def error_scr(message):
    run = True

    button_rect = pygame.Rect(698, 402, 140, 40)

    while run:
        screen.fill((89, 120, 142, 128))
        popup = pygame.Rect(513, 327, 496, 150)
        pygame.draw.rect(screen, (200, 50, 50), popup, border_radius=10)
        write(message, font2, (255, 255, 255), screen, 520, 340)
        pygame.draw.rect(screen, (50, 200, 50), button_rect, border_radius=5)
        write("OK", font2, (255, 255, 255), screen, 750, 410)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    run = False

def start():
    clicked = False
    while True:
        screen.fill(bg)
        key = pygame.key.get_pressed()
        pygame.display.set_caption("Altitude Adventures")
        write("Altitude Adventures", font1, (255, 255, 255), screen, 501, 100)

        mx, my = pygame.mouse.get_pos()
        loginbtn = Button(615, 300, "Login")
        regbtn = Button(615, 430, "Register")
        exitbtn = Button(615, 560, "Quit")
        if loginbtn.click((mx, my)):
            if clicked:
                login()
        if regbtn.click((mx, my)):
            if clicked:
                register()
        if exitbtn.click((mx, my)):
            if clicked:
                pygame.quit()

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
        if key[pygame.K_k] == True:
            menu()
        if key[pygame.K_l] == True:
            lselect()

        pygame.display.update()

def register():
    running = True
    clicked = False

    email_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((115, 200), (1350, 75)), manager=manager)
    username_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((115, 300), (1350, 75)), manager=manager)
    passw_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((115, 400), (1350, 75)), manager=manager)
    conpassw_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((115, 500), (1350, 75)), manager=manager)

    while running:
        screen.fill(bg)
        manager.draw_ui(screen)

        write("Register", font1, (255, 255, 255), screen, 701, 100)
        write("Email Address", font2, (255, 255, 255), screen, 120, 205)
        write("Username:", font2, (255, 255, 255), screen, 120, 305)
        write("Password:", font2, (255, 255, 255), screen, 120, 405)
        write("Confirm Password", font2, (255, 255, 255), screen, 120, 505)

        mx, my = pygame.mouse.get_pos()

        button_register = Button(120, 600, "Register")
        button_back = Button(1160, 600, "Back")

        refresh = clock.tick(60) / 1000
        manager.update(refresh)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            manager.process_events(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        if button_register.click((mx, my)):
            if clicked:
                email_text = email_entry.get_text().strip()
                username_text = username_entry.get_text().strip()
                password_text = passw_entry.get_text().strip()
                confirm_password_text = conpassw_entry.get_text().strip()
                if len(username_text) < 3:
                    error_scr("Username needs 3 characters minimum")
                elif password_text != confirm_password_text:
                    error_scr("Passwords do not match")

                elif len(password_text) < 8:
                    error_scr("Passwords needs to be 8 characters long")
                else:
                    cursor.execute("INSERT INTO USERS (email, username, password) VALUES (?, ?, ?)",
                                (email_text, username_text, password_text))
                    connection.commit()
                    running = False
                    menu()

        if button_back.click((mx, my)):
            if clicked:
                running = False

        clicked = False
        pygame.display.update()

def login():
    for element in manager.get_root_container().elements[:]:
        element.kill()
    running = True
    clicked = False
    username_entry_login = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((115, 300), (1350, 75)), manager=manager, object_id="#user"
    )
    password_entry_login = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((115, 400), (1350, 75)), manager=manager, object_id="#pass"
    )

    password_entry_login.set_text_hidden(True)

    while running:
        screen.fill(bg)
        manager.draw_ui(screen)

        write("Login", font1, (255, 255, 255), screen, 701, 100)
        write("Username:", font2, (255, 255, 255), screen, 120, 305)
        write("Password:", font2, (255, 255, 255), screen, 120, 405)

        mx, my = pygame.mouse.get_pos()
        button_login = Button(120, 500, "Login")
        button_back = Button(1160, 500, "Back")
        button_forgot = Button(640, 500, "Forgot Password")

        refresh = clock.tick(60) / 1000
        manager.update(refresh)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            manager.process_events(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        if button_login.click((mx, my)):
            if clicked:
                username_text = username_entry_login.get_text().strip()
                password_text = password_entry_login.get_text().strip()
                cursor.execute("SELECT password FROM USERS WHERE username = ?", (username_text,))
                result = cursor.fetchone()
                if result:
                    stored_password = result[0]
                    if stored_password == password_text:
                        menu()
                    else:
                        error_scr("Invalid password")
                else:
                    error_scr("User not found")
        if button_back.click((mx, my)):
            if clicked:
                running = False
                return
        if button_forgot.click((mx,my)):
            if clicked:
                for element in manager.get_root_container().elements[:]:
                    element.kill()
                forgot_password()

        clicked = False
        pygame.display.update()

def forgot_password():
    for element in manager.get_root_container().elements[:]:
        element.kill()

    running = True
    clicked = False

    email = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((115, 300), (1350, 75)), manager=manager, object_id="#email"
    )
    username = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((115, 400), (1350, 75)), manager=manager, object_id="#user"
    )
    new_pass = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((115, 500), (1350, 75)), manager=manager, object_id="#pass"
    )

    while running:
        screen.fill(bg)
        manager.draw_ui(screen)

        write("Forgot Password", font1, (255, 255, 255), screen, 600, 100)
        write("Email:", font2, (255, 255, 255), screen, 120, 305)
        write("Username:", font2, (255, 255, 255), screen, 120, 405)
        write("New password:", font2, (255, 255, 255), screen, 120, 505)

        mx, my = pygame.mouse.get_pos()
        button_reset = Button(120, 600, "Reset")
        button_back = Button(1160, 600, "Back")

        refresh = clock.tick(60) / 1000
        manager.update(refresh)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            manager.process_events(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        if button_reset.click((mx, my)):
            if clicked:
                email_text = email.get_text().strip()
                username_text = username.get_text().strip()
                new_pass_text = new_pass.get_text().strip()

                cursor.execute("SELECT email, username FROM USERS WHERE username = ?", (username_text,))
                result = cursor.fetchone()

                if result:
                    stored_email, stored_username = result
                    if stored_email == email_text and stored_username == username_text:
                        cursor.execute("UPDATE USERS SET password = ? WHERE username = ?", (new_pass_text, username_text))
                        connection.commit()
                        error_scr("Password Reset Successfully")
                        start()
                    else:
                        error_scr("Invalid Email or Username")
                else:
                    error_scr("User not found")

        if button_back.click((mx, my)):
            if clicked:
                running = False

        clicked = False
        pygame.display.update()

def menu():
    clicked = False
    while True:
        screen.fill(bg)
        pygame.display.set_caption("Altitude Adventures")
        write("Main Menu", font1, (255, 255, 255), screen, 630, 100)

        mx, my = pygame.mouse.get_pos()
        playbtn = Button (615, 300, "Play")
        leaderboardbtn = Button(615, 430, "Leaderboard")
        optionsbtn = Button(615, 560, "Options")
        quitbtn=Button(616, 690, "Quit")
        if playbtn.click((mx, my)):
            if clicked:
                lselect()
        if leaderboardbtn.click((mx, my)):
            if clicked:
                leaderboard()
        if optionsbtn.click((mx, my)):
            if clicked:
                opt()
        if quitbtn.click((mx, my)):
            if clicked:
                pygame.quit()
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        pygame.display.update()

def lselect():
    click = False

    key = pygame.key.get_pressed()

    running = True
    while running:


        screen.fill(bg)
        pygame.display.set_caption("Altitude Adventures")
        write("Level Select", font1, (255, 255, 255), screen, 630, 100)

        mx, my = pygame.mouse.get_pos()

        button1 = pygame.Rect(615, 290, 300, 75)
        button2 = pygame.Rect(615, 390, 300, 75)
        button3 = pygame.Rect(615, 490, 300, 75)
        button4 = pygame.Rect(615, 590, 300, 75)
        button5 = pygame.Rect(615, 690, 300, 75)
        if button1.collidepoint((mx, my)):
            if click:
                lvl1(lvl)
        if button2.collidepoint((mx, my)):
            if click:
                if lvl == 2:
                    lvl2(lvl)
                else:
                    error_scr("Complete level 1")

        if button3.collidepoint((mx, my)):
            if click:
                if lvl == 3:
                    lvl3(lvl)
                else:
                    error_scr("Complete level 2")
        if button4.collidepoint((mx,my)):
            if click:
                char_select()

        if button5.collidepoint((mx, my)):
            if click:
                running = False

        pygame.draw.rect(screen, (33, 40, 45), button1)
        pygame.draw.rect(screen, (33, 40, 45), button2)
        pygame.draw.rect(screen, (33, 40, 45), button3)
        pygame.draw.rect(screen, (33, 40 ,45), button4)
        pygame.draw.rect(screen, (33, 40, 45), button5)
        click = False
        write("Level One", font1, (255, 255, 255), screen, 615, 300)
        write("Level Two", font1, (255, 255, 255), screen, 615, 400)
        write("Level Three", font1, (255, 255, 255), screen, 615, 500)
        write("Character Select",font3,(255,255,255),screen,615,600)
        write("Back", font1, (255, 255, 255), screen, 615, 700)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if key[pygame.K_ESCAPE] == True:
                return
            pygame.display.update()

def leaderboard():
    return

def opt():
    click = False
    running = True
    vol = 1.0

    while running:
        pygame.mixer.music.set_volume(vol)
        mx, my = pygame.mouse.get_pos()
        screen.fill(bg)
        pygame.display.set_caption("Altitude Adventures")
        write("Options",font1,(255,255,255),screen,680,100)

        volume = pygame.Rect(100, 150, 410, 75)
        pygame.draw.rect(screen, (33, 40, 45), volume)
        write("Volume", font2, (255, 255, 255), screen, 310, 170)

        volume_decrease = pygame.Rect(100, 150, 75, 75)
        pygame.draw.rect(screen, (33, 40, 45), volume_decrease)
        write("-", font2, (255, 255, 255), screen, 130, 170)

        volume_increase = pygame.Rect(500, 150, 75, 75)
        pygame.draw.rect(screen, (33, 40, 45), volume_increase)
        write("+", font2, (255, 255, 255), screen, 530, 170)

        if volume_increase.collidepoint((mx,my)):
            if click:
                vol = vol + 0.1
                click = False

        elif volume_decrease.collidepoint((mx,my)):
            if click:
                vol = vol - 0.1
                click = False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            manager.process_events(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

def game_opt():
    click = False
    running = True
    vol = 1.0

    while running:
        pygame.mixer.music.set_volume(vol)
        mx, my = pygame.mouse.get_pos()
        screen.fill(bg)
        pygame.display.set_caption("Altitude Adventures")
        write("Options", font1, (255, 255, 255), screen, 680, 100)

        volume = pygame.Rect(100, 150, 410, 75)
        pygame.draw.rect(screen, (33, 40, 45), volume)
        write("Volume", font2, (255, 255, 255), screen, 310, 170)

        volume_decrease = pygame.Rect(100, 150, 75, 75)
        pygame.draw.rect(screen, (33, 40, 45), volume_decrease)
        write("-", font2, (255, 255, 255), screen, 130, 170)

        volume_increase = pygame.Rect(500, 150, 75, 75)
        pygame.draw.rect(screen, (33, 40, 45), volume_increase)
        write("+", font2, (255, 255, 255), screen, 530, 170)

        if volume_increase.collidepoint((mx, my)):
            if vol <= 0:
                if click:
                    vol = vol + 0.1
                    click = False

        elif volume_decrease.collidepoint((mx, my)):
            if vol >= 1:
                if click:
                    vol = vol - 0.1
                    click = False

        vol_txt = str(round(vol * 100 ))
        print(vol_txt)
        write(vol_txt, font2, (255, 255, 255), screen, 310, 190)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            manager.process_events(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

def lvl1(lvl):

    from physics import Player, game_over, en_group, spike_group, coin_group

    world = physics.World(maps.tilemap1, screen)
    player = Player(100, screen_height - 130, screen)
    start_ticks = pygame.time.get_ticks()
    score = 0
    while config.running:

        if game_over == True:
            config.running = False

        screen.fill(bg)
        clock.tick(fps)
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000

        world.draw()

        if game_over == False:
            en_group.update()
            if pygame.sprite.spritecollide(player, coin_group, True):
                score = (score + 100) - seconds

        en_group.draw(screen)
        spike_group.draw(screen)
        coin_group.draw(screen)

        game_over = player.update(screen, game_over)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_opt()

        timer_text = font2.render(f"Time: {seconds}s", True, (255, 255, 255))
        screen.blit(timer_text, (20, 20))
        score_text = font2.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 40))
        player.draw_health(screen)
        pygame.display.update()

    pygame.quit()
    return lvl

def lvl2(lvl):
    return

def lvl3(lvl):
    return

def char_select():
    running = True
    click = False
    show = player1
    playerimg = None
    while running:
        key = pygame.key.get_pressed()
        screen.fill((bg))
        mx, my = pygame.mouse.get_pos()
        pygame.display.set_caption("Altitude Adventures")
        write("Character Select", font1, (255, 255, 255), screen, 600, 100)

        secondbtn = pygame.Rect(615, 690, 300, 75)
        thirdbtn = pygame.Rect(930, 690, 300, 75)
        firstbtn = pygame.Rect(300, 690, 300, 75)
        backbtn = pygame.Rect(50, 50, 300, 75)

        if secondbtn.collidepoint((mx, my)):
            if click:
                show = player2
                config.playerimg = player2

        if thirdbtn.collidepoint((mx, my)):
            if click:
                show = player3
                config.playerimg = player3

        if firstbtn.collidepoint((mx, my)):
            if click:
                show = player1
                config.playerimg = player1
    
        if backbtn.collidepoint((mx, my)):
            if click:
                running = False

        pygame.draw.rect(screen, (33, 40, 45), secondbtn)
        pygame.draw.rect(screen, (33, 40, 45), thirdbtn)
        pygame.draw.rect(screen, (33, 40, 45), firstbtn)
        pygame.draw.rect(screen, (33, 40, 45), backbtn)

        write("One", font2, (255, 255, 255), screen,310 ,720)
        write("Two", font2, (255, 255, 255), screen,630 ,720)
        write("Three", font2, (255, 255, 255), screen,950 ,720)
        write("Back", font2, (255, 255, 255), screen, 70, 70)

        screen.blit(show, (500, 120))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            else:
                click = False

            if key[pygame.K_ESCAPE] == True:
                return

        pygame.display.update()

        return playerimg

start()
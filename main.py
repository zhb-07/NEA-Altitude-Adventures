import pygame
import pygame_gui
import sqlite3
import game

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sounds/bg_sound.mp3")
pygame.mixer.music.play(loops = -1)
height = 805
width = 1535
bg = (89, 120, 142)
bg_image = pygame.image.load("images/bg_image.png")
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((width, height))
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
font1 = pygame.font.SysFont(None, 75)
font2 = pygame.font.SysFont(None, 35)
font3 = pygame.font.SysFont(None, 50)
lvl = 1

print("I LOVE ONIONS!!!!!!!!!!!")
print("Hello World!")

def write(text, font, colour, surface, x, y):
    obj = font.render(text, True, colour)
    rect = obj.get_rect()
    rect.topleft = (x, y)
    surface.blit(obj, rect)

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
    click = False
    while True:
        screen.fill(bg)
        key = pygame.key.get_pressed()
        pygame.display.set_caption("Altitude Adventures")
        write("Altitude Adventures", font1, (255, 255, 255), screen, 501, 100)

        mx, my = pygame.mouse.get_pos()

        button1 = pygame.Rect(615, 300, 300, 75)
        button2 = pygame.Rect(615, 430, 300, 75)
        button3 = pygame.Rect(615, 560, 300, 75)
        if button1.collidepoint((mx, my)):
            if click:
                login()
        if button2.collidepoint((mx, my)):
            if click:
                register()
        if button3.collidepoint((mx, my)):
            if click:
                pygame.quit()
        pygame.draw.rect(screen, (33, 40, 45), button1)
        pygame.draw.rect(screen, (33, 40, 45), button2)
        pygame.draw.rect(screen, (33, 40, 45), button3)
        click = False
        write("Login", font1, (255, 255, 255), screen, 615, 300)
        write("Register", font1, (255, 255, 255), screen, 615, 430)
        write("Quit", font1, (255, 255, 255), screen, 615, 560)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        if key[pygame.K_k] == True:
            menu()
        if key[pygame.K_l] == True:
            lselect()

        pygame.display.update()

def register():
    running = True
    click = False

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

        button_register = pygame.Rect(120, 600, 300, 75)
        pygame.draw.rect(screen, (33, 40, 45), button_register)
        write("Register", font2, (255, 255, 255), screen, 210, 620)

        button_back = pygame.Rect(1160, 600, 300, 75)
        pygame.draw.rect(screen, (33, 40, 45), button_back)
        write("Back", font2, (255, 255, 255), screen, 1280, 620)

        refresh = clock.tick(60) / 1000
        manager.update(refresh)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            manager.process_events(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if button_register.collidepoint((mx, my)) and click:
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

        if button_back.collidepoint((mx, my)) and click:
            running = False

        click = False
        pygame.display.update()

def login():
    for element in manager.get_root_container().elements[:]:
        element.kill()
    running = True
    click = False
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

        button_login = pygame.Rect(120, 500, 300, 75)
        pygame.draw.rect(screen, (33, 40, 45), button_login)
        write("Login", font2, (255, 255, 255), screen, 210, 520)

        button_back = pygame.Rect(1160, 500, 300, 75)
        pygame.draw.rect(screen, (33, 40, 45), button_back)
        write("Back", font2, (255, 255, 255), screen, 1280, 520)

        button_forgot = pygame.Rect(640, 500, 300, 75)
        pygame.draw.rect(screen, (33, 40, 45), button_forgot)
        write("Forgot Password", font2, (255, 255, 255), screen, 705, 520)

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
                    click = True

        if button_login.collidepoint((mx, my)) and click:
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
        if button_back.collidepoint((mx, my)) and click:
            running = False
            return
        if button_forgot.collidepoint((mx,my)) and click:
            for element in manager.get_root_container().elements[:]:
                element.kill()
            forgot_password()

        click = False
        pygame.display.update()

def forgot_password():
    for element in manager.get_root_container().elements[:]:
        element.kill()

    running = True
    click = False

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

        # Display Text Labels
        write("Forgot Password", font1, (255, 255, 255), screen, 600, 100)
        write("Email:", font2, (255, 255, 255), screen, 120, 305)
        write("Username:", font2, (255, 255, 255), screen, 120, 405)
        write("New password:", font2, (255, 255, 255), screen, 120, 505)

        # Buttons
        mx, my = pygame.mouse.get_pos()
        button_reset = pygame.Rect(120, 600, 300, 75)
        pygame.draw.rect(screen, (33, 40, 45), button_reset)
        write("Reset", font2, (255, 255, 255), screen, 210, 620)

        button_back = pygame.Rect(1160, 600, 300, 75)
        pygame.draw.rect(screen, (33, 40, 45), button_back)
        write("Back", font2, (255, 255, 255), screen, 1280, 620)

        # Update UI
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
                click = True

        if button_reset.collidepoint((mx, my)) and click:
            email_text = email.get_text().strip()
            username_text = username.get_text().strip()
            new_pass_text = new_pass.get_text().strip()

            # Fetch user data
            cursor.execute("SELECT email, username FROM USERS WHERE username = ?", (username_text,))
            result = cursor.fetchone()

            if result:
                stored_email, stored_username = result
                if stored_email == email_text and stored_username == username_text:
                    # Update Password
                    cursor.execute("UPDATE USERS SET password = ? WHERE username = ?", (new_pass_text, username_text))
                    connection.commit()
                    error_scr("Password Reset Successfully")
                    start()
                else:
                    error_scr("Invalid Email or Username")
            else:
                error_scr("User not found")

        if button_back.collidepoint((mx, my)) and click:
            running = False

        click = False
        pygame.display.update()

def menu():
    click = False
    while True:
        screen.fill(bg)
        pygame.display.set_caption("Altitude Adventures")
        write("Main Menu", font1, (255, 255, 255), screen, 630, 100)

        mx, my = pygame.mouse.get_pos()

        button1 = pygame.Rect(615, 300, 300, 75)
        button2 = pygame.Rect(615, 430, 300, 75)
        button3 = pygame.Rect(615, 560, 300, 75)
        button4 = pygame.Rect(615, 690, 300, 75)
        if button1.collidepoint((mx, my)):
            if click:
                lselect()
        if button2.collidepoint((mx, my)):
            if click:
                leaderboard()
        if button3.collidepoint((mx, my)):
            if click:
                opt()
        if button4.collidepoint((mx, my)):
            if click:
                pygame.quit()
        pygame.draw.rect(screen, (33, 40, 45), button1)
        pygame.draw.rect(screen, (33, 40, 45), button2)
        pygame.draw.rect(screen, (33, 40, 45), button3)
        pygame.draw.rect(screen, (33, 40, 45), button4)
        click = False
        write("Play", font1, (255, 255, 255), screen, 615, 300)
        write("Leaderboard", font3, (255, 255, 255), screen, 615, 430)
        write("Options", font1, (255, 255, 255), screen, 615, 560)
        write("Quit", font1, (255, 255, 255), screen, 615, 690)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def lselect():
    click = False
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
                lvl1()
        if button2.collidepoint((mx, my)):
            if click:
                if lvl == 2:
                    lvl2()
                else:
                    error_scr("Complete level 1")

        if button3.collidepoint((mx, my)):
            if click:
                if lvl == 3:
                    lvl3()
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
        pygame.draw.rect(screen,(33,40,45),button4)
        pygame.draw.rect(screen, (33, 40, 45), button5)
        click = False
        write("Level One", font1, (255, 255, 255), screen, 615, 300)
        write("Level Two", font1, (255, 255, 255), screen, 615, 400)
        write("Level Three", font1, (255, 255, 255), screen, 615, 500)
        write ("Character Select",font3,(255,255,255),screen,615,600)
        write("Back", font1, (255, 255, 255), screen, 615, 700)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

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
        screen.blit(bg_image, (0, 0))
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

        exitbtn = pygame.Rect(100, 700, 200, 75)
        pygame.draw.rect(screen, (33, 40, 45), exitbtn)
        write("Exit lvl 1", font2, (255, 255, 255), screen, 130, 730)

        if volume_increase.collidepoint((mx,my)):
            if click:
                vol = vol + 0.1
                click = False

        elif volume_decrease.collidepoint((mx,my)):
            if click:
                vol = vol - 0.1
                click = False

        elif exitbtn.collidepoint((mx,my)):
            if click:
                lselect()

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

def lvl1():
    player = game.Player(773, 500)
    ground_level = 730
    platform1 = game.Platform(0, ground_level, 1535, 10)
    platforms = [platform1]
    camera = game.Camera(width, height, game.tilemap)
    running = True
    while running:
        screen.fill(bg)
        game.draw_tilemap(screen, camera)
        keys = pygame.key.get_pressed()
        player.move(keys,0.1)
        player.apply_gravity(platforms)
        player.draw(screen)
        camera.update(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_opt()

        pygame.display.update()
        clock.tick()

def lvl2():
    return

def lvl3():
    return

def char_select():
    return

start()
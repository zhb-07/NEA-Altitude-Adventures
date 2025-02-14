import pygame
import pygame_gui
import sqlite3

pygame.init()
height = 805
width = 1536
bg = (89, 120, 142)
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

print("I LOVE ONIONS!!!!!!!!!!!")

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
        if button_forgot.collidepoint((mx,my)):
            forgot_password()

        click = False
        pygame.display.update()

def forgot_password():
    pass

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
        write("Leaderboard", font1, (255, 255, 255), screen, 615, 430)
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
    return

def leaderboard():
    return

def opt():
    click = False
    running = True

    while running:
        screen.fill(bg)
        pygame.display.set_caption("Altitude Adventures")
        write("Options",font1,(255,255,255),screen,500,100)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

start()
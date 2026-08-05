import sys
import pygame
import colorsys

pygame.init()

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600

WIDTH = DEFAULT_WIDTH
HEIGHT = DEFAULT_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (150, 150, 150)
DARK_GRAY = (40, 40, 40)
GREEN = (0, 255, 0)
RED = (255, 50, 50)
BLUE = (50, 150, 255)

clock = pygame.time.Clock()

PADDLE_WIDTH = 15
DEFAULT_PADDLE_HEIGHT = 100
PADDLE_HEIGHT = DEFAULT_PADDLE_HEIGHT
PADDLE_SPEED = 7

DEFAULT_BALL_SIZE = 15
BALL_SIZE = DEFAULT_BALL_SIZE
INITIAL_SPEED = 5
SPEED_UP = 1.05

font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 48)

state = "MENU"
game_mode = "SOLO"
ai_difficulty = "MEDIUM"

p1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
p2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2

ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = INITIAL_SPEED
ball_speed_y = INITIAL_SPEED

score1 = 0
score2 = 0
game_over = False

selected_option = 0
menu_options = ["Singleplayer (Solo)", "Singleplayer vs AI", "Multiplayer", "Settings", "Quit"]

diff_option = 1
diff_options = ["EASY", "MEDIUM", "HARD", "IMPOSSIBLE"]

width_text = str(WIDTH)
height_text = str(HEIGHT)
paddle_len_text = str(PADDLE_HEIGHT)
ball_size_text = str(BALL_SIZE)

bg_hsv = [0.0, 0.0, 0.0]
paddle_hsv = [0.0, 0.0, 1.0]
ball_hsv = [0.0, 0.0, 1.0]

settings_focus = 0
scroll_y = 0
active_text_box = None
dragging_slider = None
cursor_timer = 0
show_cursor = True

SETTINGS_ITEMS_COUNT = 16

def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))

def apply_all_settings():
    global WIDTH, HEIGHT, PADDLE_HEIGHT, BALL_SIZE, screen, p1_y, p2_y, ball_x, ball_y
    try:
        w = int(width_text)
        h = int(height_text)
        if w >= 400 and h >= 300:
            WIDTH = w
            HEIGHT = h
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
    except ValueError:
        pass

    try:
        p_h = int(paddle_len_text)
        PADDLE_HEIGHT = max(20, min(HEIGHT - 50, p_h))
    except ValueError:
        pass

    try:
        b_s = int(ball_size_text)
        BALL_SIZE = max(5, min(100, b_s))
    except ValueError:
        pass

    p1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    p2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2

def reset_defaults():
    global WIDTH, HEIGHT, PADDLE_HEIGHT, BALL_SIZE, bg_hsv, paddle_hsv, ball_hsv
    global width_text, height_text, paddle_len_text, ball_size_text, screen
    WIDTH = DEFAULT_WIDTH
    HEIGHT = DEFAULT_HEIGHT
    PADDLE_HEIGHT = DEFAULT_PADDLE_HEIGHT
    BALL_SIZE = DEFAULT_BALL_SIZE
    bg_hsv = [0.0, 0.0, 0.0]
    paddle_hsv = [0.0, 0.0, 1.0]
    ball_hsv = [0.0, 0.0, 1.0]
    width_text = str(WIDTH)
    height_text = str(HEIGHT)
    paddle_len_text = str(PADDLE_HEIGHT)
    ball_size_text = str(BALL_SIZE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

def reset_game():
    global p1_y, p2_y, ball_x, ball_y, ball_speed_x, ball_speed_y, score1, score2, game_over
    p1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    p2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed_x = INITIAL_SPEED
    ball_speed_y = INITIAL_SPEED
    score1 = 0
    score2 = 0
    game_over = False

def adjust_scroll_to_focus():
    global scroll_y
    item_y = 120 + settings_focus * 45 + scroll_y
    if item_y > HEIGHT - 100:
        scroll_y -= (item_y - (HEIGHT - 100))
    elif item_y < 120:
        scroll_y += (120 - item_y)

while True:
    cursor_timer += 1
    if cursor_timer % 30 == 0:
        show_cursor = not show_cursor

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        game_mode = "SOLO"
                        reset_game()
                        state = "GAME"
                    elif selected_option == 1:
                        state = "DIFFICULTY_SELECT"
                    elif selected_option == 2:
                        game_mode = "MULTIPLAYER"
                        reset_game()
                        state = "GAME"
                    elif selected_option == 3:
                        width_text = str(WIDTH)
                        height_text = str(HEIGHT)
                        paddle_len_text = str(PADDLE_HEIGHT)
                        ball_size_text = str(BALL_SIZE)
                        settings_focus = 0
                        scroll_y = 0
                        active_text_box = None
                        state = "SETTINGS"
                    elif selected_option == 4:
                        pygame.quit()
                        sys.exit()

        elif state == "DIFFICULTY_SELECT":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    diff_option = (diff_option - 1) % len(diff_options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    diff_option = (diff_option + 1) % len(diff_options)
                elif event.key == pygame.K_RETURN:
                    ai_difficulty = diff_options[diff_option]
                    game_mode = "VS_AI"
                    reset_game()
                    state = "GAME"
                elif event.key == pygame.K_ESCAPE:
                    state = "MENU"

        elif state == "SETTINGS":
            start_y = 120 + scroll_y

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll_y = min(0, scroll_y + 40)
                elif event.button == 5:
                    scroll_y = max(-400, scroll_y - 40)
                elif event.button == 1:
                    mx, my = event.pos
                    active_text_box = None
                    
                    text_boxes = [
                        (0, WIDTH // 2 + 20, start_y, 160, 35),
                        (1, WIDTH // 2 + 20, start_y + 45, 160, 35),
                        (2, WIDTH // 2 + 20, start_y + 90, 160, 35),
                        (3, WIDTH // 2 + 20, start_y + 135, 160, 35)
                    ]
                    for idx, bx, by, bw, bh in text_boxes:
                        if bx <= mx <= bx + bw and by <= my <= by + bh:
                            active_text_box = idx
                            settings_focus = idx
                            break

                    sliders = [
                        (4, bg_hsv, 0, start_y + 180),
                        (5, bg_hsv, 1, start_y + 225),
                        (6, bg_hsv, 2, start_y + 270),
                        (7, paddle_hsv, 0, start_y + 315),
                        (8, paddle_hsv, 1, start_y + 360),
                        (9, paddle_hsv, 2, start_y + 405),
                        (10, ball_hsv, 0, start_y + 450),
                        (11, ball_hsv, 1, start_y + 495),
                        (12, ball_hsv, 2, start_y + 540)
                    ]
                    for s_idx, target_hsv, hsv_i, sy in sliders:
                        sx = WIDTH // 2 + 20
                        if sx <= mx <= sx + 160 and sy <= my <= sy + 35:
                            dragging_slider = (target_hsv, hsv_i)
                            settings_focus = s_idx
                            rel_x = max(0, min(160, mx - sx))
                            target_hsv[hsv_i] = rel_x / 160.0
                            break

                    save_y = start_y + 600
                    reset_y = start_y + 645
                    cancel_y = start_y + 690

                    if WIDTH // 2 - 120 <= mx <= WIDTH // 2 + 120:
                        if save_y <= my <= save_y + 35:
                            apply_all_settings()
                            state = "MENU"
                        elif reset_y <= my <= reset_y + 35:
                            reset_defaults()
                        elif cancel_y <= my <= cancel_y + 35:
                            state = "MENU"

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging_slider = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging_slider is not None:
                    target_hsv, hsv_i = dragging_slider
                    mx = event.pos[0]
                    sx = WIDTH // 2 + 20
                    rel_x = max(0, min(160, mx - sx))
                    target_hsv[hsv_i] = rel_x / 160.0

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "MENU"
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    settings_focus = (settings_focus - 1) % SETTINGS_ITEMS_COUNT
                    active_text_box = settings_focus if settings_focus in [0, 1, 2, 3] else None
                    adjust_scroll_to_focus()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    settings_focus = (settings_focus + 1) % SETTINGS_ITEMS_COUNT
                    active_text_box = settings_focus if settings_focus in [0, 1, 2, 3] else None
                    adjust_scroll_to_focus()
                elif event.key == pygame.K_LEFT and settings_focus in range(4, 13):
                    sliders_map = [
                        (bg_hsv, 0), (bg_hsv, 1), (bg_hsv, 2),
                        (paddle_hsv, 0), (paddle_hsv, 1), (paddle_hsv, 2),
                        (ball_hsv, 0), (ball_hsv, 1), (ball_hsv, 2)
                    ]
                    target, h_i = sliders_map[settings_focus - 4]
                    target[h_i] = max(0.0, target[h_i] - 0.05)
                elif event.key == pygame.K_RIGHT and settings_focus in range(4, 13):
                    sliders_map = [
                        (bg_hsv, 0), (bg_hsv, 1), (bg_hsv, 2),
                        (paddle_hsv, 0), (paddle_hsv, 1), (paddle_hsv, 2),
                        (ball_hsv, 0), (ball_hsv, 1), (ball_hsv, 2)
                    ]
                    target, h_i = sliders_map[settings_focus - 4]
                    target[h_i] = min(1.0, target[h_i] + 0.05)
                elif event.key == pygame.K_RETURN:
                    if settings_focus == 13 or active_text_box is not None:
                        apply_all_settings()
                        state = "MENU"
                    elif settings_focus == 14:
                        reset_defaults()
                    elif settings_focus == 15:
                        state = "MENU"
                elif event.key == pygame.K_BACKSPACE:
                    if active_text_box == 0:
                        width_text = width_text[:-1]
                    elif active_text_box == 1:
                        height_text = height_text[:-1]
                    elif active_text_box == 2:
                        paddle_len_text = paddle_len_text[:-1]
                    elif active_text_box == 3:
                        ball_size_text = ball_size_text[:-1]
                else:
                    if event.unicode.isdigit() and active_text_box is not None:
                        if active_text_box == 0 and len(width_text) < 4:
                            width_text += event.unicode
                        elif active_text_box == 1 and len(height_text) < 4:
                            height_text += event.unicode
                        elif active_text_box == 2 and len(paddle_len_text) < 3:
                            paddle_len_text += event.unicode
                        elif active_text_box == 3 and len(ball_size_text) < 3:
                            ball_size_text += event.unicode

        elif state == "GAME":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "MENU"
                if game_over and event.key == pygame.K_r:
                    reset_game()

    if state == "GAME" and not game_over:
        keys = pygame.key.get_pressed()
        
        if (keys[pygame.K_w]) and p1_y > 0:
            p1_y -= PADDLE_SPEED
        if (keys[pygame.K_s]) and p1_y < HEIGHT - PADDLE_HEIGHT:
            p1_y += PADDLE_SPEED

        if game_mode == "MULTIPLAYER":
            if keys[pygame.K_UP] and p2_y > 0:
                p2_y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and p2_y < HEIGHT - PADDLE_HEIGHT:
                p2_y += PADDLE_SPEED

        elif game_mode == "VS_AI":
            ai_center = p2_y + PADDLE_HEIGHT // 2
            
            if ai_difficulty == "EASY":
                ai_speed = 3
                if abs(ai_center - ball_y) > 35:
                    if ai_center < ball_y and p2_y < HEIGHT - PADDLE_HEIGHT:
                        p2_y += ai_speed
                    elif ai_center > ball_y and p2_y > 0:
                        p2_y -= ai_speed
            elif ai_difficulty == "MEDIUM":
                ai_speed = 5.5
                if abs(ai_center - ball_y) > 20:
                    if ai_center < ball_y and p2_y < HEIGHT - PADDLE_HEIGHT:
                        p2_y += ai_speed
                    elif ai_center > ball_y and p2_y > 0:
                        p2_y -= ai_speed
            elif ai_difficulty == "HARD":
                ai_speed = 7.5
                if abs(ai_center - ball_y) > 10:
                    if ai_center < ball_y and p2_y < HEIGHT - PADDLE_HEIGHT:
                        p2_y += ai_speed
                    elif ai_center > ball_y and p2_y > 0:
                        p2_y -= ai_speed
            elif ai_difficulty == "IMPOSSIBLE":
                p2_y = ball_y - PADDLE_HEIGHT // 2
                if p2_y < 0:
                    p2_y = 0
                if p2_y > HEIGHT - PADDLE_HEIGHT:
                    p2_y = HEIGHT - PADDLE_HEIGHT

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_speed_y *= -1

        if game_mode == "SOLO":
            if ball_x >= WIDTH - BALL_SIZE:
                ball_speed_x *= -1
        else:
            if ball_x >= WIDTH - BALL_SIZE:
                score1 += 1
                ball_x = WIDTH // 2
                ball_y = HEIGHT // 2
                ball_speed_x = -INITIAL_SPEED
                ball_speed_y = INITIAL_SPEED

        p1_rect = pygame.Rect(30, p1_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball_rect = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)

        if ball_rect.colliderect(p1_rect) and ball_speed_x < 0:
            ball_speed_x *= -1
            ball_speed_x *= SPEED_UP
            ball_speed_y *= SPEED_UP
            if game_mode == "SOLO":
                score1 += 1

        if game_mode != "SOLO":
            p2_rect = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, p2_y, PADDLE_WIDTH, PADDLE_HEIGHT)
            if ball_rect.colliderect(p2_rect) and ball_speed_x > 0:
                ball_speed_x *= -1
                ball_speed_x *= SPEED_UP
                ball_speed_y *= SPEED_UP

        if ball_x < 0:
            if game_mode == "SOLO":
                game_over = True
            else:
                score2 += 1
                ball_x = WIDTH // 2
                ball_y = HEIGHT // 2
                ball_speed_x = INITIAL_SPEED
                ball_speed_y = INITIAL_SPEED

    bg_rgb = hsv_to_rgb(*bg_hsv)
    paddle_rgb = hsv_to_rgb(*paddle_hsv)
    ball_rgb = hsv_to_rgb(*ball_hsv)

    screen.fill(bg_rgb)

    if state == "MENU":
        title = big_font.render("PONG GAME", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 6))
        
        for i, option in enumerate(menu_options):
            color = WHITE if i == selected_option else GRAY
            text = font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3 + i * 45))

    elif state == "DIFFICULTY_SELECT":
        title = big_font.render("SELECT DIFFICULTY", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 6))

        for i, option in enumerate(diff_options):
            color = WHITE if i == diff_option else GRAY
            text = font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3 + i * 45))

        back_text = font.render("Press ESC to go back", True, LIGHT_GRAY)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 80))

    elif state == "SETTINGS":
        start_y = 120 + scroll_y

        title = big_font.render("SETTINGS", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, start_y - 70))

        text_items = [
            ("Width:", width_text, 0),
            ("Height:", height_text, 1),
            ("Paddle Length:", paddle_len_text, 2),
            ("Ball Size:", ball_size_text, 3)
        ]

        for label, val_text, f_idx in text_items:
            curr_y = start_y + f_idx * 45
            if -40 < curr_y < HEIGHT:
                lbl = font.render(label, True, WHITE)
                screen.blit(lbl, (WIDTH // 2 - 180, curr_y))

                box_color = GREEN if active_text_box == f_idx or settings_focus == f_idx else GRAY
                pygame.draw.rect(screen, DARK_GRAY, (WIDTH // 2 + 20, curr_y, 160, 35))
                pygame.draw.rect(screen, box_color, (WIDTH // 2 + 20, curr_y, 160, 35), 2)

                display_str = val_text + ("|" if active_text_box == f_idx and show_cursor else "")
                val_rendered = font.render(display_str, True, WHITE)
                screen.blit(val_rendered, (WIDTH // 2 + 30, curr_y + 4))

        slider_items = [
            ("BG Hue:", bg_hsv, 0, 4),
            ("BG Saturation:", bg_hsv, 1, 5),
            ("BG Value:", bg_hsv, 2, 6),
            ("Paddle Hue:", paddle_hsv, 0, 7),
            ("Paddle Saturation:", paddle_hsv, 1, 8),
            ("Paddle Value:", paddle_hsv, 2, 9),
            ("Ball Hue:", ball_hsv, 0, 10),
            ("Ball Saturation:", ball_hsv, 1, 11),
            ("Ball Value:", ball_hsv, 2, 12)
        ]

        for label, target_hsv, hsv_i, f_idx in slider_items:
            curr_y = start_y + (f_idx) * 45
            if -40 < curr_y < HEIGHT:
                lbl = font.render(label, True, WHITE)
                screen.blit(lbl, (WIDTH // 2 - 180, curr_y))

                box_color = GREEN if settings_focus == f_idx else GRAY
                sx = WIDTH // 2 + 20
                pygame.draw.rect(screen, DARK_GRAY, (sx, curr_y + 12, 160, 10))
                pygame.draw.rect(screen, box_color, (sx, curr_y + 12, 160, 10), 1)

                handle_x = sx + int(target_hsv[hsv_i] * 160)
                pygame.draw.circle(screen, GREEN if settings_focus == f_idx else BLUE, (handle_x, curr_y + 17), 8)

        btn_save_y = start_y + 600
        btn_reset_y = start_y + 645
        btn_cancel_y = start_y + 690

        if -40 < btn_save_y < HEIGHT:
            color = GREEN if settings_focus == 13 else GRAY
            btn1 = font.render("[ Save & Apply ]", True, color)
            screen.blit(btn1, (WIDTH // 2 - btn1.get_width() // 2, btn_save_y))

        if -40 < btn_reset_y < HEIGHT:
            color = RED if settings_focus == 14 else GRAY
            btn2 = font.render("[ Reset to Defaults ]", True, color)
            screen.blit(btn2, (WIDTH // 2 - btn2.get_width() // 2, btn_reset_y))

        if -40 < btn_cancel_y < HEIGHT:
            color = WHITE if settings_focus == 15 else GRAY
            btn3 = font.render("[ Cancel ]", True, color)
            screen.blit(btn3, (WIDTH // 2 - btn3.get_width() // 2, btn_cancel_y))

        hint_text = font.render("Click or UP/DOWN to focus | Drag Sliders | ESC: Exit", True, LIGHT_GRAY)
        screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT - 30))

    elif state == "GAME":
        pygame.draw.rect(screen, paddle_rgb, (30, p1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        
        if game_mode != "SOLO":
            pygame.draw.rect(screen, paddle_rgb, (WIDTH - 30 - PADDLE_WIDTH, p2_y, PADDLE_WIDTH, PADDLE_HEIGHT))

        pygame.draw.ellipse(screen, ball_rgb, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

        text_color = WHITE if bg_hsv[2] < 0.5 else BLACK

        if game_mode == "SOLO":
            score_text = font.render(f"Score: {score1}", True, text_color)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
            ctrl_text = font.render("Controls: W/S or UP/DOWN | Press ESC for Menu", True, LIGHT_GRAY)
            screen.blit(ctrl_text, (WIDTH // 2 - ctrl_text.get_width() // 2, HEIGHT - 30))
        elif game_mode == "VS_AI":
            score_text = font.render(f"P1: {score1}  |  AI ({ai_difficulty}): {score2}", True, text_color)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
            ctrl_text = font.render("Controls: P1 [W/S] | Press ESC for Menu", True, LIGHT_GRAY)
            screen.blit(ctrl_text, (WIDTH // 2 - ctrl_text.get_width() // 2, HEIGHT - 30))
        elif game_mode == "MULTIPLAYER":
            score_text = font.render(f"P1: {score1}  |  P2: {score2}", True, text_color)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
            ctrl_text = font.render("Controls: P1 [W/S]  vs  P2 [UP/DOWN] | Press ESC for Menu", True, LIGHT_GRAY)
            screen.blit(ctrl_text, (WIDTH // 2 - ctrl_text.get_width() // 2, HEIGHT - 30))

        if game_over:
            msg1 = big_font.render("GAME OVER!", True, text_color)
            msg2 = font.render("Press 'R' to Restart", True, text_color)
            screen.blit(msg1, (WIDTH // 2 - msg1.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.flip()
    clock.tick(60)

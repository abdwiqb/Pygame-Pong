import random
import pygame
import sys

# CONST
FPS = 60
EVENT_TICK_RATE = 1
WIN_POINTS = 9
OPPONENT_DELAY = 1.5
CLOCK = pygame.time.Clock()
WIDTH, HEIGHT = 1000, 800
BALL_SIZE, BALL_XSPEED, BALL_YSPEED = 9, 4, 2
PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED = 10, 75, 5
TEXT_SIZE = 40
# COLOR
MAIN_COLOR = (255, 255, 255)
BG_COLOR = (75, 75, 75)
SECONDARY_COLOR = (140, 140, 140)
DANGER_COLOR = (255, 0, 0)
TEXT_COLOR = (25, 25, 25)
# FONT
pygame.font.init()
text_font = pygame.font.SysFont('Comic sans', TEXT_SIZE)
# PLAYER STUFF
ball_spawn_side = -1
ball_xspeed, ball_yspeed = 5 * -ball_spawn_side, 3 * -ball_spawn_side
player_one_speed, player_two_speed = 0, 0
text_player_one = text_font.render("PL", False, TEXT_COLOR)
text_player_two = text_font.render("OP", False, TEXT_COLOR)
desc = text_font.render("Made with Pygame", False, TEXT_COLOR)
title = text_font.render("PYPONG", False, TEXT_COLOR)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyPong")


class Ball:
    def __init__(self, is_clone, is_danger, color, side):
        self.body = pygame.Rect(WIDTH/2-(WIDTH/7*side)-BALL_SIZE/2,
                                HEIGHT/2-BALL_SIZE/2, BALL_SIZE, BALL_SIZE)

        self.xspeed = BALL_XSPEED*-side
        self.yspeed = BALL_YSPEED
        self.is_clone = is_clone
        self.is_danger = is_danger
        self.color = color
        self.tick = EVENT_TICK_RATE


class Paddle:
    def __init__(self, xpos):
        self.body = pygame.Rect(xpos, HEIGHT/2-PADDLE_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.score = 0
        self.speed = 1
        self.speed_multiplier = 1


# OBJ
balls = [Ball(False, False, MAIN_COLOR, ball_spawn_side)]
paddles = [PLAYER_ONE := Paddle(WIDTH-WIDTH/20), PLAYER_TWO := Paddle(WIDTH/20)]
#          PLAYER                                


def ball_out(ball):

    global ball_spawn_side

    if ball.body.left <= 0:
        PLAYER_ONE.score += 1
        ball_spawn_side = 1
    elif ball.body.right >= WIDTH:
        PLAYER_TWO.score += 1
        ball_spawn_side = -1
    if ball.is_clone:
        del ball.body
        balls.remove(ball)
    else:
        ball.body.x = WIDTH / 2 - (WIDTH / 7 * -ball_spawn_side) - BALL_SIZE / 2
        ball.body.y = HEIGHT / 2 - BALL_SIZE / 2
        ball.xspeed *= -1
        ball.yspeed *= -1


def mod_paddle(paddle, size, speed, speed_multiplier):
    global PADDLE_SPEED
    paddle.body.height = PADDLE_HEIGHT*size
    paddle.speed = speed * speed_multiplier


def mod_ball(ball, size, speed):
    ball.body.width = BALL_SIZE*size
    ball.body.height = BALL_SIZE*size
    ball.xspeed = BALL_XSPEED*speed
    ball.yspeed = BALL_YSPEED*speed


def do_rand_event(ball, side, paddle):
    if ball.tick >= 0 or ball.is_clone:
        ball.tick -= 1
        return 0
    for paddle_ in paddles:
        mod_paddle(paddle_, 1, 1, 1)
    mod_ball(ball, 1, 1)
    ball.tick = EVENT_TICK_RATE
    choice = random.choice([1, 2, 3])
    if choice == 3:
        mod_ball(ball, random.choice([1, 2, 3]), random.choice([1, 1.5]))
        mod_paddle(paddle, random.choice([0.75, 1, 1.5]), random.choice([1, 2]), random.choice([1, 1, -1]))
    elif choice == 2:
        balls.append(Ball(True, True, DANGER_COLOR, side))
    else:
        balls.append(Ball(True, False, SECONDARY_COLOR, side))


def ball_movement():
    for ball in balls:
        ball.body.x += ball.xspeed
        ball.body.y += ball.yspeed

        if ball.body.top <= 0 or ball.body.bottom >= HEIGHT:
            ball.yspeed *= -1
        if ball.body.right <= 0 or ball.body.left >= WIDTH:
            if ball.is_danger:
                ball.xspeed *= -1
            else:
                ball_out(ball)
                break
        if ball.body.colliderect(PLAYER_ONE.body) or ball.body.colliderect(PLAYER_TWO.body):
            if ball.body.colliderect(PLAYER_ONE.body):
                side = 1
                collide = PLAYER_ONE
            else:
                side = -1
                collide = PLAYER_TWO
            ball.body.left -= BALL_SIZE * (ball.xspeed / abs(ball.xspeed))
            ball.xspeed *= -1
            if ball.is_danger:
                if collide.score < 1:
                    for paddle in paddles:
                        paddle.score += 1
                        collide.score -= 1
                else:
                    collide.score -= 1
                del ball.body
                balls.remove(ball)
                break
            do_rand_event(ball, side, collide)


def paddle_movement():
    PLAYER_ONE.body.y += player_one_speed*PLAYER_ONE.speed
    PLAYER_TWO.body.y += player_two_speed*PLAYER_TWO.speed
    if PLAYER_ONE.body.top <= 0-HEIGHT/50:
        PLAYER_ONE.body.bottom = HEIGHT
    if PLAYER_ONE.body.bottom >= HEIGHT+HEIGHT/50:
        PLAYER_ONE.body.top = 0
    if PLAYER_TWO.body.top <= 0-HEIGHT/50:
        PLAYER_TWO.body.bottom = HEIGHT
    if PLAYER_TWO.body.bottom >= HEIGHT+HEIGHT/50:
        PLAYER_TWO.body.top = 0


def draw_window():

    WIN.fill((0, 0, 0))

    pygame.draw.aaline(WIN, TEXT_COLOR, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    WIN.blit(text_font.render(str(PLAYER_TWO.score), False, BG_COLOR), (WIDTH/4-TEXT_SIZE/2, 50))
    WIN.blit(text_font.render(str(PLAYER_ONE.score), False, BG_COLOR), ((WIDTH/4)*3-TEXT_SIZE/2, 50))
    WIN.blit(text_player_two, (WIDTH / 4 - TEXT_SIZE / 2, HEIGHT/5*4))
    WIN.blit(text_player_one, ((WIDTH / 4) * 3 - TEXT_SIZE / 2, HEIGHT/5*4))
    WIN.blit(title, (WIDTH/6, HEIGHT/2-TEXT_SIZE/2))
    WIN.blit(desc, (WIDTH / 6*3.35, HEIGHT / 2 - TEXT_SIZE / 2))

    for ball in balls:
        pygame.draw.rect(WIN, ball.color, ball.body)
    pygame.draw.rect(WIN, MAIN_COLOR, PLAYER_ONE.body)
    pygame.draw.rect(WIN, MAIN_COLOR, PLAYER_TWO.body)

    pygame.display.update()


def end_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        WIN.fill((0, 0, 0))
        if PLAYER_ONE.score > PLAYER_TWO.score:
            WIN.blit(text_font.render("PLAYER WINS", False, MAIN_COLOR),
                     (WIDTH / 2-TEXT_SIZE*3.5, HEIGHT / 2-TEXT_SIZE/2))
        else:
            WIN.blit(text_font.render("OPPONENT WINS", False, DANGER_COLOR),
                     (WIDTH / 2-TEXT_SIZE*4.5, HEIGHT / 2-TEXT_SIZE/2))
        WIN.blit(text_font.render(str(PLAYER_TWO.score), False, BG_COLOR),
                 (WIDTH / 4 - TEXT_SIZE / 2, HEIGHT/2-TEXT_SIZE/2))
        WIN.blit(text_font.render(str(PLAYER_ONE.score), False, BG_COLOR),
                 ((WIDTH / 4) * 3 - TEXT_SIZE / 2, HEIGHT/2-TEXT_SIZE/2))
        pygame.display.update()


def check_points():
    if (PLAYER_ONE.score >= WIN_POINTS and PLAYER_TWO.score+1 < PLAYER_ONE.score or
            PLAYER_TWO.score >= WIN_POINTS and PLAYER_ONE.score+1 < PLAYER_TWO.score):
        end_screen()


def main():

    global player_one_speed, player_two_speed

    while True:
        check_points()

        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_one_speed -= PADDLE_SPEED
                if event.key == pygame.K_DOWN:
                    player_one_speed += PADDLE_SPEED
                if event.key == pygame.K_w:
                    player_two_speed -= PADDLE_SPEED
                if event.key == pygame.K_s:
                    player_two_speed += PADDLE_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player_one_speed += PADDLE_SPEED
                if event.key == pygame.K_DOWN:
                    player_one_speed -= PADDLE_SPEED
                if event.key == pygame.K_w:
                    player_two_speed += PADDLE_SPEED
                if event.key == pygame.K_s:
                    player_two_speed -= PADDLE_SPEED

        ball_movement()
        paddle_movement()

        draw_window()


if __name__ == "__main__":
    main()

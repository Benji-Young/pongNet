import pygame
from ball import Ball
from defs import *
from paddle import Paddle, PaddleCollection


def update_label(data, title, x, y, display, font):
    label = font.render("{} {}".format(title, data), 1, DATA_FONT_COLOUR)
    display.blit(label, (x,y))
    return y

def update_data_labels(display, dt, game_time, font, iteration, paddle_count):
    y_pos = 0
    gap = 20
    x_pos = 10
    y_pos = update_label(round(1000/dt,2), "FPS", x_pos, y_pos + gap, display, font)
    y_pos = update_label(round(game_time/1000,2), "Game time", x_pos, y_pos + gap, display, font)
    y_pos = update_label(iteration, "Iteration", x_pos, y_pos + gap, display, font)
    y_pos = update_label(paddle_count, "Right side paddle count", x_pos, y_pos + gap, display, font)
    
def reset(left, right, ball, score, position):
    left.evolve_pop()
    right.evolve_pop()
    score = 0
    ball.reset(left.paddles, right.paddles, score)
    return 0

def paddle_count(paddles):
    count = 0
    for p in paddles:
        if p.state == PADDLE_ALIVE:
            count += 1
    return count



def play_pong():
    
    pygame.init()
    display = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("PongAI")
    
    timer = pygame.time.Clock()
    dt = 0
    game_time = 0
    score = 0
    iteration = 0
    
    background = pygame.image.load(BACKGROUND_PATH).convert()
    label_font = pygame.font.SysFont("monospace", DATA_FONT_SIZE)
    game_active = True
    
    player = Paddle(display, 25, SCREEN_H/2)
    left = PaddleCollection(display, 25, SCREEN_H/2)
    right = PaddleCollection(display, SCREEN_W-25, SCREEN_H/2)
    ball = Ball(SCREEN_W/2, SCREEN_H/2, display, left.paddles, right.paddles, score)
    
    position = False
    
    while game_active:
        dt = timer.tick(FPS)
        game_time += dt
        
        display.blit(background, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
             
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            player.move_up(dt/1000)
        elif pressed[pygame.K_DOWN]:
            player.move_down(dt/1000)
        
        score = ball.return_score()
        ball.update(dt/1000)
        right.update_paddles(dt/1000, ball)
        left.update_paddles(dt/1000, ball)
        update_data_labels(display, dt, game_time, label_font, iteration, paddle_count(right.paddles))
        
        temp = 0
        for p in left.paddles:
            temp += p.state
        if temp == PADDLE_COLLECTION_SIZE:
            iteration += 1
            position == False
            game_time = reset(left, right, ball, score, position)
        temp = 0
        for p in right.paddles:
            temp += p.state
        if temp == PADDLE_COLLECTION_SIZE:
            iteration += 1
            position == True
            game_time = reset(left, right, ball, score, position)
        
        pygame.display.update()


if __name__ == "__main__":
    play_pong()
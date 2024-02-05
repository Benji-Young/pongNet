from defs import *
import pygame
import random
from nnet import Nnet
import numpy as np

class Paddle:
    
    def __init__(self, display, x, y):
        self.image = pygame.image.load(PADDLE_PATH).convert()
        self.rect = self.image.get_rect()
        self.display = display
        self.score = 0
        self.set_position(x, y)
        self.ball_speed = BALL_H
        self.nnet = Nnet(NNET_INPUTS, NNET_HIDDEN, NNET_OUTPUTS)
        self.fitness = 0
        self.state = PADDLE_ALIVE

    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        
    def move_up(self, dt):
        if self.rect.top > 0:
            self.rect.centery -= PADDLE_SPEED * dt
        else:
            self.rect.top = 0
            
    def move_down(self, dt):
        if self.rect.bottom < SCREEN_H:
            self.rect.centery += PADDLE_SPEED * dt
        else:
            self.rect.bottom = SCREEN_H
            
    def assign_fitness(self, ball):
        if ball.rect.centery < self.rect.centery:
            self.fitness = self.rect.top - ball.rect.top
        else:
            self.fitness = self.rect.bottom - ball.rect.bottom
        
        self.fitness = -(abs(self.fitness))
            
    def update(self):
        if self.state == PADDLE_ALIVE:
            self.display.blit(self.image, (self.rect.x, self.rect.y))
        
    def update_score(self):
        self.score += 1
        
    def update_ball_speed(self, bs):
        self.ball_speed = bs
        
    def move(self, dt, ball):
        inputs = self.get_inputs(ball)
        val = self.nnet.get_max_value(inputs)
        if val[0] == DOWN_CHANCE:
            self.move_down(dt)
        elif val[1 == UP_CHANCE]:
            self.move_up(dt)
            
    def get_inputs(self, ball):
        horizonatal_distance = ball.rect.right - self.rect.centerx
        vertical_distance = (self.rect.centery) - (ball.rect.centery)
        
        inputs = [
                  ((horizonatal_distance / SCREEN_W) * 0.99) + 0.01,
                  (((vertical_distance + Y_SHIFT) / NORMALIZER) * 0.99) + 0.01
                  ]
        
        return inputs
        
    def create_offspring(p1 ,p2, display, x, y):
        new_paddle = Paddle(display, x, y)
        new_paddle.nnet.create_mixed_weights(p1.nnet, p2.nnet)
        return new_paddle
    
    def reset(self, x, y):
        self.score = 0
        self.fitness = 0
        self.ball_speed = BALL_H
        self.set_position(x, y)
        self.state = PADDLE_ALIVE
        
        
class PaddleCollection:
    
    def __init__(self, display, x, y):
        self.paddles = []
        self.display = display
        self.generate_paddles(x, y)
        self.x = x
        self.y = y
        
    def generate_paddles(self,x,y):
        for xr in range(PADDLE_COLLECTION_SIZE):
            self.paddles.append(Paddle(self.display, x, y))
            
    def update_paddles(self, dt, ball):
        for paddle in self.paddles:
            if paddle.state == PADDLE_ALIVE:
                paddle.move(dt, ball)
                paddle.update()
            
    def evolve_pop(self):
        for p in self.paddles:
            p.fitness += p.score * p.ball_speed
            
        self.paddles.sort(key=lambda x: x.fitness, reverse=True)
        
        cut_off = int(len(self.paddles) * MUTATION_CUT_OFF)
        good_paddles = self.paddles[0:cut_off]
        bad_paddles = self.paddles[cut_off:]
        num_bad_to_take = int(len(self.paddles) * MUTATION_BAD_TO_KEEP)
        
        for p in bad_paddles:
            p.nnet.modify_weights()
            
        new_paddles = []
        
        idx_bad_to_take = np.random.choice(np.arange(len(bad_paddles)), num_bad_to_take, replace=False)
        
        for index in idx_bad_to_take:
            new_paddles.append(bad_paddles[index])
            
        new_paddles.extend(good_paddles)
        
        children_needed = len(self.paddles) - len(new_paddles)
        
        while len(new_paddles) < len(self.paddles):
            idx_to_breed = np.random.choice(np.arange(len(good_paddles)), 2, replace=False)
            if idx_to_breed[0] != idx_to_breed[1]:
                new_paddle = Paddle.create_offspring(good_paddles[idx_to_breed[0]], good_paddles[idx_to_breed[1]], self.display, self.x, self.y)
                if random.random() < MUTATION_MODIFY_CHANCE_LIMIT:
                    new_paddle.nnet.modify_weights()
                new_paddles.append(new_paddle)
        
        for paddle in self.paddles:
            paddle.reset(self.x, self.y)
        
        self.paddles = new_paddles
        
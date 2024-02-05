from pickle import TRUE
from random import random
import pygame
from defs import *
import random

class Ball:
    def __init__(self, x, y, display, left, right, score):
        self.image = pygame.image.load(BALL_PATH).convert_alpha()
        self.rect = self.image.get_rect()
        self.vel_v = self.get_vertical_vel()
        self.vel_h = BALL_H
        self.left = left
        self.right = right
        self.score = score
        self.display = display
        self.rect.centerx = x
        self.rect.centery = y
        self.collide_player = False
        self.collide_paddle = False
        
    def get_vertical_vel(self):
        return random.randint(0, BALL_V*2) - BALL_V
    
    def move_ball(self, dt):
        # vertical
        if self.rect.top <= 0:
            self.rect.top = 1
            self.vel_v = -self.vel_v
        elif self.rect.bottom >= SCREEN_H:
            self.rect.bottom = SCREEN_H - 1
            self.vel_v = -self.vel_v
        self.rect.centery += (self.vel_v * dt)
        
        # horizontal
        # if (not self.collide_player) and self.rect.centery >= self.player.rect.top and self.rect.centery <= self.player.rect.bottom and self.rect.left < self.player.rect.right and self.rect.left > self.player.rect.left:
        #     self.vel_h = -self.vel_h
        #     self.vel_v = self.get_vertical_vel()
        #     self.collide_player = True
        #     self.collide_paddle = False
        
        collision = False
        ball_hit = False
        one_hit = False
        for p in self.left:
            if self.rect.left <= p.rect.right-5:
                if self.rect.left <= p.rect.right and self.rect.left >= p.rect.left and self.rect.top <= p.rect.bottom and self.rect.bottom >= p.rect.top and p.state == PADDLE_ALIVE:
                    if not one_hit:
                        self.vel_h -= 10
                        one_hit = True
                    ball_hit = True
                    p.ball_speed = self.vel_h
                    p.score += 1
                if p.ball_speed != self.vel_h or not one_hit:
                    p.state = PADDLE_DEAD
                    #self.left.remove(p)
        if ball_hit:
            one_hit = False
            ball_hit = False
            self.vel_h = -self.vel_h
            self.rect.x = p.rect.right+5
            self.vel_v = self.get_vertical_vel()
            
            
        for p in self.right:
            if self.rect.right >= p.rect.left +5:
                if self.rect.right >= p.rect.left and self.rect.right <= p.rect.right and self.rect.top <= p.rect.bottom and self.rect.bottom >= p.rect.top and p.state == PADDLE_ALIVE:
                    collision = True
                    one_hit = True
                    p.ball_speed = self.vel_h
                    p.score += 1
                if p.ball_speed != self.vel_h or not one_hit:
                    p.state = PADDLE_DEAD
        if collision:
            collision = False
            self.vel_h = -self.vel_h
            self.vel_v = self.get_vertical_vel()
        
        self.rect.centerx += (self.vel_h * dt)
        
        
        
    def reset(self, left, right, score):
        self.rect.center = (SCREEN_W/2, SCREEN_H/2) 
        self.vel_h = BALL_H
        self.left = left
        self.right = right
        self.score = score
        self.collide_player = False
        self.collide_paddle = False
        self.vel_v = self.get_vertical_vel()
    
    def update(self, dt):
        self.move_ball(dt)
        self.display.blit(self.image, (self.rect.centerx, self.rect.centery))
        
    def return_score(self):
        return self.score
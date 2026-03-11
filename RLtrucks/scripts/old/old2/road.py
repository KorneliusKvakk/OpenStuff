# %%
"""
Created on June 5 10:11 2023
@author: Johan Andreas Stendal
"""
import math
import random

import pygame

from config import *
from utilities import *

class Road:
    def __init__(self, screen, road_name, road_end0_position, road_end1_position, road_length_km):
        self.screen = screen
        self.name = road_name
        self.end0_position = road_end0_position
        self.end1_position = road_end1_position
        self.length_km = road_length_km
        self.middle_position = ((self.end0_position[0] + self.end1_position[0]) // 2, (self.end0_position[1] + self.end1_position[1]) // 2)
        self.closed = False
        self.closed_timer = 0

    def draw_road(self):
        # draw road
        if self.closed:
            pygame.draw.line(self.screen, COLOR_ROAD_CLOSED, self.end0_position, self.end1_position, ROAD_THICKNESS)
        else:
            pygame.draw.line(self.screen, COLOR_ROAD, self.end0_position, self.end1_position, ROAD_THICKNESS)
        # draw title
        middle_position_x, middle_position_y = self.middle_position
        str_road_title = str(self.name)
        img_road_title = FONT_BIG.render(str_road_title, True, COLOR_FONT_WHITE)
        self.screen.blit(img_road_title, (middle_position_x + 10, middle_position_y + 10))
    
    def close_road(self):
        trigger = random.uniform(0, 1)
        if trigger > 0.9999:
            self.closed = True
            self.closed_timer = random.uniform(180, 4320)
            print(str(self.name) + ' closed for ' + str(int(self.closed_timer)) + ' min')
        
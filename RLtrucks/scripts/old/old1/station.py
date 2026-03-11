# %%
"""
Created on June 5 10:11 2023
@author: Johan Andreas Stendal
"""
import math

import pygame

from config import *
from utilities import *

class Station:
    def __init__(self, screen, station_name):
        self.screen = screen
        self.name = station_name
        self.position_x = stations_stats[self.name]['position_x']
        self.position_y = stations_stats[self.name]['position_y']
        self.position = (self.position_x, self.position_y)
        self.station_capacity = stations_stats[self.name]['station_capacity']
        self.color = stations_stats[self.name]['color']
        self.size_x = stations_stats[self.name]['size_x']
        self.size_y = stations_stats[self.name]['size_y']
        self.packages_at_station = []

    def get_available_roads(self, roads):
        available_roads = []
        for road in roads:
            if road.end0_position == self.position or road.end1_position == self.position:
                available_roads.append(road)

        return available_roads

    def draw_station(self):
        # draw station
        position_upperleftcorner_x = self.position_x - self.size_x / 2
        position_upperleftcorner_y = self.position_y - self.size_y / 2
        pygame.draw.rect(self.screen, self.color, (position_upperleftcorner_x, position_upperleftcorner_y, self.size_x, self.size_y))
        # draw title
        str_station_title = str(self.name)
        img_station_title = FONT_BIG.render(str_station_title, True, COLOR_FONT_BLACK)
        if self.position_y > SCREEN_HEIGHT * 0.5:
            self.screen.blit(img_station_title, (self.position_x - 30, self.position_y + self.size_y / 2 + 10))
        else:
            self.screen.blit(img_station_title, (self.position_x - 30, self.position_y - self.size_y / 2 - 30))

    def draw_n_packages(self):
        # draw number of packages
        str_n_packages = str(len(self.packages_at_station))
        img_n_packages = FONT_BIG.render(str_n_packages, True, COLOR_FONT_BLACK)
        self.screen.blit(img_n_packages, (self.position_x + self.size_x / 2 + 5, self.position_y - 20))

    def print_packages_at_station(self):
        if self.packages_at_station:
            print('packages at ' + self.name + ': ' + str(len(self.packages_at_station)))

# %%

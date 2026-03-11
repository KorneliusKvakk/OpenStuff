# %%
"""
Created on June 5 10:11 2023
@author: Johan Andreas Stendal
"""
import math

import pygame

from config import *
from utilities import *

class Truck:
    def __init__(self, screen, truck_name, truck_postion):
        self.screen = screen
        self.name = truck_name
        self.capacity_kg = trucks_stats[self.name]['truck_capacity_kg']
        self.capacity_kg_0 = self.capacity_kg
        self.velocity_kmpm = trucks_stats[self.name]['truck_velocity_kmpm']
        self.velocity_kmpm_0 = self.velocity_kmpm
        self.fuel_consumption_lpkm = trucks_stats[self.name]['truck_fuel_consumption_lpkm']
        self.fuel_consumption_lpkm_0 = self.fuel_consumption_lpkm
        self.position = truck_postion
        self.color = trucks_stats[self.name]['color']
        self.size_x = trucks_stats[self.name]['size_x']
        self.size_y = trucks_stats[self.name]['size_y']
        self.loaded_packages = []
        self.ready_to_go = False
        self.driving = False
        self.driving_time_min = 0
        self.driving_time_min_0 = 0
        self.roadtrip_start_position = (0, 0)
        self.roadtrip_end_position = (0, 0)
        self.last_road_driven = []
        self.available_depots = ['Depot00', 'Depot01', 'Depot02', 'Depot03', 'Depot04', 'Depot05']
        # self.milk_route_counter = 0
        # if self.name == 'Truck00':
        #     self.available_depots = ['Depot03', 'Depot05', 'Depot04', 'Depot02', 'Depot01', 'Depot00']
        #     self.milk_route = ['Road09', 'Road01', 'Road02', 'Road03', 'Road04', 'Road05', 'Road06', 'Road07', 'Road08', 'Road00', 'Road09']
        #     self.milk_route_length = len(self.milk_route)
        # elif self.name == 'Truck01':
        #     self.available_depots = ['Depot00', 'Depot01', 'Depot02']
        #     self.milk_route = ['Road09', 'Road00', 'Road08', 'Road07', 'Road06', 'Road11']
        #     self.milk_route_length = len(self.milk_route)

    def start_moving_truck(self, road_to_go):
        # get roadtrip start and end points from road_to_go
        if self.position == road_to_go.end0_position:
            self.roadtrip_start_position = road_to_go.end0_position
            self.roadtrip_end_position = road_to_go.end1_position
            self.driving = True
        elif self.position == road_to_go.end1_position:
            self.roadtrip_start_position = road_to_go.end1_position
            self.roadtrip_end_position = road_to_go.end0_position
            self.driving = True
        else:
            print(self.name + ' could not find road end')
        if self.driving:
            self.driving_time_min = road_to_go.length_km / self.velocity_kmpm
            self.driving_time_min_0 = self.driving_time_min
            self.ready_to_go = False
            # print(self.name + ' started')
        self.last_road_driven.append(road_to_go)

    def calculate_fuel_consumption(self):
        self.fuel_consumption_lpkm = self.fuel_consumption_lpkm_0 + self.fuel_consumption_lpkm_0 * 0.0005 * (self.capacity_kg_0 - self.capacity_kg)

    def calculate_velocity(self):
        self.velocity_kmpm = self.velocity_kmpm_0 - self.velocity_kmpm_0 * 0.0002 * (self.capacity_kg_0 - self.capacity_kg)

    def move_truck_while_driving(self):
        driving_time_fraction = 1 - (self.driving_time_min / self.driving_time_min_0)
        self.position = lerp(self.roadtrip_start_position, self.roadtrip_end_position, driving_time_fraction)

    def stop_moving_truck(self):
        self.position = self.roadtrip_end_position
        self.driving = False
        # print(self.name + ' stopped')

    def draw_truck(self):
        # draw truck
        position_x, position_y = self.position
        position_upperleftcorner_x = position_x - self.size_x / 2
        position_upperleftcorner_y = position_y - self.size_y / 2
        pygame.draw.rect(self.screen, self.color, (position_upperleftcorner_x, position_upperleftcorner_y, self.size_x, self.size_y))
        # draw cabin
        cabin_position_upperleftcorner_x = position_upperleftcorner_x - self.size_y / 2 + 1
        cabin_position_upperleftcorner_y = position_upperleftcorner_y + self.size_y / 3
        pygame.draw.rect(self.screen, COLOR_TRUCK_CABIN, (cabin_position_upperleftcorner_x, cabin_position_upperleftcorner_y, self.size_y / 2, self.size_y * 2 / 3))
        # draw loaded packages
        loaded_size_x = 0.8 * self.size_x
        loaded_size_y_0 = 0.8 * self.size_y
        capacity_fraction = self.capacity_kg / self.capacity_kg_0
        loaded_fraction = 1 - capacity_fraction
        loaded_position_upperleftcorner_x = position_upperleftcorner_x + 0.1 * self.size_x
        loaded_position_upperleftcorner_y = position_upperleftcorner_y + 0.9 * self.size_y - loaded_fraction * loaded_size_y_0
        loaded_size_y = loaded_fraction * loaded_size_y_0
        pygame.draw.rect(self.screen, COLOR_TRUCK_LOADED, (loaded_position_upperleftcorner_x, loaded_position_upperleftcorner_y, loaded_size_x, loaded_size_y))
        # # draw title
        # str_truck_title = str(self.name)
        # img_truck_title = FONT_SMALL.render(str_truck_title, True, COLOR_FONT_WHITE)
        # self.screen.blit(img_truck_title, (position_upperleftcorner_x, position_upperleftcorner_y - 20))

# %%

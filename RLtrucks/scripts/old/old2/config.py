# %%
"""
Created on June 5 10:11 2023
@author: Johan Andreas Stendal
"""
import pygame
pygame.init()

# Initial episode length, episode number, timestep number and reward
EPISODE_LENGTH = 1000 # in number of stops
update_action = False

# constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 10000

SIZE_HUB_X = 40
SIZE_HUB_Y = 30
SIZE_DEPOT_X = 35
SIZE_DEPOT_Y = 25
ROAD_THICKNESS = 5

# colors
COLOR_BACKGROUND = (0, 26, 51)
COLOR_FONT_BLACK = (0, 0, 0)
COLOR_FONT_WHITE = (255, 255, 255)
COLOR_FONT_RED = (204, 0, 0)
COLOR_FONT_BLUE = (0, 0, 204)
COLOR_HUB = (179, 0, 0)
COLOR_DEPOT = (0, 119, 230)
COLOR_JUNCTION = (153, 153, 153)
COLOR_TRUCK = (128, 128, 128)
COLOR_TRUCK_BIG = (77, 77, 77)
COLOR_TRUCK_CABIN = (0, 102, 255)
COLOR_TRUCK_LOADED = (255, 0, 102)
COLOR_ROAD = (153, 153, 153)
COLOR_ROAD_CLOSED = (255, 0, 0)

# fonts
FONT_SIZE_SMALL = 10
FONT_SIZE_BIG = 14
FONT_SMALL = pygame.font.Font('freesansbold.ttf', FONT_SIZE_SMALL)
FONT_BIG = pygame.font.Font('freesansbold.ttf', FONT_SIZE_BIG)

# variables

# trucks stats dictionary
trucks_stats = {
    'Truck00': {
        'truck_capacity_kg': 1500,
        'truck_velocity_kmpm': 25 / 60,
        'truck_fuel_consumption_lpkm': 0.2,
        'color': COLOR_TRUCK,
        'size_x': 40,
        'size_y': 20
    },

    'Truck01': {
        'truck_capacity_kg': 800,
        'truck_velocity_kmpm': 35 / 60,
        'truck_fuel_consumption_lpkm': 0.2,
        'color': COLOR_TRUCK,
        'size_x': 40,
        'size_y': 20
    },

    'Truck02': {
        'truck_capacity_kg': 10000,
        'truck_velocity_kmpm': 10 / 60,
        'truck_fuel_consumption_lpkm': 0.2,
        'color': COLOR_TRUCK_BIG,
        'size_x': 50,
        'size_y': 25
    },
}

# stations stats dictionary
stations_stats = {
    'Hub00': {
        'position_x': int(SCREEN_WIDTH * 0.50),
        'position_y': int(SCREEN_HEIGHT * 0.50),
        'station_capacity': 5,
        'color': COLOR_HUB,
        'size_x': SIZE_HUB_X,
        'size_y': SIZE_HUB_Y
    },

    'Depot00': {
        'position_x': int(SCREEN_WIDTH * 0.14),
        'position_y': int(SCREEN_HEIGHT * 0.13),
        'station_capacity': 1,
        'color': COLOR_DEPOT,
        'size_x': SIZE_DEPOT_X,
        'size_y': SIZE_DEPOT_Y
    },

    'Depot01': {
        'position_x': int(SCREEN_WIDTH * 0.19),
        'position_y': int(SCREEN_HEIGHT * 0.51),
        'station_capacity': 2,
        'color': COLOR_DEPOT,
        'size_x': SIZE_DEPOT_X,
        'size_y': SIZE_DEPOT_Y
    },

    'Depot02': {
        'position_x': int(SCREEN_WIDTH * 0.10),
        'position_y': int(SCREEN_HEIGHT * 0.90),
        'station_capacity': 1,
        'color': COLOR_DEPOT,
        'size_x': SIZE_DEPOT_X,
        'size_y': SIZE_DEPOT_Y
    },

    'Depot03': {
        'position_x': int(SCREEN_WIDTH * 0.60),
        'position_y': int(SCREEN_HEIGHT * 0.30),
        'station_capacity': 1,
        'color': COLOR_DEPOT,
        'size_x': SIZE_DEPOT_X,
        'size_y': SIZE_DEPOT_Y
    },

    'Depot04': {
        'position_x': int(SCREEN_WIDTH * 0.70),
        'position_y': int(SCREEN_HEIGHT * 0.80),
        'station_capacity': 1,
        'color': COLOR_DEPOT,
        'size_x': SIZE_DEPOT_X,
        'size_y': SIZE_DEPOT_Y
    },

    'Depot05': {
        'position_x': int(SCREEN_WIDTH * 0.88),
        'position_y': int(SCREEN_HEIGHT * 0.11),
        'station_capacity': 1,
        'color': COLOR_DEPOT,
        'size_x': SIZE_DEPOT_X,
        'size_y': SIZE_DEPOT_Y
    },

    'Junction00': {
        'position_x': int(SCREEN_WIDTH * 0.45),
        'position_y': int(SCREEN_HEIGHT * 0.33),
        'station_capacity': 5,
        'color': COLOR_JUNCTION,
        'size_x': 10,
        'size_y': 10
    },

    'Junction01': {
        'position_x': int(SCREEN_WIDTH * 0.65),
        'position_y': int(SCREEN_HEIGHT * 0.49),
        'station_capacity': 5,
        'color': COLOR_JUNCTION,
        'size_x': 10,
        'size_y': 10
    },

    'Junction02': {
        'position_x': int(SCREEN_WIDTH * 0.51),
        'position_y': int(SCREEN_HEIGHT * 0.79),
        'station_capacity': 5,
        'color': COLOR_JUNCTION,
        'size_x': 10,
        'size_y': 10
    },
}


# %%

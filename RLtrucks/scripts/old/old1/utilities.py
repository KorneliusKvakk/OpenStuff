# %%
"""
Created on June 5 10:11 2023
@author: Johan Andreas Stendal
"""
import math
import os
import numpy as np

import pygame

from config import *

def generate_neighbor_matrix(sim):
    neighbour_matrix = [[[] for _ in range(len(sim.stations))] for _ in range(len(sim.stations))]

    for road in sim.roads:
        for start_station in sim.stations:
            if start_station.position == road.end0_position:
                start_index = sim.stations.index(start_station)
                break
        for end_station in sim.stations:
            if end_station.position == road.end1_position:
                end_index = sim.stations.index(end_station)
                break
        neighbour_matrix[start_index][end_index].append(road.length_km)
        neighbour_matrix[end_index][start_index].append(road.length_km)

    return neighbour_matrix

def get_route(sim, neighbour_matrix, start_station, end_station):
    pass

def get_station_position(stations, station_name):
    station_position = next((station.position for station in stations if station.name == station_name), None)

    return station_position

def find_closest_position(position, targets):
    position_x, position_y = position
    closest_position = min(targets, key=lambda coord: math.sqrt((coord[0] - position_x) ** 2 + (coord[1] - position_y) ** 2))

    return closest_position

def lerp(start_position, end_position, time_fraction):
    x = start_position[0] + (end_position[0] - start_position[0]) * time_fraction
    y = start_position[1] + (end_position[1] - start_position[1]) * time_fraction
    
    return (x, y)

def get_road_angle_deg(start_position, end_position):
    start_position_x, start_position_y = start_position
    end_position_x, end_position_y = end_position
    road_angle_rad = math.atan2(end_position_y - start_position_y, end_position_x - start_position_x)
    road_angle_deg = math.degrees(road_angle_rad)
    road_angle_deg = road_angle_deg % 360
    if road_angle_deg < 0:
        road_angle_deg += 360

    return road_angle_deg

def find_closest_road_angle_deg(roads_angle_deg, action_deg):
    roads_angle_deg = [angle % 360 for angle in roads_angle_deg]
    action_deg %= 360
    angular_distances = [min(abs(action_deg - angle), 360 - abs(action_deg - angle)) for angle in roads_angle_deg]
    closest_index = angular_distances.index(min(angular_distances))
    closest_angle = roads_angle_deg[closest_index]

    return closest_angle, closest_index

import math

def calculate_resultant_vector(vectors):
    resultant_x = 0.0
    resultant_y = 0.0
    for vector in vectors:
        x, y = vector
        resultant_x += x
        resultant_y += y
    resultant_vector = (resultant_x, resultant_y)
    resultant_magnitude = math.sqrt(resultant_x**2 + resultant_y**2)
    resultant_angle_radians = math.atan2(resultant_y, resultant_x)
    resultant_angle_deg = math.degrees(resultant_angle_radians)
    resultant_angle_deg = resultant_angle_deg % 360
    if resultant_angle_deg < 0:
        resultant_angle_deg += 360

    return resultant_vector, resultant_magnitude, resultant_angle_deg

# Get output directory
def getDir(i):
    path = os.path.join(
        os.pardir,       # adaptal
        'ML',           # Opt
        'mlrun_%05d'%i, # Current opt directory
        'model_outputs'  # folder for model outputs csvs
    )
    return path

# Create output directory
def createDir():
    CONTINUE  = False
    CONT_INDEX = 0000
    """ Create new dir or cont. opt. run """
    if CONTINUE:
        dir_index = CONT_INDEX
    else:
        dir_index = 0
        while os.path.exists(getDir(dir_index)):
            dir_index += 1
        
    newdir = getDir(dir_index)
    os.makedirs(newdir,exist_ok=True)
    os.chdir(newdir)

# Create new directory
def newDir(n_episode):
    newdir = '%05d'%n_episode
    os.makedirs(newdir)
    os.chdir(newdir)

# Convert seconds to hours:minutes:seconds
def formatSeconds(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%dhr:%02dmin:%02dsec" % (hour, min, sec)

# %%

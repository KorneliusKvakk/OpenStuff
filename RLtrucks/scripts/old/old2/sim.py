# %%
"""
Created on June 5 10:11 2023
@author: Johan Andreas Stendal
"""
import math
import numpy as np
import itertools
import random
import pandas as pd

import pygame

from config import *
from utilities import *
from station import *
from hub import *
from depot import *
from truck import *

class Sim:
    def __init__(self, draw_env):
        # pygame
        self.draw_env = draw_env

        if self.draw_env:
            pygame.init()
            self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        else:
            self.screen = object()

        # initialize simulation time step counter
        self.timestep_sim = 0

        # initialize hub
        self.hubs = []
        self.hubs.append(Hub(self.screen, 'Hub00'))
        
        # initialize depots
        self.depots = []
        self.depots.append(Depot(self.screen, 'Depot00'))
        self.depots.append(Depot(self.screen, 'Depot01'))
        self.depots.append(Depot(self.screen, 'Depot02'))
        self.depots.append(Depot(self.screen, 'Depot03'))
        self.depots.append(Depot(self.screen, 'Depot04'))
        self.depots.append(Depot(self.screen, 'Depot05'))

        # initialize juntions
        self.juntions = []
        self.juntions.append(Station(self.screen, 'Junction00'))
        self.juntions.append(Station(self.screen, 'Junction01'))
        self.juntions.append(Station(self.screen, 'Junction02'))

        # initialize list of all stations
        self.stations = self.hubs + self.depots + self.juntions

        # initialize list of all station positions
        self.stations_position = []
        for station in self.stations:
            self.stations_position.append((station.position_x, station.position_y))

        # initialize roads (road length given in km)
        self.roads = []
        self.roads.append(Road(self.screen, 'Road00', get_station_position(self.stations, 'Depot00'),    get_station_position(self.stations, 'Junction00'), 4.5))
        self.roads.append(Road(self.screen, 'Road01', get_station_position(self.stations, 'Junction00'), get_station_position(self.stations, 'Depot03'),    4.0))
        self.roads.append(Road(self.screen, 'Road02', get_station_position(self.stations, 'Depot03'),    get_station_position(self.stations, 'Depot05'),    5.0))
        self.roads.append(Road(self.screen, 'Road03', get_station_position(self.stations, 'Depot05'),    get_station_position(self.stations, 'Junction01'), 7.5))
        self.roads.append(Road(self.screen, 'Road04', get_station_position(self.stations, 'Junction01'), get_station_position(self.stations, 'Depot04'),    4.0))
        self.roads.append(Road(self.screen, 'Road05', get_station_position(self.stations, 'Depot04'),    get_station_position(self.stations, 'Junction02'), 4.0))
        self.roads.append(Road(self.screen, 'Road06', get_station_position(self.stations, 'Junction02'), get_station_position(self.stations, 'Depot02'),    6.0))
        self.roads.append(Road(self.screen, 'Road07', get_station_position(self.stations, 'Depot02'),    get_station_position(self.stations, 'Depot01'),    6.0))
        self.roads.append(Road(self.screen, 'Road08', get_station_position(self.stations, 'Depot01'),    get_station_position(self.stations, 'Depot00'),    6.4))
        self.roads.append(Road(self.screen, 'Road09', get_station_position(self.stations, 'Hub00'),      get_station_position(self.stations, 'Junction00'), 4.0))
        self.roads.append(Road(self.screen, 'Road10', get_station_position(self.stations, 'Hub00'),      get_station_position(self.stations, 'Depot01'),    6.4))
        self.roads.append(Road(self.screen, 'Road11', get_station_position(self.stations, 'Hub00'),      get_station_position(self.stations, 'Junction02'), 6.4))
        self.roads.append(Road(self.screen, 'Road12', get_station_position(self.stations, 'Hub00'),      get_station_position(self.stations, 'Junction01'), 6.4))
        
        # initialize trucks list
        self.trucks = []
        self.trucks.append(Truck(self.screen, 'Truck00', get_station_position(self.stations, 'Hub00')))
        # self.trucks.append(Truck(self.screen, 'Truck01', get_station_position(self.stations, 'Hub00')))
        # self.trucks.append(Truck(self.screen, 'Truck02', get_station_position(self.stations, 'Hub00')))

        # initialize metrics
        self.truck00_roads_driven = []
        self.truck00_km_driven = []
        self.truck00_total_min = []
        self.truck00_road_min = []
        self.truck00_fuel_consumption = []
        self.truck00_n_packages = []
        self.truck00_n_packages_delivered = 0
        
    def run_sim(self, action_deg):
        global update_action

        # handle inputs
        if self.draw_env:
            for event in pygame.event.get():
                # quit sim
                if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    running = False

        # move trucks if at hubs
        for hub in self.hubs:
            for truck in self.trucks:
                if truck.position == hub.position:
                    if truck.ready_to_go:
                        available_roads = hub.get_available_roads(self.roads)
                        roads_angle_deg = []
                        for road in available_roads:
                            if truck.position == road.end0_position:
                                roads_angle_deg.append(get_road_angle_deg(road.end0_position, road.end1_position))
                            elif truck.position == road.end1_position:
                                roads_angle_deg.append(get_road_angle_deg(road.end1_position, road.end0_position))
                        closest_road_angle_deg, closest_road_angle_idx = find_closest_road_angle_deg(roads_angle_deg, action_deg)
                        road_to_go = available_roads[closest_road_angle_idx]
                        truck.start_moving_truck(road_to_go)
                        truck.ready_to_go = False
                        truck.calculate_fuel_consumption()
                        if truck.name == 'Truck00':
                            self.truck00_roads_driven.append(road_to_go.name)
                            self.truck00_km_driven.append(road_to_go.length_km)
                            self.truck00_fuel_consumption.append(truck.fuel_consumption_lpkm)
                            self.truck00_n_packages.append(len(truck.loaded_packages))

        # load trucks if there are packages and trucks at hubs
        for hub in self.hubs:
            for truck in self.trucks:
                if truck.position == hub.position:
                    if not truck.driving:
                        if not truck.ready_to_go:
                            if self.timestep_sim % 3 == 0:
                                package_destination_name = random.choice(truck.available_depots)
                                package_weight_kg = random.uniform(1, 100)
                                if truck.capacity_kg < package_weight_kg:
                                    truck.ready_to_go = True
                                    break
                                else:
                                    hub.generate_package(package_destination_name, package_weight_kg)
                                    package_to_load = hub.packages_at_station[0]
                                    hub.load_truck(truck, package_to_load)

        # move trucks if at depot and no packages left with matching destination
        for depot in self.depots:
            for truck in self.trucks:
                if truck.position == depot.position:
                    if not truck.driving:
                        if truck.ready_to_go:
                            available_roads = depot.get_available_roads(self.roads)
                            roads_angle_deg = []
                            for road in available_roads:
                                if truck.position == road.end0_position:
                                    roads_angle_deg.append(get_road_angle_deg(road.end0_position, road.end1_position))
                                elif truck.position == road.end1_position:
                                    roads_angle_deg.append(get_road_angle_deg(road.end1_position, road.end0_position))
                            closest_road_angle_deg, closest_road_angle_idx = find_closest_road_angle_deg(roads_angle_deg, action_deg)
                            road_to_go = available_roads[closest_road_angle_idx]
                            truck.start_moving_truck(road_to_go)
                            truck.ready_to_go = False
                            truck.calculate_fuel_consumption()
                            if truck.name == 'Truck00':
                                self.truck00_roads_driven.append(road_to_go.name)
                                self.truck00_km_driven.append(road_to_go.length_km)
                                self.truck00_fuel_consumption.append(truck.fuel_consumption_lpkm)
                                self.truck00_n_packages.append(len(truck.loaded_packages))

        # off-load trucks that are at depots
        for depot in self.depots:
            for truck in self.trucks:
                if truck.position == depot.position:
                    if not truck.driving:
                        if not truck.ready_to_go:
                            loaded_packages_destination_name = []
                            for loaded_package in truck.loaded_packages:
                                loaded_packages_destination_name.append(loaded_package.destination_name)
                            if depot.name not in loaded_packages_destination_name:
                                truck.ready_to_go = True
                            else:
                                off_load_time = depot.get_off_load_time(truck)
                                if self.timestep_sim % off_load_time == 0:
                                    depot.off_load_truck(truck)
                                    self.truck00_n_packages_delivered += 1

        # move trucks that are at junctions
        for junction in self.juntions:
            for truck in self.trucks:
                if truck.position == junction.position:
                    if not truck.driving:
                        if truck.ready_to_go:
                            available_roads = junction.get_available_roads(self.roads)
                            roads_angle_deg = []
                            for road in available_roads:
                                if truck.position == road.end0_position:
                                    roads_angle_deg.append(get_road_angle_deg(road.end0_position, road.end1_position))
                                elif truck.position == road.end1_position:
                                    roads_angle_deg.append(get_road_angle_deg(road.end1_position, road.end0_position))
                            closest_road_angle_deg, closest_road_angle_idx = find_closest_road_angle_deg(roads_angle_deg, action_deg)
                            road_to_go = available_roads[closest_road_angle_idx]
                            truck.start_moving_truck(road_to_go)
                            truck.ready_to_go = False
                            truck.calculate_fuel_consumption()
                            if truck.name == 'Truck00':
                                self.truck00_roads_driven.append(road_to_go.name)
                                self.truck00_km_driven.append(road_to_go.length_km)
                                self.truck00_fuel_consumption.append(truck.fuel_consumption_lpkm)
                                self.truck00_n_packages.append(len(truck.loaded_packages))

        # check if trucks are at juntions
        for junction in self.juntions:
            for truck in self.trucks:
                if truck.position == junction.position:
                    if not truck.driving:
                        truck.ready_to_go = True
                        
        # count down one driving time tick per time step for all driving trucks
        for truck in self.trucks:
            if truck.driving:
                truck.move_truck_while_driving()
                truck.driving_time_min -= 1
                # stop trucks with 0 driving time
                if truck.driving_time_min <= 0:
                    truck.stop_moving_truck()
                    if truck.name == 'Truck00':
                        self.truck00_total_min.append(self.timestep_sim)
                        if len(self.truck00_total_min) > 1:
                            self.truck00_road_min.append(self.truck00_total_min[-1] - self.truck00_total_min[-2])
                        else:
                            self.truck00_road_min.append(self.truck00_total_min[-1])
        if self.draw_env:
            # draw background
            self.screen.fill(COLOR_BACKGROUND)

            # draw roads
            for road in self.roads:
                road.draw_road()
            # for closed_road in self.closed_roads:
            #     closed_road.draw_road()

            # draw stations
            for station in self.stations:
                station.draw_station()
            
            # draw number of packages at hubs and depots
            for hub in self.hubs:
                hub.draw_n_packages()
            for depot in self.depots:
                depot.draw_n_packages()

            # draw trucks
            for truck in self.trucks:
                truck.draw_truck()

            # draw timestep text
            str_timestep = 'Time: ' + str(self.timestep_sim) + ' min'
            img_timestep = FONT_BIG.render(str_timestep, True, COLOR_FONT_WHITE)
            self.screen.blit(img_timestep, (int(SCREEN_WIDTH * 0.85), int(SCREEN_HEIGHT * 0.95)))

        self.timestep_sim += 1

        # get observations
        obs = []
        if update_action:
            for truck in self.trucks:
                # get truck capacity
                truck_capacity_kg = truck.capacity_kg
                # get integer corresponding to truck position at station
                for idx_station, station in enumerate(self.stations):
                    if station.position == truck.position:
                        truck_position_int = idx_station
                        break
                # get number of packages for each depot
                depots_vector = []
                for depot in self.depots:
                    n_packages_for_depot = 0
                    for package in truck.loaded_packages:
                        if package.destination_name == depot.name:
                            n_packages_for_depot += 1
                    delta_x = n_packages_for_depot * (depot.position_x - self.hubs[0].position_x)
                    delta_y = n_packages_for_depot * (depot.position_y - self.hubs[0].position_y)
                    depot_vector = (delta_x, delta_y)
                    depots_vector.append(depot_vector)
                
                _depots_resultant_vector, depots_resultant_magnitude, depots_resultant_angle_deg = calculate_resultant_vector(depots_vector)

            obs = [truck_position_int, truck_capacity_kg, depots_resultant_angle_deg, depots_resultant_magnitude]

        # check if any truck is moving
        update_action = False
        for truck in self.trucks:
            if truck.ready_to_go:
                update_action = True

        # reward function
        reward_packages_delivered = -1 + self.truck00_n_packages_delivered / (1 + self.timestep_sim) * 26/1
        reward_km_driven = 1 - np.sum(np.array(self.truck00_km_driven)) / (1 + self.timestep_sim) * 26/5.5
        reward_fuel_consumption = 1 - np.sum(np.array(self.truck00_fuel_consumption) * np.array(self.truck00_km_driven)) / (1 + self.timestep_sim) * 26/1.65

        reward = -1 + reward_packages_delivered * 2 + reward_km_driven + reward_fuel_consumption

        # print(reward_packages_delivered)
        # print(reward_km_driven)
        # print(reward_fuel_consumption)
        # print(reward)


        # reward_packages_delivered = self.truck00_n_packages_delivered / (1 + self.timestep_sim / 55)
        # penalty_km_driven = np.sum(np.array(self.truck00_km_driven)) / (1 + self.timestep_sim / 3)
        # penalty_fuel_consumption = np.sum(np.array(self.truck00_fuel_consumption) * np.array(self.truck00_km_driven)) / (1 + self.timestep_sim / 12)

        # reward = reward_packages_delivered - penalty_km_driven - penalty_fuel_consumption

        # timestep_sim = 1000
        # n_packages_delivered = 20
        # km_driven = 100
        # fuel_consumed = 25

        # reward_packages_delivered = n_packages_delivered / (1 + timestep_sim / 55)
        # penalty_km_driven = km_driven / (1 + timestep_sim / 3)
        # penalty_fuel_consumption = fuel_consumed / (1 + timestep_sim / 12)

        # reward = -2 + reward_packages_delivered - penalty_km_driven - penalty_fuel_consumption
        # print(reward_packages_delivered)
        # print(penalty_km_driven)
        # print(penalty_fuel_consumption)
        # print(reward)

        # timestep_sim = 26000
        # n_packages_delivered = 1000 
        # km_driven = 5500
        # fuel_consumed = 1450 

        # reward_packages_delivered = n_packages_delivered / (1 + timestep_sim / 35)
        # penalty_km_driven = km_driven / (1 + timestep_sim / 1)
        # penalty_fuel_consumption = fuel_consumed / (1 + timestep_sim / 4)

        # reward = -1 + reward_packages_delivered - penalty_km_driven - penalty_fuel_consumption
        # print(reward_packages_delivered)
        # print(penalty_km_driven)
        # print(penalty_fuel_consumption)
        # print(reward)






        # maximum possible n_packages_delivered = 3000 (guess) 
        # higest possible timestep_sim = 7.5 * 1000 / 0.291666 (lowest possible speed at max capacity) = 25715
        # longest possible km_driven = 7.5 * 1000 = 7500
        # maximum possible fuel consumed = 0.35 * 7.5 * 1000 = 2625
        # reward_packages_delivered = self.truck00_n_packages_delivered / 1500
        # penalty_km_driven = np.sum(np.array(self.truck00_km_driven)) / 7500
        # penalty_fuel_consumption = np.sum(np.array(self.truck00_fuel_consumption) * np.array(self.truck00_km_driven)) / 2700
        # print(np.sum(np.array(self.truck00_fuel_consumption) * np.array(self.truck00_km_driven)))
        # print(np.sum(np.array(self.truck00_km_driven)))

        # reward = -1 + reward_packages_delivered - penalty_km_driven - penalty_fuel_consumption

        # reward_timestep = (self.truck00_n_packages_delivered/3000) / (self.timestep_sim/26000)
        # reward_km_driven = (self.truck00_n_packages_delivered/3000) / (np.sum(np.array(self.truck00_km_driven))/7500)
        # reward_fuel_consumption = (self.truck00_n_packages_delivered/3000) / (np.sum(np.array(self.truck00_fuel_consumption) * np.array(self.truck00_km_driven))/2700)

        # reward = -1.5 + reward_timestep + reward_km_driven + reward_fuel_consumption

        # if self.timestep_sim < 500:
        #     reward = 0
        # else:
        #     reward0 = self.truck00_n_packages_delivered
        #     reward1 = -self.timestep_sim / (self.truck00_n_packages_delivered + 1)
        #     reward2 = -np.sum(self.truck00_km_driven) / (self.truck00_n_packages_delivered + 1)
        #     reward3 = -np.sum(np.array(self.truck00_fuel_consumption) * np.array(self.truck00_km_driven)) / self.truck00_n_packages_delivered
        # # reward 0 før forlater hub for første gang, slipper if else
        # # if timesteps < 20 % no reward
        #     reward = 2 - (reward0 + reward1 + reward2 + reward3)
        # # reward = self.truck00_n_packages_delivered / (self.timestep_sim / 20) - 1
        # # reward = 1.5 - (sum(self.truck00_km_driven) / n_trips / max_possible_km_driven + self.truck00_fuel_consumption / ref + self.timestep_sim / ref ) # divide arrays by number of trips/full capacity to 0

        # output sim metrics
        self.sim_metrics = [self.truck00_roads_driven, self.truck00_km_driven, self.truck00_total_min, self.truck00_road_min, self.truck00_fuel_consumption, self.truck00_n_packages]

        if self.draw_env:
            pygame.display.update()

        return update_action, obs, reward

# %%

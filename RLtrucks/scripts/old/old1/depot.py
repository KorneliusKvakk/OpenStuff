# %%
"""
Created on June 5 10:11 2023
@author: Johan Andreas Stendal
"""
import math

import pygame

from config import *
from utilities import *
from station import *

class Depot(Station):
    def off_load_truck(self, truck):
        if truck.loaded_packages:
            for package in truck.loaded_packages:
                if package.destination_name == self.name:
                    self.packages_at_station.append(package)
                    truck.loaded_packages.remove(package)
                    truck.capacity_kg += package.weight_kg
                    print('1 package off-loaded at ' + str(self.name))
                    break

    def get_off_load_time(self, truck):
        packages_for_other_depots = 0
        if truck.loaded_packages:
            for package in truck.loaded_packages:
                if package.destination_name != self.name:
                    packages_for_other_depots += 1
        off_load_time = int(2 + packages_for_other_depots / 5)

        return off_load_time


# %%

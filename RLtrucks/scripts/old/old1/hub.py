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
from station import *
from road import *
from package import *

class Hub(Station):
    def generate_package(self, package_destination_name, package_weight_kg):
        package = Package(package_destination_name, package_weight_kg)
        self.packages_at_station.append(package)

    def load_truck(self, truck, package):
        if truck.capacity_kg >= package.weight_kg:
            truck.loaded_packages.append(package)
            truck.capacity_kg -= package.weight_kg
            self.packages_at_station.remove(package)
            print('1 package loaded at ' + str(self.name))
    
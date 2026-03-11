from enum import Enum
import random
import math
import numpy as np
import pandas as pd
from opensimplex import OpenSimplex
import pygame
import matplotlib.pyplot as plt

from utils import *

SCREEN_SIZE = 1000
FPS = 6000

WORLD_SIZE = 10000.0
WORLD_BORDER = 1000.0

SCREEN_SCALE = SCREEN_SIZE / WORLD_SIZE

WIND_MAX_FORCE = 0.8
WIND_NOISE_FREQUENCY = 0.0002

MAX_AGENTS = 5
MAX_STATIONS = 5

STATION_SIZE = 200.0

AGENT_MAX_VELOCITY = 20.0
AGENT_FORCE = 1.0
AGENT_DRAGCOEFFICIENT = 0.05
AGENT_WEIGHT = 1.0
AGENT_SIZE = 50.0
AGENT_RANGE = 500.0

MAXROLL_PART_GENERATION = 600
MIN_PARTWEIGHT = 0.5
MAX_PARTWEIGHT = 5.0

EVOLUTION_INTERVAL = 10000 # in timesteps

maxNodeGenes = 50
compatibilityDistanceThreshold = 3.0
minConnectionWeight = -1.0
maxConnectionWeight = 1.0
mutationProbability = 0.3
perturbingProbability = 0.9
perturbingSigma = 0.1
perturbingRadius = 0.2
inheritDisabledGeneProbability = 0.75
c1 = 1.0 # weight of excess and disjoint genes
c2 = 0.4 # weight of average connection weight difference

class NetworkNodeType(Enum):
    INPUT = 1
    HIDDEN = 2
    OUTPUT = 3

COLOR_BACKGROUND = (26, 26, 26)
COLOR_AGENT_EMPTY = (255, 255, 255)
COLOR_AGENT_FULL = (255, 26, 26)
COLOR_AGENT_RANGE = (0, 89, 179)
COLOR_STATION = (255, 163, 26)
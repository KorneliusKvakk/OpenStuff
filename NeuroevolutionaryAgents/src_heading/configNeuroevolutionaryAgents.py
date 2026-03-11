from enum import Enum
import random
import math
import numpy as np
import pandas as pd
import opensimplex
import pygame
import matplotlib.pyplot as plt

SCREEN_SIZE = 1000
FPS = 60

opensimplex.seed(random.randint(-1000, 1000))

WORLD_SIZE = 5000

SCREEN_SCALE = SCREEN_SIZE / WORLD_SIZE

WIND_SCALE = 1.0
WIND_MAX_VELOCITY = 2.0

MAX_AGENTS = 5
MAX_STATIONS = 5

AGENT_MAX_VELOCITY = 5.0
AGENT_MAX_ANGULARVELOCITY = 2.0

AGENT_WEIGHT = 1.0

AGENT_SIZE = 25.0
AGENT_RANGE = 300.0
STATION_SIZE = 100.0

WORLD_BORDER = 1000

MAXROLL_PART_GENERATION = 1

MIN_PARTWEIGHT = 0.5
MAX_PARTWEIGHT = 5.0

maxNodeGenes = 40
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
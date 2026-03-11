from configNeuroevolutionaryAgents import *
from Genome import *
from NeuralNetwork import *

class SenseType(Enum):
    BIAS = 1 # constant bias input, constant float between -1 and 1
    OSCILLATOR = 2 # oscillator value (-1, 1)
    RANDOM_NOISE = 3 # random noise value according to simplexnoise (-1, 1)
    I1 = 4
    I2 = 5
    I3 = 6
    I4 = 7
    NAMO_YIELD_END = 8
    NAMO_TENSILE_END = 9
    EXP_YIELD_END = 10
    EXP_TENSILE_END = 11
    n_Senses = 11

class ActionType(Enum):
    YIELD_CORRECTION = 12 # move in positive y direction (0, 1)
    TENSILE_CORRECTION = 13 # move in negative y direction (0, 1)
    n_Actions = 2

class Agent(Entity):
    def __init__(self, genome : Genome, net : NeuralNetwork):
        self.genome = genome
        self.net = net
        self.fitness = 0.0
        # senses
        self.Senses = {}
        self.Actions = {}
        self.biasValue = self.genome.biasValue
        self.counterOscillator = self.genome.counterOscillator
        self.oscillatorFrequency = self.genome.oscillatorFrequency
        self.oscillatorValue = self.genome.oscillatorValue
        self.randomNoiseSeed = self.genome.randomNoiseSeed
        self.counterRandomNoise = self.genome.counterRandomNoise
        self.randomNoiseFrequency = self.genome.randomNoiseFrequency
        self.randomNoiseValue = self.genome.randomNoiseValue

    def UpdateOscillator(self):
        self.oscillatorValue = math.sin(self.oscillatorFrequency * float(self.counterOscillator))
        self.counterOscillator += 1

    def UpdateRandomNoise(self):
        self.randomNoiseValue = opensimplex.noise2(self.randomNoiseFrequency * float(self.counterRandomNoise) + self.randomNoiseSeed, 0.0)
        self.counterRandomNoise += 1

    def UpdateSenses(self):
        if self.toTarget.x > -1000.0 and self.toTarget.x < 1000.0:
            targetDistance_x = 2.0 / (1.0 + math.exp(-2.0 * (self.toTarget.x / 1000.0))) - 1.0 # sigmoiding distance
        else:
            targetDistance_x = 1.0
        if self.toTarget.y > -1000.0 and self.toTarget.y < 1000.0:
            targetDistance_y = 2.0 / (1.0 + math.exp(-2.0 * (self.toTarget.y / 1000.0))) - 1.0 # sigmoiding distance
        else:
            targetDistance_y = 1.0
        # update senses
        self.Senses[SenseType.BIAS.value] = self.biasValue
        self.Senses[SenseType.OSCILLATOR.value] = self.oscillatorValue
        self.Senses[SenseType.RANDOM_NOISE.value] = self.randomNoiseValue
        
    def ExecuteActions(self):
        self.Actions = self.net.Calculate(self.Senses)
        idxMax = max(self.Actions, key=self.Actions.get)
        
    def SetFitnessAdjustment(self, fitnessAdjustment : float):
        self.fitness += fitnessAdjustment
    def GetFitness(self):
        return self.fitness

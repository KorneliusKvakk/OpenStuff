from configNeuroevolutionaryAgents import *

from neuralNetwork import *
from genome import *
from entity import *

from part import *

class SenseType(Enum):
    BIAS = 1 # constant bias input, constant float between -1 and 1
    OSCILLATOR = 2 # oscillator value (-1, 1)
    RANDOM_NOISE = 3 # random noise value according to simplexnoise (-1, 1)
    WEIGHT = 4
    VELOCITY_X = 5
    VELOCITY_Y = 6
    DISTANCE_X_DESTINATION = 7
    DISTANCE_Y_DESTINATION = 8
    DISTANCE_X_AGENT1 = 9
    DISTANCE_Y_AGENT1 = 10
    DISTANCE_X_AGENT2 = 11
    DISTANCE_Y_AGENT2 = 12
    DISTANCE_X_AGENT3 = 13
    DISTANCE_Y_AGENT3 = 14
    DISTANCE_X_AGENT4 = 15
    DISTANCE_Y_AGENT4 = 16

n_Senses = 16

class ActionType(Enum):
    MOVE_NORTH = 17
    MOVE_SOUTH = 18
    MOVE_EAST = 19
    MOVE_WEST = 20
    # ACTIVITY = 25

n_Actions = 4

class Agent(Entity):
    def __init__(self, genome : Genome, net : NeuralNetwork, initialPosition : pygame.Vector2):
        super().__init__(initialPosition)
        self.genome = genome
        self.net = net
        self.fitness = 0.0
        self.Senses = {}
        self.Actions = {}
        self.biasValue = self.genome.biasValue
        self.noiseGenerator = OpenSimplex(seed=random.randint(-10000, 10000))
        self.counterOscillator = self.genome.counterOscillator
        self.oscillatorFrequency = self.genome.oscillatorFrequency
        self.oscillatorValue = self.genome.oscillatorValue
        self.counterRandomNoise = self.genome.counterRandomNoise
        self.randomNoiseFrequency = self.genome.randomNoiseFrequency
        self.randomNoiseValue = self.genome.randomNoiseValue
        self.destinationStationPosition = pygame.Vector2(0.0, 0.0)
        self.previousToDestination = pygame.Vector2(0.0, 0.0)
        self.toDestination = pygame.Vector2(0.0, 0.0)
        self.toAgent1 = pygame.Vector2(0.0, 0.0)
        self.toAgent2 = pygame.Vector2(0.0, 0.0)
        self.toAgent3 = pygame.Vector2(0.0, 0.0)
        self.toAgent4 = pygame.Vector2(0.0, 0.0)
        self.Parts = []

    def InsertPart(self, part : Part):
        self.Parts.append(part)

    def DeliverPart(self):
        self.Parts.clear()

    def UpdateOscillator(self):
        self.oscillatorValue = math.sin(self.oscillatorFrequency * float(self.counterOscillator))
        self.counterOscillator += 1

    def UpdateRandomNoise(self):
        self.randomNoiseValue = self.noiseGenerator.noise2(self.randomNoiseFrequency * float(self.counterRandomNoise), 0.0)
        self.counterRandomNoise += 1

    def UpdateToDestination(self):
        self.toDestination = self.destinationStationPosition - self.position
        if self.toDestination.length() < self.previousToDestination.length():
            self.fitness += 1.0
        self.previousToDestination = self.toDestination

    def UpdateToAgents(self,
        Agent1 : pygame.Vector2,
        Agent2 : pygame.Vector2,
        Agent3 : pygame.Vector2,
        Agent4 : pygame.Vector2):

        self.toAgent1 = Agent1 - self.position
        self.toAgent2 = Agent2 - self.position
        self.toAgent3 = Agent3 - self.position
        self.toAgent4 = Agent4 - self.position

    def SigmoidDistance(self, toTarget : pygame.Vector2) -> pygame.Vector2:
        targetDistance = pygame.Vector2(0.0, 0.0)
        targetDistance.x = 2.0 / (1.0 + math.exp(-2.0 * (toTarget.x / WORLD_SIZE))) - 1.0 # sigmoiding distance
        targetDistance.y = 2.0 / (1.0 + math.exp(-2.0 * (toTarget.y / WORLD_SIZE))) - 1.0 # sigmoiding distance

        # if toTarget.x > -WORLD_SIZE and toTarget.x < WORLD_SIZE:
        #     targetDistance.x = 2.0 / (1.0 + math.exp(-2.0 * (toTarget.x / WORLD_SIZE))) - 1.0 # sigmoiding distance
        # else:
        #     targetDistance.x = 1.0
        # if toTarget.y > -WORLD_SIZE and toTarget.y < WORLD_SIZE:
        #     targetDistance.y = 2.0 / (1.0 + math.exp(-2.0 * (toTarget.y / WORLD_SIZE))) - 1.0 # sigmoiding distance
        # else:
        #     targetDistance.y = 1.0

        return targetDistance

    def UpdateSenses(self):
        destinationDistance = self.SigmoidDistance(self.toDestination)
        agent1Distance = self.SigmoidDistance(self.toAgent1)
        agent2Distance = self.SigmoidDistance(self.toAgent2)
        agent3Distance = self.SigmoidDistance(self.toAgent3)
        agent4Distance = self.SigmoidDistance(self.toAgent4)

        self.Senses[SenseType.BIAS.value] = self.biasValue
        self.Senses[SenseType.OSCILLATOR.value] = self.oscillatorValue
        self.Senses[SenseType.RANDOM_NOISE.value] = self.randomNoiseValue
        self.Senses[SenseType.WEIGHT.value] = self.weight / (AGENT_WEIGHT + MAX_PARTWEIGHT)
        self.Senses[SenseType.VELOCITY_X.value] = self.velocity.x / AGENT_MAX_VELOCITY
        self.Senses[SenseType.VELOCITY_Y.value] = self.velocity.y / AGENT_MAX_VELOCITY
        self.Senses[SenseType.DISTANCE_X_DESTINATION.value] = destinationDistance.x
        self.Senses[SenseType.DISTANCE_Y_DESTINATION.value] = destinationDistance.y
        self.Senses[SenseType.DISTANCE_X_AGENT1.value] = agent1Distance.x
        self.Senses[SenseType.DISTANCE_Y_AGENT1.value] = agent1Distance.y
        self.Senses[SenseType.DISTANCE_X_AGENT2.value] = agent2Distance.x
        self.Senses[SenseType.DISTANCE_Y_AGENT2.value] = agent2Distance.y
        self.Senses[SenseType.DISTANCE_X_AGENT3.value] = agent3Distance.x
        self.Senses[SenseType.DISTANCE_Y_AGENT3.value] = agent3Distance.y
        self.Senses[SenseType.DISTANCE_X_AGENT4.value] = agent4Distance.x
        self.Senses[SenseType.DISTANCE_Y_AGENT4.value] = agent4Distance.y

    def ExecuteActions(self):
        self.Actions = self.net.Calculate(self.Senses)
        moveActionMax = max(self.Actions, key=self.Actions.get)
        powerVector = pygame.Vector2(0.0, 0.0)
        if moveActionMax == ActionType.MOVE_NORTH.value:
            powerVector = pygame.Vector2(0.0, -1.0)
        if moveActionMax == ActionType.MOVE_SOUTH.value:
            powerVector = pygame.Vector2(0.0, 1.0)
        if moveActionMax == ActionType.MOVE_EAST.value:
            powerVector = pygame.Vector2(1.0, 0.0)
        if moveActionMax == ActionType.MOVE_WEST.value:
            powerVector = pygame.Vector2(-1.0, 0.0)
        pygame.Vector2.scale_to_length(powerVector, AGENT_FORCE)
        self.velocity = self.velocity + powerVector
        
    def SetFitnessAdjustment(self, fitnessAdjustment : float):
        self.fitness += fitnessAdjustment

    def GetFitness(self):
        return self.fitness
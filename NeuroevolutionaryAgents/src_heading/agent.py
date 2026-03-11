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
    ANGULARVELOCITY_CW = 7
    ANGULARVELOCITY_CCW = 8
    # HEADING_DIFF_DESTINATION = 9
    DISTANCE_X_DESTINATION = 9
    DISTANCE_Y_DESTINATION = 10
    DISTANCE_X_AGENT1 = 11
    DISTANCE_Y_AGENT1 = 12
    DISTANCE_X_AGENT2 = 13
    DISTANCE_Y_AGENT2 = 14
    DISTANCE_X_AGENT3 = 15
    DISTANCE_Y_AGENT3 = 16
    DISTANCE_X_AGENT4 = 17
    DISTANCE_Y_AGENT4 = 18

n_Senses = 18

class ActionType(Enum):
    MOVE_NORTH = 19
    MOVE_SOUTH = 20
    MOVE_EAST = 21
    MOVE_WEST = 22
    # ROTATE_CW = 23
    # ROTATE_CCW = 24
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
        self.counterOscillator = self.genome.counterOscillator
        self.oscillatorFrequency = self.genome.oscillatorFrequency
        self.oscillatorValue = self.genome.oscillatorValue
        self.randomNoiseSeed = self.genome.randomNoiseSeed
        self.counterRandomNoise = self.genome.counterRandomNoise
        self.randomNoiseFrequency = self.genome.randomNoiseFrequency
        self.randomNoiseValue = self.genome.randomNoiseValue
        self.destinationStationPosition = pygame.Vector2(0.0, 0.0)
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
        self.randomNoiseValue = opensimplex.noise2(self.randomNoiseFrequency * float(self.counterRandomNoise) + self.randomNoiseSeed, 0.0)
        self.counterRandomNoise += 1

    def UpdateToDestination(self):
        self.toDestination = self.destinationStationPosition - self.position

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
        if toTarget.x > -500.0 and toTarget.x < 500.0:
            targetDistance.x = 2.0 / (1.0 + math.exp(-2.0 * (toTarget.x / 500.0))) - 1.0 # sigmoiding distance
        else:
            targetDistance.x = 1.0
        if toTarget.y > -500.0 and toTarget.y < 500.0:
            targetDistance.y = 2.0 / (1.0 + math.exp(-2.0 * (toTarget.y / 500.0))) - 1.0 # sigmoiding distance
        else:
            targetDistance.y = 1.0

        return targetDistance

    def UpdateSenses(self):
        destinationDistance = self.SigmoidDistance(self.toDestination)
        agent1Distance = self.SigmoidDistance(self.toAgent1)
        agent2Distance = self.SigmoidDistance(self.toAgent2)
        agent3Distance = self.SigmoidDistance(self.toAgent3)
        agent4Distance = self.SigmoidDistance(self.toAgent4)

        angularVelocity_cw = 0.0
        if self.angularVelocity > 0.0:
            angularVelocity_cw = self.angularVelocity
        angularVelocity_ccw = 0.0
        if self.angularVelocity < 0.0:
            angularVelocity_ccw = -self.angularVelocity

        # update senses
        self.Senses[SenseType.BIAS.value] = self.biasValue
        self.Senses[SenseType.OSCILLATOR.value] = self.oscillatorValue
        self.Senses[SenseType.RANDOM_NOISE.value] = self.randomNoiseValue
        self.Senses[SenseType.WEIGHT.value] = self.weight / (AGENT_WEIGHT + MAX_PARTWEIGHT)
        self.Senses[SenseType.VELOCITY_X.value] = self.velocity.x / AGENT_MAX_VELOCITY
        self.Senses[SenseType.VELOCITY_Y.value] = self.velocity.y / AGENT_MAX_VELOCITY
        self.Senses[SenseType.ANGULARVELOCITY_CW.value] = angularVelocity_cw / AGENT_MAX_ANGULARVELOCITY
        self.Senses[SenseType.ANGULARVELOCITY_CCW.value] = angularVelocity_ccw / AGENT_MAX_ANGULARVELOCITY

        # self.Senses[SenseType.HEADING_DIFF_DESTINATION.value] = self.randomNoiseValue

        self.Senses[SenseType.DISTANCE_X_DESTINATION.value] = destinationDistance.x / WORLD_SIZE
        self.Senses[SenseType.DISTANCE_Y_DESTINATION.value] = destinationDistance.y / WORLD_SIZE
        self.Senses[SenseType.DISTANCE_X_AGENT1.value] = agent1Distance.x / WORLD_SIZE
        self.Senses[SenseType.DISTANCE_Y_AGENT1.value] = agent1Distance.y / WORLD_SIZE
        self.Senses[SenseType.DISTANCE_X_AGENT2.value] = agent2Distance.x / WORLD_SIZE
        self.Senses[SenseType.DISTANCE_Y_AGENT2.value] = agent2Distance.y / WORLD_SIZE
        self.Senses[SenseType.DISTANCE_X_AGENT3.value] = agent3Distance.x / WORLD_SIZE
        self.Senses[SenseType.DISTANCE_Y_AGENT3.value] = agent3Distance.y / WORLD_SIZE
        self.Senses[SenseType.DISTANCE_X_AGENT4.value] = agent4Distance.x / WORLD_SIZE
        self.Senses[SenseType.DISTANCE_Y_AGENT4.value] = agent4Distance.y / WORLD_SIZE
        
    def ExecuteActions(self):
        self.Actions = self.net.Calculate(self.Senses)
        idxMax = max(self.Actions, key=self.Actions.get)
        powerVector = pygame.Vector2(0.0, 0.0)
        if idxMax == ActionType.MOVE_NORTH.value:
            powerVector = pygame.Vector2(0.0, -1.0)
        if idxMax == ActionType.MOVE_SOUTH.value:
            powerVector = pygame.Vector2(0.0, 1.0)
        if idxMax == ActionType.MOVE_EAST.value:
            powerVector = pygame.Vector2(1.0, 0.0)
        if idxMax == ActionType.MOVE_WEST.value:
            powerVector = pygame.Vector2(-1.0, 0.0)
        pygame.Vector2.scale_to_length(powerVector, 0.1)
        self.velocity = self.velocity + powerVector
    
    def ClampVelocity(self):
        if pygame.Vector2.length(self.velocity) > AGENT_MAX_VELOCITY:
            pygame.Vector2.scale_to_length(self.velocity, AGENT_MAX_VELOCITY)
        # elif pygame.Vector2.length(self.velocity) > self.maxVelocity:
        #     pygame.Vector2.scale_to_length(self.velocity, self.maxVelocity)
        if self.angularVelocity > AGENT_MAX_ANGULARVELOCITY:
            self.angularVelocity = AGENT_MAX_ANGULARVELOCITY
        elif self.angularVelocity < -AGENT_MAX_ANGULARVELOCITY:
            self.angularVelocity = -AGENT_MAX_ANGULARVELOCITY
        
    def SetFitnessAdjustment(self, fitnessAdjustment : float):
        self.fitness += fitnessAdjustment

    def GetFitness(self):
        return self.fitness
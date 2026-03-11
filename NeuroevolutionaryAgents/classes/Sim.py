from PoissonSamplingGenerator import *

from configNeuroevolutionaryAgents import *

from Part import *
from Station import *

from Neuron import *
from NeuralNetwork import *
from Agent import *
from Genome import *
from Breed import *
from EvolutionManager import *

class Sim:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.poissonGenerator = PoissonSamplingGenerator.PoissonGenerator(num_dim = 2, disk = False, repeatPattern = False, first_point_zero = False)

        self.timeStep = 0
        self.Stations = {}

        self.evolutionManager = EvolutionManager()
        self.evolutionManager.GenerateGenesisGenome()
        self.Agents = []
        for i in range(MAX_AGENTS):
            self.Agents.append(self.evolutionManager.GenerateGenesisAgent())
            
        self.imgFood = pygame.image.load('../assets/food.png').convert()
        self.imgHerbivore = pygame.image.load('../assets/herbivore.png').convert()
        self.imgCarnivore = pygame.image.load('../assets/carnivore.png').convert()

    def Initialize(self):
        Positions = self.poissonGenerator.find_point_set(num_points = MAX_STATIONS, num_iterations = 4, iterations_per_point = 128, num_rotations = 1)
        Positions = self.poissonGenerator.cache_sort(points, sorting_buckets = 0)
        for position in Positions:
            newStation = Station(stationId, position)
            self.Stations[stationId] = newStation

    def Reset(self):
        self.timeStep = 0
        self.Stations = {}

    def HandleCollisions(self):
        for chunk in self.world.Chunks:
            for agentAggressor in self.Agents:
                if self.IsInChunkRadius(agentAggressor.GetPosition(), chunk.x_idx, chunk.x_idx):
                    if agentAggressor.herbivore:
                        for food in self.world.Food:
                            if self.IsInChunkRadius(food.GetPosition(), chunk.x_idx, chunk.x_idx):
                                if pygame.Vector2.distance_to(agentAggressor.position, food.position) < agentAggressor.size / 2.0 + food.size / 2.0:
                                    agentAggressor.SetSatiationAdjustment(+1.0 * agentAggressor.attackPower)
                                    food.SetHealthAdjustment(-1.0 * agentAggressor.attackPower)
                                    agentAggressor.SetFitnessAdjustment(+1.0)
                    elif agentAggressor.carnivore:
                        for agentTarget in self.Agents:
                            if self.IsInChunkRadius(agentTarget.GetPosition(), chunk.x_idx, chunk.x_idx):
                                if pygame.Vector2.distance_to(agentAggressor.position, agentTarget.position) < agentAggressor.size / 2.0 + agentTarget.size / 2.0:
                                    agentAggressor.SetSatiationAdjustment(+1.0 * agentAggressor.attackPower)
                                    agentTarget.SetHealthAdjustment(-1.0 * agentAggressor.attackPower)
                                    agentAggressor.SetHealthAdjustment(-0.2 * agentTarget.attackPower)
                                    agentAggressor.SetFitnessAdjustment(+1.0)
                                    agentTarget.SetFitnessAdjustment(-1.0)

    def UpdateTargets(self):
        for chunk in self.world.Chunks:
            idx_agentAggressor = 0
            for agentAggressor in self.Agents:
                if self.IsInChunkRadius(agentAggressor.GetPosition(), chunk.x_idx, chunk.x_idx):
                    if agentAggressor.herbivore:
                        distanceToClosestFood = 2000.0
                        newDistanceToClosestFood = distanceToClosestFood
                        idx_closestFood = 0
                        for food in self.world.Food:
                            if self.IsInChunkRadius(food.GetPosition(), chunk.x_idx, chunk.x_idx):
                                newDistanceToClosestFood = pygame.Vector2.distance_to(agentAggressor.position, food.position)
                                if newDistanceToClosestFood < distanceToClosestFood:
                                    distanceToClosestFood = newDistanceToClosestFood
                                    idx_closestFood = self.world.Food.index(food)
                        agentAggressor.UpdateTargetHealthFraction(self.world.Food[idx_closestFood].GetHealthFraction())
                        agentAggressor.UpdatToTarget(self.world.Food[idx_closestFood].GetPosition())
                        agentAggressor.UpdateTargetVelocity(self.world.Food[idx_closestFood].GetVelocity())
                    elif agentAggressor.carnivore:
                        distanceToClosestAgent = 2000.0
                        newDistanceToClosestAgent = distanceToClosestAgent
                        idx_closestAgentTarget = 0
                        for agentTarget in self.Agents:
                            if idx_agentAggressor == idx_closestAgentTarget: # skip the aggressor itself
                                idx_closestAgentTarget += 1
                                continue
                            if self.IsInChunkRadius(agentTarget.GetPosition(), chunk.x_idx, chunk.x_idx):
                                newDistanceToClosestAgent = pygame.Vector2.distance_to(agentAggressor.position, agentTarget.position)
                                if newDistanceToClosestAgent < distanceToClosestFood:
                                    distanceToClosestFood = newDistanceToClosestAgent
                                    idx_closestAgentTarget = self.Agents.index(agentTarget)
                        agentAggressor.UpdateTargetHealthFraction(self.Agents[idx_closestAgentTarget].GetHealthFraction())
                        agentAggressor.UpdatToTarget(self.Agents[idx_closestAgentTarget].GetPosition())
                        agentAggressor.UpdateTargetVelocity(self.Agents[idx_closestAgentTarget].GetVelocity())
                idx_agentAggressor += 1
                
    def Update(self):
        # remove entities
        for food in self.world.Food:
            if food.health <= 0.0:
                self.world.Food.remove(food)
                break
        for agent in self.Agents:
            if agent.health <= 0.0:
                self.Agents.remove(agent)
                break
        # update entities
        for food in self.world.Food:
            food.UpdatePosition()
            # clamp food position
            if food.position.x < 0.0:
                food.position.x = float(SCREEN_WIDTH)
            elif food.position.x > float(SCREEN_WIDTH):
                food.position.x = 0.0
            elif food.position.y < 0.0:
                food.position.y = float(SCREEN_HEIGHT)
            elif food.position.y > float(SCREEN_HEIGHT):
                food.position.y = 0.0
        for agent in self.Agents:
            agent.UpdatePosition()
            # clamp agent position
            if agent.position.x < 0.0:
                agent.position.x = float(SCREEN_WIDTH)
            elif agent.position.x > float(SCREEN_WIDTH):
                agent.position.x = 0.0
            elif agent.position.y < 0.0:
                agent.position.y = float(SCREEN_HEIGHT)
            elif agent.position.y > float(SCREEN_HEIGHT):
                agent.position.y = 0.0
            agent.UpdateSatiation()
            agent.UpdateHunger()
            agent.UpdateOscillator()
            agent.UpdateRandomNoise()
            agent.UpdateSenses()
            agent.ExecuteActions()
            agent.ClampVelocity()
        # update targets
        self.UpdateTargets()
        # handle collisions
        self.HandleCollisions()
        # add entities
        if len(self.world.Food) < MAX_FOOD:
            self.world.GenerateFood()
        if len(self.Agents) < MAX_AGENTS:
            self.Agents.append(self.evolutionManager.GenerateGenesisAgent())
        self.UpdateTimeStep()

    def UpdateTimeStep(self):
        self.timeStep += 1
        print(self.timeStep)

    def IsInChunkRadius(self, position : pygame.Vector2, chunk_x_idx : int, chunk_y_idx : int):
        if position.x >= float((chunk_x_idx - 1) * CHUNK_SIZE) and position.x < float(CHUNK_SIZE + (chunk_x_idx + 1) * CHUNK_SIZE):
            if position.y >= float((chunk_y_idx - 1) * CHUNK_SIZE) and position.y < float(CHUNK_SIZE + (chunk_y_idx + 1) * CHUNK_SIZE):
                return True
        return False

    def Draw(self):
        self.screen.fill(COLOR_BACKGROUND)
        for food in self.world.Food:
            self.DrawFood(food)
        for agent in self.Agents:
            self.DrawAgent(agent)
        self.fps_counter()
        pygame.display.update()
        self.clock.tick(FPS)

    def DrawAgent(self, agent : Agent):
        if agent.herbivore:
            # self.screen.blit(self.imgHerbivore, (agent.position.x - agent.size / 2.0,  agent.position.y - agent.size / 2.0))
            pygame.draw.circle(self.screen, COLOR_HERBIVORE, agent.position, agent.size / 2.0)
        if agent.carnivore:
            # self.screen.blit(self.imgCarnivore, (agent.position.x - agent.size / 2.0,  agent.position.y - agent.size / 2.0))
            pygame.draw.circle(self.screen, COLOR_CARNIVORE, agent.position, agent.size / 2.0)

    def DrawFood(self, food : Food):
        # self.screen.blit(self.imgFood, (food.position.x - food.size / 2.0,  food.position.y - food.size / 2.0))
        pygame.draw.circle(self.screen, COLOR_FOOD, food.position, food.size / 2.0)

    def fps_counter(self):
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps , 1, pygame.Color("RED"))
        self.screen.blit(fps_t,(0,0))
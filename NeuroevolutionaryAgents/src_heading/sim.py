import poissonSamplingGenerator

from configNeuroevolutionaryAgents import *

from part import *
from station import *

from neuron import *
from neuralNetwork import *
from agent import *
from genome import *
from breed import *
from evolutionManager import *

class Sim:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.poissonGenerator = poissonSamplingGenerator.PoissonGenerator(num_dim = 2, disk = False, repeatPattern = False, first_point_zero = False)

        self.timeStep = 0
        self.Stations = {}
        self.windVelocity = pygame.Vector2(0.0, 0.0)

        self.evolutionManager = EvolutionManager()
        self.evolutionManager.GenerateGenesisGenome()
        self.Agents = []

    def Initialize(self):
        Positions = self.poissonGenerator.find_point_set(num_points = MAX_STATIONS, num_iter = 4, iterations_per_point = 128, rotations = 1)
        Positions = self.poissonGenerator.cache_sort(Positions, sorting_buckets = 0)
        stationId = 1
        for position in Positions:
            stationPosition = pygame.Vector2(position[0] * WORLD_SIZE, position[1] * WORLD_SIZE)
            if stationPosition.x < WORLD_BORDER:
                stationPosition.x = WORLD_BORDER
            elif stationPosition.x > WORLD_SIZE - WORLD_BORDER:
                stationPosition.x = WORLD_SIZE - WORLD_BORDER
            if stationPosition.y < WORLD_BORDER:
                stationPosition.y = WORLD_BORDER
            elif stationPosition.y > WORLD_SIZE - WORLD_BORDER:
                stationPosition.y = WORLD_SIZE - WORLD_BORDER
            newStation = Station(stationId, stationPosition)
            self.Stations[stationId] = newStation
            stationId += 1

        for i in range(MAX_AGENTS):
            self.Agents.append(self.evolutionManager.GenerateGenesisAgent(self.Stations[i+1].position))

        # windVelocity_x = WIND_SCALE * random.gauss(0.0, 0.5)
        # if (windVelocity_x > WIND_MAX_VELOCITY):
        #     windVelocity_x = WIND_MAX_VELOCITY
        # if (windVelocity_x < -WIND_MAX_VELOCITY):
        #     windVelocity_x = -WIND_MAX_VELOCITY
        # windVelocity_y = WIND_SCALE * random.gauss(0.0, 0.5)
        # if (windVelocity_x > WIND_MAX_VELOCITY):
        #     windVelocity_x = WIND_MAX_VELOCITY
        # if (windVelocity_x < -WIND_MAX_VELOCITY):
        #     windVelocity_x = -WIND_MAX_VELOCITY
        # self.windVelocity = pygame.Vector2(windVelocity_x, windVelocity_y)

        self.windVelocity = pygame.Vector2(0.0, 0.0)

    def Reset(self):
        self.timeStep = 0
        self.Stations = {}

    def UpdateStations(self):
        for stationId, station in self.Stations.items():
            station.GeneratePart()
            for agent in self.Agents:
                if station.position.distance_to(agent.position) < STATION_SIZE:
                    if len(agent.Parts) > 0:
                        if agent.Parts[-1].destinationId == stationId:
                            agent.DeliverPart()
                            agent.ResetWeight()
                            agent.SetFitnessAdjustment(+50.0)
                    else:
                        if (len(station.Parts) > 0):
                            partToWithdraw = station.WithdrawPart()
                            agent.InsertPart(partToWithdraw)
                            agent.SetWeight(partToWithdraw.weight)

    def UpdateAgents(self):
        currentAgentIdx = 0
        for currentAgent in self.Agents:
            currentAgent.SetFitnessAdjustment(-1.0)

            currentAgent.UpdatePosition(self.windVelocity)
            currentAgent.ClampPosition()
            currentAgent.UpdateHeading()

            if len(currentAgent.Parts) > 0:
                currentAgent.destinationStationPosition = self.Stations[currentAgent.Parts[-1].destinationId].position

            currentAgent.UpdateToDestination()

            OtherAgents = self.Agents[:currentAgentIdx] + self.Agents[currentAgentIdx + 1:]
            otherAgentIdx = 0
            for otherAgent in OtherAgents:
                if otherAgentIdx == 0:
                    agent1Position = otherAgent.GetPosition()
                elif otherAgentIdx == 1:
                    agent2Position = otherAgent.GetPosition()
                elif otherAgentIdx == 2:
                    agent3Position = otherAgent.GetPosition()
                elif otherAgentIdx == 3:
                    agent4Position = otherAgent.GetPosition()

                if currentAgent.position.distance_to(otherAgent.position) < AGENT_RANGE:
                    currentAgent.SetFitnessAdjustment(-2.0)

                otherAgentIdx += 1

            currentAgent.UpdateToAgents(
                agent1Position,
                agent2Position,
                agent3Position,
                agent4Position)
            currentAgent.UpdateOscillator()
            currentAgent.UpdateRandomNoise()
            currentAgent.UpdateSenses()
            currentAgent.ExecuteActions()
            currentAgent.ClampVelocity()

            currentAgentIdx += 1

    def Update(self):
        self.UpdateAgents()
        self.UpdateStations()

        self.timeStep += 1

    def Draw(self):
        self.screen.fill(COLOR_BACKGROUND)
        
        for agent in self.Agents:
            pygame.draw.circle(self.screen, COLOR_AGENT_RANGE, agent.position * SCREEN_SCALE, AGENT_RANGE / 2.0 * SCREEN_SCALE)

        for stationId, station in self.Stations.items():
            pygame.draw.circle(self.screen, COLOR_STATION, station.position * SCREEN_SCALE, STATION_SIZE / 2.0 * SCREEN_SCALE)

        for agent in self.Agents:
            if len(agent.Parts) > 0:
                pygame.draw.circle(self.screen, COLOR_AGENT_FULL, agent.position * SCREEN_SCALE, AGENT_SIZE / 2.0 * SCREEN_SCALE)
            else:
                pygame.draw.circle(self.screen, COLOR_AGENT_EMPTY, agent.position * SCREEN_SCALE, AGENT_SIZE / 2.0 * SCREEN_SCALE)

        self.DrawFPSCounter()
        pygame.display.update()
        self.clock.tick(FPS)

    def DrawFPSCounter(self):
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps , 1, pygame.Color("RED"))
        self.screen.blit(fps_t,(0,0))
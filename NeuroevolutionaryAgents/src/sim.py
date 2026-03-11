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
        self.generation = 0

        self.Stations = {}

        self.counterRandomNoise = 0
        self.noiseGenerator_windX = OpenSimplex(seed=random.randint(-10000, 10000))
        self.noiseGenerator_windY = OpenSimplex(seed=random.randint(-10000, 10000))
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

        stationId = 1
        for i in range(MAX_AGENTS):
            self.Agents.append(self.evolutionManager.GenerateGenesisAgent(self.Stations[stationId].position))
            stationId += 1
            if stationId > MAX_STATIONS:
                stationId = 1

        self.timeStep = 0
        self.generation = 0
        print("Generation: ", self.generation)

    def Reset(self):
        self.timeStep = 0
        self.Stations = {}

        self.counterRandomNoise = 0
        self.noiseGenerator_windX = OpenSimplex(seed=random.randint(-10000, 10000))
        self.noiseGenerator_windY = OpenSimplex(seed=random.randint(-10000, 10000))
        self.windVelocity = pygame.Vector2(0.0, 0.0)

    def UpdateWind(self):
        self.windVelocity.x = self.noiseGenerator_windX.noise2(WIND_NOISE_FREQUENCY * float(self.counterRandomNoise), 0.0)
        self.windVelocity.y = self.noiseGenerator_windY.noise2(WIND_NOISE_FREQUENCY * float(self.counterRandomNoise), 0.0)
        if pygame.Vector2.length(self.windVelocity) > 0.0:
            # pygame.Vector2.scale_to_length(self.windVelocity, WIND_MAX_FORCE)
            self.windVelocity = self.windVelocity * WIND_MAX_FORCE
        self.counterRandomNoise += 1

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
                    currentAgent.SetFitnessAdjustment(-1.0)

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
            currentAgent.UpdateVelocity()

            currentAgentIdx += 1

    def Update(self):
        self.UpdateWind()
        self.UpdateAgents()
        self.UpdateStations()
        self.timeStep += 1
        if self.timeStep > EVOLUTION_INTERVAL:
            self.NewAgents = self.evolutionManager.Evolve(self.Agents, self.Stations)
            self.Agents.clear()
            self.Agents = self.NewAgents
            self.timeStep = 0
            self.generation += 1
            print("Generation: ", self.generation)

    def Draw(self):
        self.screen.fill(COLOR_BACKGROUND)
        
        for agent in self.Agents:
            pygame.draw.circle(self.screen, COLOR_AGENT_RANGE, agent.position * SCREEN_SCALE, AGENT_RANGE * SCREEN_SCALE)

        for stationId, station in self.Stations.items():
            pygame.draw.circle(self.screen, COLOR_STATION, station.position * SCREEN_SCALE, STATION_SIZE * SCREEN_SCALE)

        for agent in self.Agents:
            if len(agent.Parts) > 0:
                pygame.draw.circle(self.screen, COLOR_AGENT_FULL, agent.position * SCREEN_SCALE, AGENT_SIZE * SCREEN_SCALE)
            else:
                pygame.draw.circle(self.screen, COLOR_AGENT_EMPTY, agent.position * SCREEN_SCALE, AGENT_SIZE * SCREEN_SCALE)

        self.DrawFPSCounter()
        self.DrawWindIndicator()
        pygame.display.update()
        self.clock.tick(FPS)

    def DrawFPSCounter(self):
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps , 1, pygame.Color("RED"))
        self.screen.blit(fps_t,(0,0))

    def DrawWindIndicator(self):
        # Bottom-left corner position
        base_pos = pygame.Vector2(50, self.screen.get_height() - 50)
        # Normalize and scale for arrow length
        if self.windVelocity.length() > 0:
            direction = self.windVelocity.normalize()
        else:
            direction = pygame.Vector2(0, 0)
        arrow_length = 40  # Fixed display length
        end_pos = base_pos + direction * arrow_length
        # Draw arrow shaft
        pygame.draw.line(self.screen, (255, 255, 255), base_pos, end_pos, 3)
        # Draw arrowhead
        angle = math.atan2(direction.y, direction.x)
        head_size = 8
        left = end_pos + pygame.Vector2(math.cos(angle + math.pi * 0.75),
                                        math.sin(angle + math.pi * 0.75)) * head_size
        right = end_pos + pygame.Vector2(math.cos(angle - math.pi * 0.75),
                                        math.sin(angle - math.pi * 0.75)) * head_size
        pygame.draw.polygon(self.screen, (255, 255, 255), [end_pos, left, right])
        # Draw magnitude text
        magnitude_text = self.font.render(f"{self.windVelocity.length():.1f}", True, (255, 255, 255))
        self.screen.blit(magnitude_text, (base_pos.x + 50, base_pos.y - 0))
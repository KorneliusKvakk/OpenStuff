from configNeuroevolutionaryAgents import *

class Entity:
    def __init__(self, initialPosition : pygame.Vector2):
        self.position = initialPosition
        self.weight = AGENT_WEIGHT
        self.velocity = pygame.Vector2(0.0, 0.0)
        self.maxVelocity = AGENT_MAX_VELOCITY

    def SetWeight(self, partWeight : float):
        self.weight += partWeight

    def ResetWeight(self):
        self.weight = AGENT_WEIGHT

    def UpdatePosition(self, windVelocity : pygame.Vector2):
        self.position = self.position + self.velocity + windVelocity

    def ClampPosition(self):
        if self.position.x < 0.0:
            self.position.x = 0.0
        elif self.position.x > WORLD_SIZE:
            self.position.x = WORLD_SIZE
        if self.position.y < 0.0:
            self.position.y = 0.0
        elif self.position.y > WORLD_SIZE:
            self.position.y = WORLD_SIZE

    def UpdateVelocity(self):
        self.velocity = self.velocity - self.velocity * AGENT_DRAGCOEFFICIENT
        self.maxVelocity = AGENT_MAX_VELOCITY - (self.weight / (AGENT_WEIGHT + MAX_PARTWEIGHT)) * AGENT_MAX_VELOCITY * 0.5
        if pygame.Vector2.length(self.velocity) > AGENT_MAX_VELOCITY:
            pygame.Vector2.scale_to_length(self.velocity, AGENT_MAX_VELOCITY)
        elif pygame.Vector2.length(self.velocity) > self.maxVelocity:
            pygame.Vector2.scale_to_length(self.velocity, self.maxVelocity)
            
    def GetPosition(self):
        return self.position

    def GetVelocity(self):
        return self.velocity
from configNeuroevolutionaryAgents import *

class Entity:
    def __init__(self, initialPosition : pygame.Vector2):
        self.position = initialPosition
        self.weight = AGENT_WEIGHT
        self.velocity = pygame.Vector2(0.0, 0.0)
        self.heading_deg = 0.0
        self.angularVelocity = 0.0

    def SetWeight(self, partWeight : float):
        self.weight += partWeight

    def ResetWeight(self):
        self.weight = AGENT_WEIGHT

    def UpdatePosition(self, windVelocity : pygame.Vector2):
        self.position = self.position + self.velocity + windVelocity

    def ClampPosition(self):
        if self.position.x < 0.0:
            self.position.x = 0.0
        elif self.position.x > float(WORLD_SIZE):
            self.position.x = float(WORLD_SIZE)
        elif self.position.y < 0.0:
            self.position.y = 0.0
        elif self.position.y > float(WORLD_SIZE):
            self.position.y = float(WORLD_SIZE)

    def UpdateHeading(self):
        self.heading_deg += self.angularVelocity
        if (self.heading_deg > 360.0):
            self.heading_deg -= 360.0
        elif (self.heading_deg < 0.0):
            self.heading_deg += 360.0

    def GetPosition(self):
        return self.position

    def GetVelocity(self):
        return self.velocity